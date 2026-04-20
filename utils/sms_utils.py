import pickle
import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

# Load model
with open("models/sms_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/sms_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


# 🔹 Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z₹$]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)


# 🔹 ML score (0–1)
def get_ml_score(text):
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    prob = model.predict_proba(vectorized)[0][1]
    return prob


def rule_boost(text):
    text = text.lower()
    boost = 0
    reasons = []

    # 🔴 Prize scams
    if "win" in text or "won" in text:
        boost += 0.15
        reasons.append("Winning/prize-related message")

    # 🔴 Urgency
    if "urgent" in text:
        boost += 0.10
        reasons.append("Uses urgency word")

    # 🔴 Action triggers
    if "click" in text:
        boost += 0.10
        reasons.append("Asks to click a link")

    if "verify" in text:
        boost += 0.10
        reasons.append("Requests verification")

    # 🔴 Links
    if "http" in text or "www" in text:
        boost += 0.15
        reasons.append("Contains a link")

    # 🔴 Money bait
    if "₹" in text or "$" in text:
        boost += 0.10
        reasons.append("Mentions money")

    # 🔥 NEW: JOB SCAM DETECTION
    job_keywords = [
        "earn", "daily", "income", "work from home",
        "job offer", "part time", "limited slots",
        "no experience", "start earning"
    ]

    matches = sum(1 for word in job_keywords if word in text)

    if matches >= 3:
        boost += 0.45
        reasons.append("Strong job scam pattern detected")
    elif matches == 2:
        boost += 0.30
        reasons.append("Possible job scam indicators")

    return boost, reasons

# 🔹 FINAL FUNCTION (MAIN FIX HERE)
def predict_sms(text, threshold=0.4):
    ml_score = get_ml_score(text)        # 0–1
    boost, reasons = rule_boost(text)    # 0–1

    final_score = min(ml_score + boost, 1.0)

    # Label decision
    if final_score >= threshold:
        label = "Scam"
    else:
        label = "Genuine"

    # Convert to percentage ONLY here
    percentage_score = round(final_score * 100, 2)

    return label, percentage_score, reasons