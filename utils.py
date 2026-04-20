# utils.py
import re
import pickle
import numpy as np
import nltk
import easyocr
from urllib.parse import urlparse

nltk.download('stopwords')
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))

# Load models (adjust paths if needed)
with open('models/sms_model.pkl', 'rb') as f:
    sms_model = pickle.load(f)
with open('models/sms_vectorizer.pkl', 'rb') as f:
    sms_vectorizer = pickle.load(f)

with open('models/email_model.pkl', 'rb') as f:
    email_model = pickle.load(f)
with open('models/email_vectorizer.pkl', 'rb') as f:
    email_vectorizer = pickle.load(f)

with open('models/url_model.pkl', 'rb') as f:
    url_model = pickle.load(f)

try:
    with open('models/url_feature_columns.pkl', 'rb') as f:
        URL_FEATURE_NAMES = pickle.load(f)
except:
    URL_FEATURE_NAMES = [f'feat_{i}' for i in range(30)]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join([word for word in text.split() if word not in STOP_WORDS])
    return text

def predict_sms(text):
    cleaned = clean_text(text)
    vec = sms_vectorizer.transform([cleaned])
    prob = sms_model.predict_proba(vec)[0][1]
    return prob * 100

def predict_email(text):
    cleaned = clean_text(text)
    vec = email_vectorizer.transform([cleaned])
    prob = email_model.predict_proba(vec)[0][1]
    return prob * 100

def extract_url_features(url):
    features = {name: 0 for name in URL_FEATURE_NAMES}
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
    except:
        domain = ''
    # Implement all 30 features (simplified)
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    features['having_IPhaving_IP_Address'] = 1 if re.search(ip_pattern, url) else 0
    features['URLURL_Length'] = len(url)
    shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 'ow.ly', 'is.gd']
    features['Shortining_Service'] = 1 if any(s in url for s in shorteners) else 0
    features['having_At_Symbol'] = 1 if '@' in url else 0
    parts = url.split('://')
    if len(parts) > 1:
        rest = parts[1]
        features['double_slash_redirecting'] = 1 if rest.count('//') > 0 else 0
    else:
        features['double_slash_redirecting'] = 0
    features['Prefix_Suffix'] = 1 if '-' in domain else 0
    features['having_Sub_Domain'] = 1 if domain.count('.') > 1 else 0
    features['SSLfinal_State'] = 1 if url.startswith('https') else -1
    port_match = re.search(r':(\d+)', domain)
    if port_match:
        port = int(port_match.group(1))
        features['port'] = 1 if port not in [80,443] else 0
    else:
        features['port'] = 0
    features['HTTPS_token'] = 1 if 'https' in domain else 0
    # Remaining default 0
    ordered = [features.get(name, 0) for name in URL_FEATURE_NAMES]
    return np.array(ordered).reshape(1, -1)

def predict_url(url):
    features = extract_url_features(url)
    prob = url_model.predict_proba(features)[0][1]
    return prob * 100

# OCR
reader = easyocr.Reader(['en'])
def extract_text_from_image(image_path):
    result = reader.readtext(image_path, detail=0)
    return ' '.join(result)

def predict_screenshot(image_path):
    raw_text = extract_text_from_image(image_path)
    risk = predict_sms(raw_text)
    return raw_text, risk