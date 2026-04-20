import streamlit as st
from navbar import show_navbar
from footer import show_footer
from utils.url_utils import predict_url

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="URL Detection", page_icon="assets/logo.png",layout="wide")

# ---------------------------------
# LOAD CSS
# ---------------------------------
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------
# NAVBAR
# ---------------------------------
show_navbar("URL")

# ---------------------------------
# PAGE HEADER
# ---------------------------------
st.markdown("""
<div class="section-label">URL Analysis</div>

<h2 class="page-header">
Check if a website is safe or a scam
</h2>

<p class="page-sub">
Enter any URL to detect phishing links, fake domains, or malicious websites.
</p>
""", unsafe_allow_html=True)

# ---------------------------------
# INPUT SECTION
# ---------------------------------
url_input = st.text_input("Enter URL (e.g., https://example.com)")

# ---------------------------------
# ANALYZE BUTTON
# ---------------------------------
if st.button("Analyze URL"):

    if url_input.strip() == "":
        st.warning("Please enter a URL to analyze.")
    else:
        with st.spinner("Analyzing URL..."):
            label, score, reasons = predict_url(url_input)

        # ---------------------------------
        # RESULT DISPLAY
        # ---------------------------------
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

        # ---------------------------------
        # PROGRESS BAR
        # ---------------------------------
        st.progress(min(score / 100, 1.0))

        # ---------------------------------
        # REASONS
        # ---------------------------------
        if reasons:
            st.markdown("### 🔍 Why this result?")
            for r in reasons:
                st.write(f"- {r}")

# ---------------------------------
# SAMPLE TEST BUTTONS (VERY USEFUL)
# ---------------------------------
st.markdown("### 🧪 Try Sample URLs")

col1, col2 = st.columns(2)

with col1:
    if st.button("Test Genuine URL"):
        test_url = "https://google.com"
        label, score, reasons = predict_url(test_url)
        st.info(f"{test_url} → {label} ({score}%)")

with col2:
    if st.button("Test Scam URL"):
        test_url = "http://free-gift-win-now.com"
        label, score, reasons = predict_url(test_url)
        st.info(f"{test_url} → {label} ({score}%)")

# ---------------------------------
# FOOTER
# ---------------------------------
show_footer()
