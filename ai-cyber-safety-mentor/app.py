from flask import Flask, render_template, request, jsonify
import joblib
import re

app = Flask(__name__)

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

    return jsonify({
        "label": label,
        "confidence": hybrid_score,
        "ml_probability": round(ml_prob, 2),
        "triggers": triggers
    })


if __name__ == '__main__':
    app.run(debug=True)