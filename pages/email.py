import streamlit as st
from navbar import show_navbar
from footer import show_footer
from utils.email_utils import predict_email

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Email Detection", layout="wide")

# ---------------------------------
# LOAD CSS
# ---------------------------------
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------
# NAVBAR
# ---------------------------------
show_navbar("Email")

# ---------------------------------
# PAGE HEADER
# ---------------------------------
st.markdown("""
<div class="section-label">Email Analysis</div>

<h2 class="page-header">
Detect phishing emails instantly
</h2>

<p class="page-sub">
Paste any email content to check whether it's genuine or a scam using AI.
</p>
""", unsafe_allow_html=True)

# ---------------------------------
# INPUT SECTION
# ---------------------------------
email_text = st.text_area("Enter Email content here", height=200)

# ---------------------------------
# ANALYZE BUTTON
# ---------------------------------
if st.button("Analyze Email"):

    if email_text.strip() == "":
        st.warning("Please enter email content to analyze.")
    else:
        with st.spinner("Analyzing email..."):
            label, score, reasons = predict_email(email_text)

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
# FOOTER
# ---------------------------------
show_footer()
