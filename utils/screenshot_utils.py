import pytesseract
from PIL import Image
import numpy as np
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

# import your existing model
from utils.sms_utils import predict_sms


# 🔹 STEP 1: OCR TEXT EXTRACTION
def extract_text_from_image(image):
    try:
        # Convert PIL → OpenCV
        img = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 🔥 Improve OCR accuracy
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        thresh = cv2.adaptiveThreshold(
            blur,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        # Extract text
        text = pytesseract.image_to_string(thresh)

        return text

    except Exception as e:
        return ""


# 🔹 STEP 2: CLEAN OCR TEXT (VERY IMPORTANT)
def clean_ocr_text(text):
    text = text.lower()

    # Remove newlines
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")

    # Fix common OCR mistakes
    text = text.replace("0", "o")
    text = text.replace("1", "l")
    text = text.replace("₹", " rupees ")
    text = text.replace("$", " dollar ")

    # Remove extra spaces
    text = " ".join(text.split())

    return text


# 🔹 STEP 3: EXTRA BOOST (FOR OCR CONTEXT)
def extra_boost_with_reasons(text):
    text = text.lower()
    boost = 0
    reasons = []

    if "otp" in text:
        boost += 0.10
        reasons.append("Mentions OTP (sensitive information)")

    if "bank" in text:
        boost += 0.10
        reasons.append("References bank/account")

    if "account" in text:
        boost += 0.05
        reasons.append("Mentions account details")

    return boost, reasons


# 🔹 STEP 4: FINAL PREDICTION FUNCTION
def predict_screenshot(image):
    # Extract text
    raw_text = extract_text_from_image(image)

    # Clean text
    cleaned_text = clean_ocr_text(raw_text)

    # ⚠️ If OCR fails
    if len(cleaned_text.strip()) < 10:
        return raw_text, "Unable to Detect", 0

    # Get prediction from SMS model
    label, score, reasons = predict_sms(cleaned_text)
    score = score / 100

    # Apply extra boost
    extra, extra_reasons = extra_boost_with_reasons(cleaned_text)

    final_score = min(score + extra , 1.0)

    all_reasons = reasons + extra_reasons

    # Recalculate label if needed
    if final_score >= 0.4:
        final_label = "Scam"
    else:
        final_label = "Genuine"

    return cleaned_text, final_label, round(final_score * 100, 2), all_reasons