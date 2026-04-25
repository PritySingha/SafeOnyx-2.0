import streamlit as st
from navbar import show_navbar
from footer import show_footer
from utils.sms_utils import predict_sms

st.set_page_config(page_title="SMS Detection",page_icon="assets/logo.png", layout="wide")

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

show_navbar("SMS")


st.markdown("""
<div class="section-label">SMS Analysis</div>

<h2 class="page-header">
Detect scam messages instantly
</h2>

<p class="page-sub">
Paste any SMS or message to check whether it's genuine or a scam using AI.
</p>
""", unsafe_allow_html=True)


sms_text = st.text_area("Enter SMS text here", height=150)


if st.button("Analyze SMS"):

    if sms_text.strip() == "":
        st.warning("Please enter a message to analyze.")
    else:
        with st.spinner("Analyzing message..."):
            label, score, reasons = predict_sms(sms_text)

        if label == "Scam":
            st.markdown(
                f"<div class='result-box result-scam'>⚠️ Scam Detected ({score}% risk)</div>",
                unsafe_allow_html=True
            )

        elif label == "Suspicious":
            st.markdown(
                f"<div class='result-box result-warning'>⚠️ Suspicious ({score}% risk)</div>",
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"<div class='result-box result-safe'>✅ Genuine ({score}% safe)</div>",
                unsafe_allow_html=True
            )

        st.progress(min(score / 100, 1.0))

        if reasons:
            st.markdown("### 🔍 Why this result?")
            for r in reasons:
                st.write(f"- {r}")

show_footer()

