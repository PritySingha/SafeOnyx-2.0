import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import numpy as np
import cv2
from utils.sms_utils import predict_sms

_reader = None

def get_reader():
    global _reader
    if _reader is None:
        import easyocr
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader


def preprocess_for_ocr(image):
    img     = np.array(image.convert("RGB"))
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray    = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # --- upscale small images for better OCR ---
    h, w = gray.shape
    if w < 1000:
        scale = 1000 / w
        gray  = cv2.resize(gray, None, fx=scale, fy=scale,
                           interpolation=cv2.INTER_CUBIC)

    mean_brightness = gray.mean()

    if mean_brightness > 180:
        # Light background (e.g. SMS bubble, white email)
        # Simple Otsu — clean separation of dark text from light bg
        blur            = cv2.GaussianBlur(gray, (3, 3), 0)
        _, processed    = cv2.threshold(blur, 0, 255,
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    elif mean_brightness > 80:
        # Mixed / medium contrast (e.g. chat apps with coloured bubbles)
        # CLAHE normalises local contrast, then Otsu binarises
        clahe           = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced        = clahe.apply(gray)
        blur            = cv2.GaussianBlur(enhanced, (3, 3), 0)
        _, processed    = cv2.threshold(blur, 0, 255,
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    else:
        # Dark background — invert so text is dark-on-light, then Otsu
        inverted        = cv2.bitwise_not(gray)
        blur            = cv2.GaussianBlur(inverted, (3, 3), 0)
        _, processed    = cv2.threshold(blur, 0, 255,
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)


def extract_text_from_image(image):
    """PIL Image → raw OCR string. Returns '' on failure."""
    try:
        processed = preprocess_for_ocr(image)
        result    = get_reader().readtext(processed, detail=0, paragraph=True)
        return " ".join(result).strip()
    except Exception:
        return ""


def clean_ocr_text(text):
    text = text.lower()
    text = text.replace("\n", " ").replace("\r", " ")
    text = text.replace("₹", " rupees ")
    text = text.replace("$", " dollar ")
    return " ".join(text.split())


def extra_boost_with_reasons(text):
    """
    Screenshot-specific rule signals on top of the SMS model.
    Covers phishing patterns the SMS model may under-weight.
    """
    rules = [
        # (regex_pattern, boost, reason)
        (r'\blogin\b',                          0.12, "Contains 'login' — phishing trigger"),
        (r'\bverify\b',                         0.10, "Requests verification"),
        (r'\baccount\b',                        0.06, "Account-related message"),
        (r'\blogged out\b|\blocked\b',          0.12, "Account lock threat"),
        (r'\b24 hours?\b|\b\d+ hours?\b',       0.10, "Time-pressure urgency"),
        (r'bit\.ly|tinyurl|goo\.gl|t\.co',      0.20, "URL shortener — destination hidden"),
        (r'https?://|www\.',                    0.08, "Contains a link"),
        (r'\burgent\b|\bimmediately\b',         0.10, "Urgency language"),
        (r'\botp\b|\bpassword\b|\bpin\b',       0.12, "Credential request"),
        (r'\bbank\b',                           0.08, "Bank-related message"),
        (r'\bwin\b|\bprize\b|\blottery\b',      0.15, "Prize / lottery scam"),
        (r'\bfree\b',                           0.06, "Free offer"),
        (r'rupees|dollar|₹|\$',                 0.06, "Money mentioned"),
        (r'\bsuspended\b|\bsuspend\b',          0.12, "Account suspension threat"),
        (r'\bclick\b.*\blink\b|\blink\b.*\bclick\b', 0.10, "Click-link call to action"),
    ]

    import re
    boost   = 0.0
    reasons = []

    for pattern, value, reason in rules:
        if re.search(pattern, text):
            boost += value
            reasons.append(reason)

    # Hard cap — rules alone should not dominate over the ML score
    return min(boost, 0.50), reasons


def predict_screenshot(image):
    raw_text     = extract_text_from_image(image)
    cleaned_text = clean_ocr_text(raw_text)

    if len(cleaned_text.strip()) < 10:
        return "Unable to Detect", 0, raw_text or "", \
               ["No readable text found — try a clearer screenshot"]

 
    _label, pct_score, sms_reasons = predict_sms(cleaned_text)

    # Normalise to 0-1 for internal maths
    ml_01 = pct_score / 100.0

    extra_boost, extra_reasons = extra_boost_with_reasons(cleaned_text)

    final_01 = min(ml_01 * 0.65 + extra_boost * 0.35 + extra_boost, 1.0)


    # Three-tier labels
    if final_01 >= 0.60:
        final_label = "Scam"
    elif final_01 >= 0.40:
        final_label = "Suspicious"
    else:
        final_label = "Genuine"

    all_reasons = sms_reasons + extra_reasons

    return final_label, round(final_01 * 100, 2), cleaned_text, all_reasons