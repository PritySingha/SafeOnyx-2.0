# 🛡️ SafeOnyx — AI-Powered Scam Detection Platform

> A production-ready, multi-modal fraud detection system that identifies scams across **SMS, Emails, URLs, and Screenshots** using Machine Learning and OCR.

---

## 🚀 Overview

SafeOnyx is a **full-stack AI application** designed to detect real-world scams in multiple formats.
It combines **NLP models, feature-engineered classifiers, and OCR pipelines** into a unified interface for real-time fraud detection.

This project simulates a **practical cybersecurity product**, not just a model — focusing on **accuracy, explainability, and usability**.

---

## ✨ Key Highlights

* 🔍 Detects scams across **4 input types**:

  * SMS
  * Email
  * URLs
  * Screenshots (via OCR)

* ⚡ **Real-time predictions** with confidence scores

* 🧠 **Explainable AI** — shows *why* something is flagged

* 🎯 High-performing ML models (up to **98% accuracy**)

* 🖼️ OCR-powered detection for image-based scams

* 🎨 Modern, responsive UI (Streamlit-based product design)

---

## 🧠 System Architecture

```
User Input → Preprocessing → Model Inference → Rule Boost → Explanation Engine → UI Output
```

### Components:

* **Text Models (SMS/Email):**

  * TF-IDF Vectorization
  * Logistic Regression classifier

* **URL Model:**

  * Feature Engineering (30+ security signals)
  * XGBoost classifier

* **Screenshot Model:**

  * EasyOCR for text extraction
  * NLP pipeline reuse (SMS model)

* **Post-processing Layer:**

  * Rule-based boost (keywords like "OTP", "bank", "urgent")
  * Confidence calibration

---

## 🛠️ Tech Stack

| Layer      | Technologies          |
| ---------- | --------------------- |
| Frontend   | Streamlit             |
| Backend    | Python                |
| ML Models  | Scikit-learn, XGBoost |
| NLP        | TF-IDF, NLTK          |
| OCR        | EasyOCR, OpenCV       |
| Deployment | Render                |

---

## 📊 Model Performance

| Module               | Accuracy      | Precision | Recall |
| -------------------- | ------------- | --------- | ------ |
| SMS Detection        | ~98%          | 0.99      | 0.92   |
| Email Detection      | ~97%          | High      | High   |
| URL Detection        | ~96%          | High      | High   |
| Screenshot Detection | OCR dependent |           |        |

> Optimized using feature tuning, threshold calibration, and hybrid rule-based boosting.

---

## 🧩 Core Features

### 📩 SMS & Email Detection

* Cleans and vectorizes text using TF-IDF
* Classifies using Logistic Regression
* Applies contextual boosting for scam patterns

---

### 🌐 URL Detection

  * URL length
  * Special characters
  * SSL status
  * Domain age
* Uses **XGBoost** for classification

---

### 🖼️ Screenshot Detection

* Extracts text using EasyOCR
* Cleans noisy OCR output
* Runs through NLP model
* Applies additional fraud heuristics

---

### 💡 Explainability Engine

* Highlights key reasons:

  * "Contains urgency words"
  * "Mentions financial info"
  * "Suspicious URL patterns"

---

## 📁 Project Structure

```
SafeOnyx/
│
├── app.py                  # Main application
├── pages/                 # Multi-page UI
│   ├── sms.py
│   ├── email.py
│   ├── url.py
│   └── screenshot.py
│
├── models/                # Trained models
├── utils/                 # Core logic modules
├── assets/                # UI styling
├── requirements.txt
└── runtime.txt
```

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/your-username/SafeOnyx.git
cd SafeOnyx

conda create -n safeonyx python=3.10
conda activate safeonyx

pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Deployment

Deployed using Render with:

* Python 3.10 runtime
* Streamlit server configuration
* Optimized dependency handling for ML + OCR

---

## ⚠️ Challenges & Solutions

| Challenge               | Solution                                  |
| ----------------------- | ----------------------------------------- |
| OCR noise               | Text cleaning + normalization             |
| Model false negatives   | Rule-based boosting                       |
| Deployment failures     | Python version control + dependency fixes |
| Multi-model integration | Modular utils architecture                |

---

## 📌 Why This Project Matters

This project demonstrates:

* End-to-end ML system design
* Real-world problem solving (fraud detection)
* Model + product integration
* Deployment and scalability awareness

---

## ⭐ Support

If you found this useful:

* ⭐ Star the repository
* 🍴 Fork it
* 🤝 Contribute

---
