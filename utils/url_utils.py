import pickle
import pandas as pd
import re
import tldextract

# Load model
with open("models/url_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/url_columns.pkl", "rb") as f:
    columns = pickle.load(f)


# 🔹 Helper: check IP address
def has_ip(url):
    return 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else -1


# 🔹 Feature extraction
def extract_features(url):
    features = {}

    extracted = tldextract.extract(url)
    domain = extracted.domain
    subdomain = extracted.subdomain

    # ✅ BASIC FEATURES
    features['having_IPhaving_IP_Address'] = has_ip(url)
    features['URLURL_Length'] = 1 if len(url) < 54 else 0
    features['Shortining_Service'] = 1 if any(x in url for x in ["bit.ly", "tinyurl", "goo.gl"]) else -1
    features['having_At_Symbol'] = 1 if "@" in url else -1
    features['double_slash_redirecting'] = 1 if url.count("//") > 1 else -1
    features['Prefix_Suffix'] = 1 if "-" in domain else -1
    features['having_Sub_Domain'] = 1 if subdomain.count('.') > 1 else -1

    # 🔐 HTTPS
    features['SSLfinal_State'] = 1 if url.startswith("https") else -1
    features['HTTPS_token'] = 1 if "https" in domain else -1

    # ⚠️ APPROXIMATED FEATURES
    features['Domain_registeration_length'] = 1
    features['age_of_domain'] = 1
    features['DNSRecord'] = 1
    features['web_traffic'] = 1
    features['Page_Rank'] = 1
    features['Google_Index'] = 1

    # ❌ UNAVAILABLE → neutral
    neutral = 1
    features['Favicon'] = neutral
    features['port'] = neutral
    features['Request_URL'] = neutral
    features['URL_of_Anchor'] = neutral
    features['Links_in_tags'] = neutral
    features['SFH'] = neutral
    features['Submitting_to_email'] = neutral
    features['Abnormal_URL'] = neutral
    features['Redirect'] = neutral
    features['on_mouseover'] = neutral
    features['RightClick'] = neutral
    features['popUpWidnow'] = neutral
    features['Iframe'] = neutral
    features['Links_pointing_to_page'] = neutral
    features['Statistical_report'] = neutral

    return features


# 🔹 Prepare dataframe
def prepare_input(url):
    features = extract_features(url)
    df = pd.DataFrame([features])

    for col in columns:
        if col not in df:
            df[col] = 0

    df = df[columns]
    return df


# 🔹 ML score
def get_ml_score(url):
    df = prepare_input(url)
    prob = model.predict_proba(df)[0][1]
    return prob


# 🔥 RULE BOOST (IMPORTANT)
def rule_boost(url):
    url = url.lower()
    boost = 0
    reasons = []

    # 🔴 Suspicious keywords (STRONG SIGNAL)
    keywords = ["login", "verify", "secure", "update", "account", "bank", "paypal"]

    for word in keywords:
        if word in url:
            boost += 0.08
            reasons.append(f"Contains '{word}' keyword")

    # 🔴 Free/gift scams
    if "free" in url or "gift" in url or "win" in url:
        boost += 0.20
        reasons.append("Free/gift scam pattern")

    # 🔴 Suspicious TLD
    if any(tld in url for tld in [".ru", ".tk", ".ml", ".xyz"]):
        boost += 0.20
        reasons.append("Suspicious domain extension")

    # 🔴 Structure issues
    if url.count("-") > 2:
        boost += 0.10
        reasons.append("Too many hyphens")

    if url.count(".") > 3:
        boost += 0.10
        reasons.append("Too many subdomains")

    if "@" in url:
        boost += 0.15
        reasons.append("Contains '@' symbol")

    return boost, reasons


# 🔹 Final prediction
def predict_url(url, threshold=0.4):
    ml_score = get_ml_score(url)
    boost, reasons = rule_boost(url)

    # ✅ CASE 1: No suspicious signals → TRUST URL
    if boost == 0:
        return "Genuine", 90.0, ["No suspicious patterns detected"]

    # ✅ CASE 2: Suspicious → use ML + rules
    final_score = (0.3 * ml_score) + (0.7 * boost)

    # Safe bonus (light)
    if url.startswith("https"):
        final_score -= 0.05

    final_score = max(0, min(final_score, 1))

    if final_score >= threshold:
        label = "Scam"
    else:
        label = "Genuine"

    return label, round(final_score * 100, 2), reasons
    ml_score = get_ml_score(url)       # 0–1
    boost, reasons = rule_boost(url)   # 0–1

    print("URL:", url)
    print("ML SCORE:", ml_score)
    print("BOOST:", boost)
    # 🔥 Balanced scoring (ML slightly stronger)
    final_score = (0.6 * ml_score) + (0.4 * boost)

    # 🔥 APPLY SAFE BONUS ONLY FOR CLEAN URLs
    safe_bonus = 0

    if (
        url.startswith("https") and
        url.count("-") == 0 and
        url.count(".") <= 2 and
        "@" not in url
    ):
        safe_bonus = 0.10

    final_score = max(0, final_score - safe_bonus)

    # 🔥 FINAL DECISION
    if final_score >= threshold:
        label = "Scam"
    else:
        label = "Genuine"

    return label, round(final_score * 100, 2), reasons

    










    ml_score = get_ml_score(url)
    boost, reasons = rule_boost(url)

    # Balanced scoring
    final_score = (0.5 * ml_score) + (0.5 * boost)

    # ✅ Safe bonus
    safe_bonus = 0

    if url.startswith("https"):
        safe_bonus += 0.05

    if url.count("-") == 0:
        safe_bonus += 0.05

    if url.count(".") <= 2:
        safe_bonus += 0.05

    final_score = max(0, final_score - safe_bonus)

    if final_score >= threshold:
        label = "Scam"
    else:
        label = "Genuine"

    return label, round(final_score * 100, 2), reasons