from flask import Flask, render_template, request, jsonify, session
import joblib
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load ML model
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "scam_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "vectorizer.pkl"))

# Psychological trigger keywords
urgency_words = ["urgent", "immediately", "now", "expire", "limited"]
authority_words = ["bank", "rbi", "income tax", "police", "govt"]
fear_words = ["blocked", "suspended", "penalty", "legal action"]
reward_words = ["won", "reward", "cashback", "lottery", "prize"]

def rule_based_score(message):
    score = 0
    triggers = []
    msg = message.lower()

    # Suspicious link
    if re.search(r"(http[s]?://|www\.|bit\.ly|tinyurl\.com)", msg):
        score += 20
        triggers.append("Suspicious Link")

    # Phone number detection
    if re.search(r"\b\d{10}\b", msg) or re.search(r"\+?\d{1,3}[\s-]?\d{6,12}", msg):
        score += 20
        triggers.append("Suspicious Contact Number")

    # Email detection
    if re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", msg):
        score += 10
        triggers.append("External Contact Channel")

    # Imperative verbs
    if any(word in msg for word in ["call", "claim", "verify", "confirm", "act now", "contact"]):
        score += 10
        triggers.append("Direct Action Pressure")

    # Urgency
    if any(word in msg for word in urgency_words):
        score += 15
        triggers.append("Urgency Manipulation")

    # Authority
    if any(word in msg for word in authority_words):
        score += 15
        triggers.append("Authority Impersonation")

    # Fear
    if any(word in msg for word in fear_words):
        score += 15
        triggers.append("Fear Tactic")

    # Reward + congratulations pattern
    if "congratulations" in msg and any(word in msg for word in reward_words):
        score += 25
        triggers.append("Unsolicited Prize Claim")

    # Basic reward detection
    elif any(word in msg for word in reward_words):
        score += 15
        triggers.append("Reward Lure")

    # 🔥 Signal Stacking Amplification
    if len(triggers) >= 3:
        score += 15
        triggers.append("Multi-Signal Manipulation")

    return score, triggers

def generate_learning_cards(triggers):
    learning_content = []

    mapping = {
        "Suspicious Link": "Always verify URLs carefully. Fraud links often use slight spelling changes or shortened URLs.",
        "Urgency Manipulation": "Scammers create urgency to stop you from thinking rationally. Take your time before acting.",
        "Authority Impersonation": "Banks and RBI never ask for OTP or passwords over SMS or calls.",
        "Fear Tactic": "Threats of account suspension or legal action are common fear-based scam tactics.",
        "Reward Lure": "Unrealistic rewards or lottery winnings are major red flags.",
        "Multi-Signal Manipulation": "This message combines multiple psychological tactics. Multi-layered manipulation significantly increases scam risk."
    }

    for trigger in triggers:
        if trigger in mapping:
            learning_content.append(mapping[trigger])

    return learning_content

def generate_explanation(message, triggers, label):

    msg = message.lower()

    explanation_parts = []

    if "Suspicious Link" in triggers:
        explanation_parts.append(
            "The message contains an external link which may redirect users to a phishing website designed to steal credentials."
        )

    if "Direct Action Pressure" in triggers:
        explanation_parts.append(
            "The sender attempts to pressure the recipient into immediate action without allowing time for verification."
        )

    if "Urgency Manipulation" in triggers:
        explanation_parts.append(
            "Urgency tactics are used to create panic and force quick decision making."
        )

    if "Authority Impersonation" in triggers:
        explanation_parts.append(
            "The message appears to impersonate an authority such as a bank or government body."
        )

    if "Reward Lure" in triggers or "Unsolicited Prize Claim" in triggers:
        explanation_parts.append(
            "Promises of rewards or prizes are commonly used to lure victims into sharing sensitive information."
        )

    if not explanation_parts:
        explanation_parts.append(
            "No strong manipulation patterns were detected in this message."
        )

    explanation = " ".join(explanation_parts)

    return explanation

