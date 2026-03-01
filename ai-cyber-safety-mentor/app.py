from flask import Flask, render_template, request, jsonify, session
import joblib
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load ML model
model = joblib.load("scam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

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
    session["risk_score"] = 70
    session["current_round"] = 0

    shuffled = random.sample(scenario_pool, 7)

    # Generate realistic messages from templates
    for s in shuffled:
        msg = s["template"]
        msg = msg.replace("{phone}", generate_phone())
        msg = msg.replace("{link}", generate_fake_link())
        msg = msg.replace("{amount}", generate_amount())
        msg = msg.replace("{last4}", generate_last4())
        s["message"] = msg  # Create final message field

    session["game_scenarios"] = shuffled

    return render_template(
        "challenge.html",
        scenario=shuffled[0],
        round=1,
        risk=70
    )

@app.route('/submit_round', methods=['POST'])
def submit_round():
    selected_flags = request.form.getlist("flags")
    action = request.form.get("action")

    current_round = session["current_round"]
    scenarios = session["game_scenarios"]
    scenario = scenarios[current_round]

    round_score = 0
    correct_flags = scenario["correct_flags"]
    correct_action = scenario["correct_action"]

    success = True
    missed_flags = []

    # Flag scoring
    for flag in selected_flags:
        if flag in correct_flags:
            round_score += 5
        else:
            round_score -= 3
            success = False

    for flag in correct_flags:
        if flag not in selected_flags:
            missed_flags.append(flag)
            success = False

    # Action scoring
    if action == correct_action:
        round_score += 10
    else:
        round_score -= 20
        success = False

    session["risk_score"] += round_score
    session["risk_score"] = max(0, min(100, session["risk_score"]))
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
    scenario = session["game_scenarios"][current_round]

    return render_template(
        "challenge.html",
        scenario=scenario,
        round=current_round + 1,
        risk=session["risk_score"]
    )

@app.route('/result')
def result():
    final_score = session.get("risk_score", 0)

    # Temporary fallback until profiling engine integrated
    dominant_vulnerability = session.get("dominant_vulnerability", "urgency")
    recommendation = session.get(
        "recommendation",
        "Practice high-pressure scam simulations to improve resistance."
    )

    if final_score >= 85:
        verdict = "Cyber Guardian"
    elif final_score >= 60:
        verdict = "Aware but Vulnerable"
    else:
        verdict = "High Risk Target"

    return render_template(
        "result.html",
        score=final_score,
        verdict=verdict,
        dominant_vulnerability=dominant_vulnerability,
        recommendation=recommendation
    )

if __name__ == "__main__":
    app.run(debug=True)