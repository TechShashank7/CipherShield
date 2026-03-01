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

    if re.search(r"http[s]?://", msg):
        score += 15
        triggers.append("Suspicious Link")

    if any(word in msg for word in urgency_words):
        score += 10
        triggers.append("Urgency Manipulation")

    if any(word in msg for word in authority_words):
        score += 10
        triggers.append("Authority Impersonation")

    if any(word in msg for word in fear_words):
        score += 10
        triggers.append("Fear Tactic")

    if any(word in msg for word in reward_words):
        score += 10
        triggers.append("Reward Lure")

    return score, triggers

def generate_learning_cards(triggers):
    learning_content = []

    mapping = {
        "Suspicious Link": "Always verify URLs carefully. Fraud links often use slight spelling changes or shortened URLs.",
        "Urgency Manipulation": "Scammers create urgency to stop you from thinking rationally. Take your time before acting.",
        "Authority Impersonation": "Banks and RBI never ask for OTP or passwords over SMS or calls.",
        "Fear Tactic": "Threats of account suspension or legal action are common fear-based scam tactics.",
        "Reward Lure": "Unrealistic rewards or lottery winnings are major red flags."
    }

    for trigger in triggers:
        if trigger in mapping:
            learning_content.append(mapping[trigger])

    return learning_content

import random

scenario_pool = [

    {
        "template": "RBI ALERT: Your bank account linked with Aadhaar ending ****{last4} has been temporarily restricted due to suspicious activity. Complete verification within 30 minutes at {link} to avoid permanent suspension.",
        "correct_flags": ["authority", "urgency", "link"],
        "correct_action": "verify"
    },

    {
        "template": "Income Tax Dept: Your refund of ₹{amount} has been approved for FY 2024-25. Submit your bank confirmation details at {link} before 6 PM today.",
        "correct_flags": ["authority", "link", "urgency"],
        "correct_action": "verify"
    },

    {
        "template": "Your UPI ID has been flagged for unusual transactions of ₹{amount}. If not verified within 15 minutes, outgoing transfers will be blocked. Update KYC here: {link}",
        "correct_flags": ["urgency", "link"],
        "correct_action": "verify"
    },

    {
        "template": "Congratulations! You’ve won ₹{amount} cashback under the Digital India Rewards Program. To receive the amount, confirm your mobile OTP now.",
        "correct_flags": ["reward", "authority"],
        "correct_action": "ignore"
    },

    {
        "template": "Dear Customer, your debit card ending ****{last4} was used for an international transaction. If this wasn’t you, call our emergency desk immediately at {phone}.",
        "correct_flags": ["urgency"],
        "correct_action": "verify"
    },

    {
        "template": "KYC UPDATE REQUIRED: As per RBI compliance norms, your bank account will be frozen within 24 hours if identity verification is not completed at {link}.",
        "correct_flags": ["authority", "urgency", "link"],
        "correct_action": "verify"
    },

    {
        "template": "Electricity Board Notice: Payment of ₹{amount} failed. Your connection will be disconnected tonight unless you confirm payment at {link}.",
        "correct_flags": ["authority", "urgency", "link"],
        "correct_action": "verify"
    },

    {
        "template": "Loan Pre-Approval Notice: You are eligible for a pre-approved loan of ₹{amount} at 0% processing fee. Activate offer immediately by submitting your Aadhaar and PAN details.",
        "correct_flags": ["reward", "urgency"],
        "correct_action": "ignore"
    },

    {
        "template": "Your SIM card will be deactivated within 2 hours due to KYC mismatch. Verify now at {link} to avoid permanent number suspension.",
        "correct_flags": ["urgency", "link"],
        "correct_action": "verify"
    },

    {
        "template": "Government Subsidy Update: You are shortlisted for the PM Financial Assistance Scheme. Confirm eligibility by sharing OTP sent to your registered number.",
        "correct_flags": ["authority"],
        "correct_action": "ignore"
    }
]

import random
import string

def generate_phone():
    return "+91 " + str(random.randint(6000000000, 9999999999))

def generate_fake_link():
    domains = [
        "rbi-secure-verification",
        "income-tax-refund",
        "upi-kyc-update",
        "govt-assistance-portal",
        "secure-bank-auth",
        "electricity-confirm",
        "sim-kyc-update"
    ]
    return "http://" + random.choice(domains) + ".in"

