import streamlit as st
from navbar import show_navbar
from footer import show_footer
from utils.email_utils import predict_email

st.set_page_config(page_title="Email Detection", page_icon="assets/logo.png", layout="wide")

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

show_navbar("Email")

st.markdown("""
<div class="section-label">Email Analysis</div>
<h2 class="page-header">Detect phishing emails instantly</h2>
<p class="page-sub">Paste the email subject and body below to check if it's a scam.</p>
""", unsafe_allow_html=True)

# Two separate inputs — merged before prediction
email_subject = st.text_input("Email Subject (optional)")
email_body    = st.text_area("Email Body", height=200)

if st.button("Analyze Email"):
    combined = (email_subject + " " + email_body).strip()
    if not combined:
        st.warning("Please enter email content to analyze.")
    else:
        with st.spinner("Analyzing email..."):
            label, score, reasons = predict_email(combined)

        if label == "Scam":
            st.markdown(
                f"<div class='result-box result-scam'>⚠️ Scam Detected ({score}% risk)</div>",
                unsafe_allow_html=True)
        elif label == "Suspicious":
            st.markdown(
                f"<div class='result-box result-warning'>⚠️ Suspicious ({score}% risk)</div>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div class='result-box result-safe'>✅ Genuine ({score}% safe)</div>",
                unsafe_allow_html=True)

        st.progress(min(score / 100, 1.0))

        if reasons:
            st.markdown("### 🔍 Why this result?")
            for r in reasons:
                st.write(f"- {r}")

show_footer()