def generate_personalized_insight(triggers):

    vulnerability = session.get("vulnerability")

    # User never attempted simulator
    if not vulnerability:
        return "Try our phishing simulator to unlock personalized scam detection insights based on your behavioral patterns."

    # Determine dominant weakness
    dominant = max(vulnerability, key=vulnerability.get)

    mapping = {
        "urgency": "Urgency Manipulation",
        "authority": "Authority Impersonation",
        "reward": "Reward Lure",
        "link": "Suspicious Link"
    }

    dominant_trigger = mapping.get(dominant)

    # If scam message uses the same weakness
    if dominant_trigger in triggers:
        return f"This message uses {dominant_trigger.lower()}, which previously influenced your behavior during the phishing simulation."

    return None

import random
import phishing_dataset

def generate_scenario_from_dataset():
    categories = [
        ("bank", phishing_dataset.bank_scams),
        ("delivery", phishing_dataset.delivery_scams),
        ("reward", phishing_dataset.reward_scams),
        ("security", phishing_dataset.account_security_scams),
        ("government", phishing_dataset.government_scams)
    ]
    
    cat_name, cat_list = random.choice(categories)
    msg = random.choice(cat_list)
    
    flags = []
    msg_lower = msg.lower()
    
    if "http" in msg_lower or ".com" in msg_lower or ".co" in msg_lower or ".net" in msg_lower:
        flags.append("link")
        
    urgency_terms = ["immediate", "now", "urgen", "within", "today", "expir", "delay", "suspend", "freeze", "tonight", "hour", "minute"]
    if any(word in msg_lower for word in urgency_terms):
        flags.append("urgency")
        
    reward_terms = ["reward", "cash", "won", "prize", "offer", "bonus", "₹", "subsidy", "lottery"]
    if cat_name == "reward" or any(word in msg_lower for word in reward_terms):
        flags.append("reward")
        
    authority_terms = ["alert", "notice", "warning", "security", "government", "bank", "rbi", "sbi", "hdfc", "tax", "gst", "uidai", "amazon", "flipkart", "dhl", "fedex"]
    if cat_name in ["bank", "delivery", "security", "government"] or any(word in msg_lower for word in authority_terms):
        flags.append("authority")
        
    if cat_name == "reward":
        action = "ignore"
    else:
        action = "verify"
        
    return {
        "message": msg,
        "correct_flags": list(set(flags)),
        "correct_action": action,
        "category": cat_name
    }

@app.route("/generate_scam")
def generate_scam():
    scenario = generate_scenario_from_dataset()
    return {"message": scenario["message"]}

@app.route('/')
def home():
    profile_data = session.get("last_profile")
    return render_template("index.html", profile=profile_data)

@app.route('/scam-detection')
def scam_detection():
    return render_template("scam_detection.html")

@app.route('/voice-simulator')
def voice_simulator():
    return render_template("voice_simulator.html")


@app.route('/analyze', methods=['POST'])
def analyze():
    message = request.form.get("message")

    # ML Prediction
    msg_vector = vectorizer.transform([message])
    ml_prob = model.predict_proba(msg_vector)[0][1]  # Probability of scam

    # Rule Layer
    rule_score, triggers = rule_based_score(message)

    # Hybrid Score
    ml_component = ml_prob * 60
    rule_component = min(rule_score, 60)

    hybrid_score = int(min(ml_component + rule_component, 100))

    # Consensus boost when multiple signals align
    if ml_prob > 0.6 and len(triggers) >= 2:
        hybrid_score = min(hybrid_score + 8, 100)

    if hybrid_score >= 70:
        label = "High Risk Scam"
    elif hybrid_score >= 40:
        label = "Moderate Risk"
    else:
        label = "Likely Safe"

    session["messages_checked"] = session.get("messages_checked", 0) + 1

    if label == "High Risk Scam":
        session["threats_detected"] = session.get("threats_detected", 0) + 1

    learning_cards = generate_learning_cards(triggers)
    explanation = generate_explanation(message, triggers, label)
    personalized = generate_personalized_insight(triggers)

    return jsonify({
        "label": label,
        "confidence": hybrid_score,
        "ml_probability": round(ml_prob, 2),
        "triggers": triggers,
        "learning_cards": learning_cards,
        "explanation": explanation,
        "personalized": personalized
    })

@app.route('/challenge')
def challenge():
    session["risk_score"] = 100
    session["current_round"] = 0

    # Initialize vulnerability profile
    session["vulnerability"] = {
        "urgency": 0,
        "authority": 0,
        "reward": 0,
        "link": 0
    }

    # We will NOT pre-generate all scenarios anymore
    session["game_scenarios"] = []

    # Select first scenario randomly
    scenario = generate_scenario_from_dataset()

    # Save first scenario
    session["game_scenarios"].append(scenario)
    session.modified = True

    return render_template(
        "challenge.html",
        scenario=scenario,
        round=1,
        risk=session["risk_score"]
    )