def generate_amount():
    return str(random.randint(1200, 95000))

def generate_last4():
    return str(random.randint(1000, 9999))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/scam-detection')
def scam_detection():
    return render_template("scam_detection.html")


@app.route('/analyze', methods=['POST'])
def analyze():
    message = request.form.get("message")

    # ML Prediction
    msg_vector = vectorizer.transform([message])
    ml_prob = model.predict_proba(msg_vector)[0][1]  # Probability of scam

    # Rule Layer
    rule_score, triggers = rule_based_score(message)

    # Hybrid Score
    hybrid_score = (ml_prob * 70) + rule_score
    hybrid_score = min(int(hybrid_score), 100)

    if hybrid_score >= 70:
        label = "High Risk Scam"
    elif hybrid_score >= 40:
        label = "Moderate Risk"
    else:
        label = "Likely Safe"

    learning_cards = generate_learning_cards(triggers)

    return jsonify({
        "label": label,
        "confidence": hybrid_score,
        "ml_probability": round(ml_prob, 2),
        "triggers": triggers,
        "learning_cards": learning_cards
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

    # Select first scenario randomly (no adaptation yet)
    scenario_template = random.choice(scenario_pool)

    # Generate realistic message from template
    msg = scenario_template["template"]
    msg = msg.replace("{phone}", generate_phone())
    msg = msg.replace("{link}", generate_fake_link())
    msg = msg.replace("{amount}", generate_amount())
    msg = msg.replace("{last4}", generate_last4())

    scenario = scenario_template.copy()
    scenario["message"] = msg

    # Save first scenario
    session["game_scenarios"].append(scenario)

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

    return jsonify({
        "success": success,
        "score": session["risk_score"],
        "game_over": game_over,
        "selected_flags": selected_flags,
        "correct_flags": correct_flags,
        "action": action,
        "correct_action": correct_action
    })

@app.route('/next_round')
def next_round():
    current_round = session["current_round"]
    vulnerability = session.get("vulnerability", {})

    # Decide scenario selection strategy
    if current_round < 2:
        # First 2 rounds are random
        scenario_template = random.choice(scenario_pool)
    else:
        # Adaptive selection based on dominant vulnerability
        dominant = max(vulnerability, key=vulnerability.get)

        adaptive_pool = [
            s for s in scenario_pool
            if dominant in s["correct_flags"]
        ]

        # Fallback if no matching scenario
        if not adaptive_pool:
            adaptive_pool = scenario_pool

        scenario_template = random.choice(adaptive_pool)

    # Generate realistic message
    msg = scenario_template["template"]
    msg = msg.replace("{phone}", generate_phone())
    msg = msg.replace("{link}", generate_fake_link())
    msg = msg.replace("{amount}", generate_amount())
    msg = msg.replace("{last4}", generate_last4())

    scenario = scenario_template.copy()
    scenario["message"] = msg

    # Save scenario to session history
    session["game_scenarios"].append(scenario)

    return render_template(
        "challenge.html",
        scenario=scenario,
        round=current_round + 1,
        risk=session["risk_score"]
    )

@app.route('/result')
def result():
    final_score = session.get("risk_score", 0)
    vulnerability = session.get("vulnerability", {})

    # Find dominant vulnerability
    dominant = max(vulnerability, key=vulnerability.get)

    # Recommendation mapping
    recommendations = {
        "urgency": "You tend to react under pressure. Practice slowing down before taking action.",
        "authority": "You trust official-looking messages easily. Always verify independently.",
        "reward": "You are attracted to reward-based offers. Be cautious of unrealistic benefits.",
        "link": "You may click suspicious links. Always inspect URLs carefully before opening."
    }

    recommendation = recommendations.get(dominant, "Stay alert and keep practicing.")

    if final_score >= 85:
        verdict = "Cyber Guardian"
    elif final_score >= 60:
        verdict = "Aware but Vulnerable"
    else:
        verdict = "High Risk Target"

    print("FINAL PROFILE:", {
        "dominant_vulnerability": dominant,
        "vulnerability_score_breakdown": vulnerability,
        "recommendation": recommendation
    })

    return render_template(
        "result.html",
        score=final_score,
        verdict=verdict,
        dominant=dominant,
        breakdown=vulnerability,
        recommendation=recommendation
    )

if __name__ == "__main__":
    app.run(debug=True)