import joblib
import re
import os
import nltk     # NLTK stopwords

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

# Load model
with open("models/sms_model.joblib", "rb") as f:
    model = joblib.load(f)

with open("models/sms_vectorizer.joblib", "rb") as f:
    vectorizer = joblib.load(f)


def clean_text(text):
    text = text.lower()
    # Keep currency symbols as words before stripping
    text = text.replace("₹", " rupees ").replace("$", " dollar ")
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stop_words and len(w) > 1]
    return " ".join(words)


def get_ml_score(text):
    cleaned    = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    prob       = model.predict_proba(vectorized)[0][1]
    return float(prob)


def rule_boost(text):
    t       = text.lower()
    boost   = 0.0
    reasons = []

    # — Prize / winning scams
    if re.search(r'\b(win|won|winner|prize|lucky draw)\b', t):
        boost += 0.15
        reasons.append("Prize or winning language detected")

    # — Urgency
    if re.search(r'\b(urgent|immediately|expire|last chance|act now)\b', t):
        boost += 0.10
        reasons.append("Urgency language detected")

    # — Action trigger
    if re.search(r'\b(click|tap|open|visit)\b', t) and \
       re.search(r'(http|www|link|\.com|\.in)', t):
        boost += 0.12
        reasons.append("Suspicious link with call-to-action")

    # — Verification / credential phishing
    if re.search(r'\b(verify|otp|password|pin|credentials)\b', t):
        boost += 0.12
        reasons.append("Credential or OTP-related request")

    # — Money / financial bait
    if re.search(r'(₹|\$|rupees|dollar|rs\.?\s*\d+|\d+\s*rs)', t):
        boost += 0.08
        reasons.append("Mentions money or financial reward")

    # — Links
    if re.search(r'https?://|www\.', t):
        boost += 0.08
        reasons.append("Contains a URL")

    # — Job scam cluster (needs multiple signals)
    job_keywords = [
        "earn", "daily", "income", "work from home",
        "job offer", "part time", "limited slots",
        "no experience", "start earning", "per day",
        "weekly pay", "guaranteed income"
    ]
    matches = sum(1 for kw in job_keywords if kw in t)
    if matches >= 3:
        boost += 0.40
        reasons.append("Strong job-scam pattern detected")
    elif matches == 2:
        boost += 0.20
        reasons.append("Possible job scam indicators")

    # Hard cap so rules alone can't reach 1.0
    return min(boost, 0.50), reasons


def predict_sms(text, threshold=0.45):
    ml_score          = get_ml_score(text)          
    boost, reasons    = rule_boost(text)            

    final_score = min(ml_score * 0.70 + boost * 0.30 + boost, 1.0)

    if final_score >= threshold:
        label = "Scam"
    elif final_score >= 0.30:
        label = "Suspicious"
    else:
        label = "Genuine"

    return label, round(final_score * 100, 2), reasons