@app.route('/submit_round', methods=['POST'])
def submit_round():
    selected_flags = request.form.getlist("flags")
    action = request.form.get("action")

    scenarios = session["game_scenarios"]

    if not scenarios:
        return jsonify({"error": "No active scenario"}), 400

    scenario = scenarios[-1]

    correct_flags = scenario["correct_flags"]
    correct_action = scenario["correct_action"]

    success = True
    round_penalty = 0

    # 🔴 1. Missed correct flags
    for flag in correct_flags:
        if flag not in selected_flags:
            round_penalty += 5
            success = False

            # Track vulnerability
            if flag in session["vulnerability"]:
                session["vulnerability"][flag] += 1

    # 🔴 2. Wrong extra flags selected
    for flag in selected_flags:
        if flag not in correct_flags:
            round_penalty += 3
            success = False

    # 🔴 3. Wrong action taken
    if action != correct_action:
        round_penalty += 15
        success = False

        # Most wrong actions happen under urgency pressure
        session["vulnerability"]["urgency"] += 1

    # 🔴 Deduct from immunity score
    session["risk_score"] -= round_penalty
    session["risk_score"] = max(0, session["risk_score"])

    session["current_round"] += 1
    game_over = session["current_round"] >= 7

    # --- Behavioral Insight (User-Focused) ---

    missed_flags = [flag for flag in correct_flags if flag not in selected_flags]
    wrong_flags = [flag for flag in selected_flags if flag not in correct_flags]

    insight_parts = []

    # Missed real red flags
    for flag in missed_flags:
        if flag == "urgency":
            insight_parts.append("You failed to identify time-pressure manipulation.")
        elif flag == "authority":
            insight_parts.append("You trusted authority-based messaging without verification.")
        elif flag == "reward":
            insight_parts.append("You were influenced by financial incentive lures.")
        elif flag == "link":
            insight_parts.append("You did not detect a deceptive link redirection attempt.")

    # Wrong action behavior
    if action != correct_action:
        if action in ["follow", "provide", "share"]:
            insight_parts.append("You engaged with a malicious prompt instead of verifying independently.")
        elif action == "ignore" and correct_action == "verify":
            insight_parts.append("You ignored a scenario requiring cautious verification.")
            
    # If user performed correctly
    if success:
        insight_parts.append("You demonstrated strong situational awareness and resisted manipulation tactics.")

    behavioral_insight = " ".join(insight_parts)

    
    return jsonify({
        "success": success,
        "score": session["risk_score"],
        "game_over": game_over,
        "selected_flags": selected_flags,
        "correct_flags": correct_flags,
        "action": action,
        "correct_action": correct_action,
        "behavioral_insight": behavioral_insight
    })

@app.route('/next_round')
def next_round():
    current_round = session["current_round"]
    vulnerability = session.get("vulnerability", {})

    # Decide scenario selection strategy
    if current_round < 2:
        # First 2 rounds are random
        scenario = generate_scenario_from_dataset()
    else:
        # Adaptive selection based on dominant vulnerability
        dominant = max(vulnerability, key=vulnerability.get)

        # Generate repeatedly until we find a match, capped at 10 times to prevent infinite loop
        scenario = generate_scenario_from_dataset()
        for _ in range(10):
            if dominant in scenario["correct_flags"]:
                break
            scenario = generate_scenario_from_dataset()

    # Save scenario to session history
    session["game_scenarios"].append(scenario)
    session.modified = True

    return render_template(
        "challenge.html",
        scenario=scenario,
        round=current_round + 1,
        risk=session["risk_score"]
    )

from flask import redirect

