import pickle
import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

# Load model
with open("models/email_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/email_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


# 🔹 Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z₹$]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)


# 🔹 Combine subject + body
def prepare_email(subject, body):
    return subject + " " + body


# 🔹 ML score
def get_ml_score(subject, body):
    text = prepare_email(subject, body)
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    prob = model.predict_proba(vectorized)[0][1]
    return prob


# 🔥 Rule-based boost (email specific)
def rule_boost(text):
    text = text.lower()
    boost = 0
    reasons = []

    # 🔴 Urgency
    if "urgent" in text or "immediately" in text:
        boost += 0.10
        reasons.append("Uses urgency language")

    # 🔴 Phishing actions
    if "verify" in text:
        boost += 0.10
        reasons.append("Requests account verification")

    if "update account" in text:
        boost += 0.10
        reasons.append("Asks to update account details")

    if "click" in text:
        boost += 0.10
        reasons.append("Asks to click a link")

    # 🔴 Links
    if "http" in text or "www" in text:
        boost += 0.15
        reasons.append("Contains suspicious link")

    # 🔴 Money / reward
    if "₹" in text or "$" in text:
        boost += 0.10
        reasons.append("Mentions money")

    if "winner" in text or "lottery" in text:
        boost += 0.15
        reasons.append("Prize/lottery related content")

    # 🔥 Job scams (same logic as SMS)
    job_keywords = [
        "earn", "income", "job", "work from home",
        "part time", "limited slots", "no experience"
    ]

    matches = sum(1 for word in job_keywords if word in text)

    if matches >= 3:
        boost += 0.45
        reasons.append("Strong job scam pattern detected")
    elif matches == 2:
        boost += 0.30
        reasons.append("Possible job scam indicators")

    return boost, reasons

# 🔹 Final prediction
def predict_email(subject, body, threshold=0.35):
    text = subject + " " + body

    ml_score = get_ml_score(subject, body)   # 0–1
    boost, reasons = rule_boost(text)

    final_score = min(ml_score + boost, 1.0)

    if final_score >= threshold:
        label = "Scam"
    else:
        label = "Genuine"

    return label, round(final_score * 100, 2), reasons