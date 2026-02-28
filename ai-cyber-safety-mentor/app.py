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
        "message": "RBI Notice: Your account will be suspended. Verify immediately at http://rbi-secure.in",
        "correct_flags": ["link", "authority", "urgency"],
        "correct_action": "verify"
    },
    {
        "message": "You have won ₹75,000 cashback. Share OTP to claim now.",
        "correct_flags": ["reward", "urgency"],
        "correct_action": "ignore"
    },
    {
        "message": "Your electricity bill payment failed. Reconfirm details at http://pay-electricity.in",
        "correct_flags": ["link"],
        "correct_action": "verify"
    },
    {
        "message": "Bank alert: Suspicious login detected. Click link to secure account.",
        "correct_flags": ["link", "authority"],
        "correct_action": "verify"
    },
    {
        "message": "Dear customer, your KYC has expired. Update within 24 hours.",
        "correct_flags": ["authority", "urgency"],
        "correct_action": "verify"
    },
    {
        "message": "Income Tax refund approved. Submit bank details to receive ₹12,000.",
        "correct_flags": ["authority"],
        "correct_action": "verify"
    },
    {
        "message": "Your UPI account will be blocked. Update KYC immediately.",
        "correct_flags": ["urgency"],
        "correct_action": "verify"
    },
    {
        "message": "You are selected for a government scheme. Share OTP to confirm.",
        "correct_flags": ["authority"],
        "correct_action": "ignore"
    },
    {
        "message": "Your debit card has unusual activity. Call this number immediately.",
        "correct_flags": ["urgency"],
        "correct_action": "verify"
    },
    {
        "message": "Congratulations! You are eligible for exclusive loan benefits.",
        "correct_flags": ["reward"],
        "correct_action": "ignore"
    }
]

@app.route('/')
def home():
    return render_template("index.html")


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

    feedback = ""
    success = True

    # Flag scoring
    for flag in selected_flags:
        if flag in correct_flags:
            round_score += 5
        else:
            round_score -= 3
            success = False

    # Action scoring
    if action == correct_action:
        round_score += 10
    else:
        round_score -= 20
        success = False

    # Update risk
    session["risk_score"] += round_score
    session["risk_score"] = max(0, min(100, session["risk_score"]))

    # Prepare feedback message
    if success:
        feedback = "Excellent analysis! You identified the manipulation tactics correctly."
    else:
        feedback = "You fell into a manipulation pattern. Review the suspicious elements carefully next time."

    session["current_round"] += 1

    return render_template(
        "feedback.html",
        success=success,
        feedback=feedback,
        score=session["risk_score"]
    )

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

if __name__ == "__main__":
    app.run(debug=True)