@app.route('/result')
def result():
    if session.get("current_round", 0) < 7: # if user tries to access result without completing the challenge
        return redirect("/challenge")
    final_score = session.get("risk_score", 0)

    session["simulations_run"] = session.get("simulations_run", 0) + 1

    if final_score < 60:
        session["high_risk_count"] = session.get("high_risk_count", 0) + 1

    session["avg_score"] = int(
        (session.get("avg_score", final_score) + final_score) / 2
    )

    history = session.get("score_history", [])
    history.append(final_score)

    session["score_history"] = history

    vulnerability = session.get("vulnerability", {})

    # Convert raw counts to percentage of total rounds
    total_rounds = 7
    if total_rounds == 0:
        total_rounds = 7  # safety fallback

    breakdown_percent = {
        k: int((min(v, total_rounds) / total_rounds) * 100)
        for k, v in vulnerability.items()
    }

    # Sort vulnerabilities by intensity
    sorted_vuln = sorted(vulnerability.items(), key=lambda x: x[1], reverse=True)

    top_trigger, top_value = sorted_vuln[0]

    # Generate dynamic analytical summary
    analysis_parts = []

    for trigger, value in sorted_vuln:
        if value > 0:
            analysis_parts.append(
                f"{trigger.capitalize()} manipulation patterns were triggered {value} time(s) during simulation."
            )

    if analysis_parts:
        analysis_summary = " ".join(analysis_parts)
    else:
        analysis_summary = "No major behavioral vulnerabilities were detected across the simulation rounds."

    # Intelligent recommendation logic based on intensity
    if top_value == 0:
        recommendation = "Your interaction profile indicates strong resistance to common manipulation tactics. Continue practicing safe verification habits."

    elif top_value == 1:
        recommendation = (
            f"Minor susceptibility detected in {top_trigger}-based scenarios. "
            "Slowing decision speed and independently verifying claims can further improve resilience."
        )

    else:
        recommendation = (
            f"Repeated behavioral exposure to {top_trigger}-driven manipulation patterns detected. "
            "Targeted awareness training for this trigger category is strongly advised."
        )

    # Verdict logic
    if final_score >= 85:
        verdict = "Cyber Guardian"
    elif final_score >= 60:
        verdict = "Aware but Vulnerable"
    else:
        verdict = "High Risk Target"

    if final_score >= 80:
        badge = "Cyber Defender"
    elif final_score >= 60:
        badge = "Security Aware"
    elif final_score >= 40:
        badge = "Vulnerable User"
    else:
        badge = "High Risk Target"

    print("FINAL PROFILE:", {
        "dominant_vulnerability": top_trigger,
        "vulnerability_score_breakdown": vulnerability,
        "analysis_summary": analysis_summary,
        "recommendation": recommendation,
        "badge": badge
    })

    session["last_profile"] = {
        "score": final_score,
        "verdict": verdict,
        "dominant": top_trigger,
        "breakdown": breakdown_percent,
        "badge": badge
    }
    
    return render_template(
        "result.html",
        score=final_score,
        verdict=verdict,
        dominant=top_trigger,
        breakdown=breakdown_percent,
        recommendation=recommendation,
        analysis=analysis_summary
    )

@app.route("/profile")
def profile():
    profile_data = session.get("last_profile")

    if profile_data and "breakdown" not in profile_data:
        profile_data["breakdown"] = {
            "authority": 0,
            "urgency": 0,
            "reward": 0,
            "fear": 0,
            "link": 0
        }

    if not profile_data:
        return render_template("profile.html", profile=None)

    # current score from latest profile
    current_score = profile_data["score"]

    # previous stored score
    previous_score = session.get("last_score")
    if previous_score is None:
        previous_score = current_score

    # update stored score for next time
    session["last_score"] = current_score

    return render_template(
        "profile.html",
        profile=profile_data,
        previous_score=previous_score,
        current_score=current_score
    )

from datetime import datetime

@app.route("/admin")
def admin_portal():
    current_time = datetime.now().strftime("%H:%M:%S")
    profile = session.get("last_profile")

    if not profile:
        profile = {
            "score": 0,
            "verdict": "No Data",
            "dominant": "None",
            "breakdown": {
                "authority": 0,
                "urgency": 0,
                "reward": 0,
                "fear": 0,
                "link": 0
            }
        }

    analytics = {
        "total_users": session.get("users_tested", 1),
        "simulations_completed": session.get("simulations_run", 1),
        "high_risk_users": session.get("high_risk_count", 0),
        "average_score": session.get("avg_score", profile["score"])
    }

    return render_template(
        "admin.html",
        profile=profile,
        analytics=analytics,
        current_time=current_time
    )

if __name__ == "__main__":
    app.run(debug=True)