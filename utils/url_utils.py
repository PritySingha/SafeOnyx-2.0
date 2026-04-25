import pickle
import re
import pandas as pd
import tldextract

with open("models/url_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/url_columns.pkl", "rb") as f:
    columns = pickle.load(f)

# Suspicious TLDs
SUSPICIOUS_TLDS = {".ru", ".tk", ".ml", ".xyz", ".top", ".gq", ".cf", ".pw", ".cc"}

# Known-safe domains (skip heavy rule boosting for these)
KNOWN_SAFE_DOMAINS = {
    "google", "youtube", "facebook", "twitter", "instagram",
    "linkedin", "microsoft", "apple", "amazon", "wikipedia",
    "github", "stackoverflow", "reddit", "netflix", "spotify"
}


def has_ip(url):
    return 1 if re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', url) else -1


def extract_features(url):
    extracted = tldextract.extract(url)
    domain    = extracted.domain
    subdomain = extracted.subdomain
    suffix    = "." + extracted.suffix if extracted.suffix else ""

    features = {}

    features['having_IPhaving_IP_Address']  = has_ip(url)
    features['URLURL_Length']               = 1 if len(url) < 75 else -1
    features['Shortining_Service']          = -1 if any(
        x in url for x in ["bit.ly", "tinyurl", "goo.gl", "t.co", "ow.ly"]
    ) else 1
    features['having_At_Symbol']            = -1 if "@" in url else 1
    features['double_slash_redirecting']    = -1 if url.count("//") > 1 else 1
    features['Prefix_Suffix']              = -1 if "-" in domain else 1
    features['having_Sub_Domain']          = -1 if subdomain.count('.') >= 1 else 1
    features['SSLfinal_State']             = 1 if url.startswith("https") else -1
    features['HTTPS_token']               = -1 if "https" in domain else 1

    # unavailable — set neutral (1)
    neutral_features = [
        'Domain_registeration_length', 'age_of_domain', 'DNSRecord',
        'web_traffic', 'Page_Rank', 'Google_Index', 'Favicon', 'port',
        'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH',
        'Submitting_to_email', 'Abnormal_URL', 'Redirect',
        'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe',
        'Links_pointing_to_page', 'Statistical_report'
    ]
    for nf in neutral_features:
        features[nf] = 1

    return features


def prepare_input(url):
    features = extract_features(url)
    df = pd.DataFrame([features])
    for col in columns:
        if col not in df.columns:
            df[col] = 0
    return df[columns]


def get_ml_score(url):
    df   = prepare_input(url)
    prob = model.predict_proba(df)[0]
    # index 1 = phishing/scam class
    return float(prob[1])


def rule_boost(url, domain):
    t       = url.lower()
    boost   = 0.0
    reasons = []

    # — Suspicious keywords in path/query
    phishing_kws = ["login", "verify", "secure", "update", "account",
                    "bank", "paypal", "signin", "confirm", "password"]
    hits = [kw for kw in phishing_kws if kw in t]
    if hits:
        boost += min(len(hits) * 0.07, 0.25)
        reasons.append(f"Phishing keywords in URL: {', '.join(hits)}")

    # — Free / gift / scam bait
    if re.search(r'\b(free|gift|win|prize|lucky|reward)\b', t):
        boost += 0.20
        reasons.append("Free/gift/prize scam pattern")

    # — Suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if t.endswith(tld) or f"{tld}/" in t:
            boost += 0.20
            reasons.append(f"Suspicious domain extension ({tld})")
            break

    # — Structural issues
    if url.count("-") > 3:
        boost += 0.10
        reasons.append("Excessive hyphens in URL")

    if url.count(".") > 4:
        boost += 0.10
        reasons.append("Excessive subdomains")

    if "@" in url:
        boost += 0.20
        reasons.append("Contains '@' — redirects to different host")

    if has_ip(url) == 1:
        boost += 0.20
        reasons.append("URL uses raw IP address instead of domain")

    # — Shortener
    if any(x in t for x in ["bit.ly", "tinyurl", "goo.gl", "t.co"]):
        boost += 0.10
        reasons.append("URL shortener detected — destination unknown")

    return min(boost, 0.60), reasons


def predict_url(url, threshold=0.45):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    extracted = tldextract.extract(url)
    domain    = extracted.domain.lower()

    # Fast-pass for well-known safe domains
    if domain in KNOWN_SAFE_DOMAINS:
        return "Genuine", 5.0, ["Recognised safe domain"]

    ml_score       = get_ml_score(url)
    boost, reasons = rule_boost(url, domain)

    # ML is primary; rules add evidence
    final_score = min(ml_score * 0.60 + boost * 0.40, 1.0)

    # HTTPS gives a small safety discount
    if url.startswith("https://") and boost < 0.20:
        final_score = max(final_score - 0.05, 0.0)

    if final_score >= threshold:
        label = "Scam"
    elif final_score >= 0.30:
        label = "Suspicious"
    else:
        label = "Genuine"

    if not reasons:
        reasons = ["No suspicious patterns detected"]

    return label, round(final_score * 100, 2), reasons