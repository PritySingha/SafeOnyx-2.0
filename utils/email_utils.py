import pickle
import re
import os

import nltk
nltk_data_dir = os.path.join(os.path.dirname(__file__), "..", "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(os.path.abspath(nltk_data_dir))

try:
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords', download_dir=os.path.abspath(nltk_data_dir))
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))


with open("models/email_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/email_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


def clean_text(text):
    text = text.lower()
    text = text.replace("₹", " rupees ").replace("$", " dollar ")
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stop_words and len(w) > 1]
    return " ".join(words)


def get_ml_score(text):
    cleaned    = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    return float(model.predict_proba(vectorized)[0][1])


def rule_boost(text):
    t       = text.lower()
    boost   = 0.0
    reasons = []

    # — Urgency
    if re.search(r'\b(urgent|immediately|expire|account suspended|action required)\b', t):
        boost += 0.10
        reasons.append("Urgency / account-threat language")

    # — Phishing actions
    if re.search(r'\b(verify|confirm|validate)\b', t) and \
       re.search(r'\b(account|email|identity|details)\b', t):
        boost += 0.12
        reasons.append("Requests account verification")

    if re.search(r'\b(update|provide|submit)\b', t) and \
       re.search(r'\b(password|pin|details|information)\b', t):
        boost += 0.12
        reasons.append("Asks to submit sensitive details")

    # — Suspicious link
    if re.search(r'https?://|www\.', t):
        boost += 0.08
        reasons.append("Contains a URL")

    if re.search(r'\b(click here|click the link|click below)\b', t):
        boost += 0.10
        reasons.append("Suspicious call-to-action link")

    # — Money / prize
    if re.search(r'(₹|\$|rupees|dollar|rs\.?\s*\d+)', t):
        boost += 0.08
        reasons.append("Mentions money")

    if re.search(r'\b(winner|lottery|prize|lucky|reward|gift card)\b', t):
        boost += 0.15
        reasons.append("Prize or lottery content")

    # — Impersonation signals
    if re.search(r'\b(dear customer|dear user|valued member|dear account holder)\b', t):
        boost += 0.10
        reasons.append("Generic impersonation greeting")

    # — Job scam cluster
    job_keywords = [
        "earn", "income", "work from home", "part time",
        "limited slots", "no experience", "per day",
        "weekly pay", "guaranteed income", "job offer"
    ]
    matches = sum(1 for kw in job_keywords if kw in t)
    if matches >= 3:
        boost += 0.40
        reasons.append("Strong job-scam pattern detected")
    elif matches == 2:
        boost += 0.20
        reasons.append("Possible job scam indicators")

    return min(boost, 0.50), reasons


def predict_email(text, threshold=0.45):
    ml_score       = get_ml_score(text)
    boost, reasons = rule_boost(text)

    final_score = min(ml_score + boost, 1.0)

    if final_score >= threshold:
        label = "Scam"
    elif final_score >= 0.30:
        label = "Suspicious"
    else:
        label = "Genuine"

    return label, round(final_score * 100, 2), reasons