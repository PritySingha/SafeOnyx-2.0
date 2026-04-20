import streamlit as st
from PIL import Image
from navbar import show_navbar
from footer import show_footer
from utils.screenshot_utils import predict_screenshot

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Screenshot Detection", layout="wide")

# ---------------------------------
# LOAD CSS
# ---------------------------------
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------
# NAVBAR
# ---------------------------------
show_navbar("Screenshot")

# ---------------------------------
# PAGE HEADER
# ---------------------------------
st.markdown("""
<div class="section-label">Screenshot Analysis</div>

<h2 class="page-header">
Detect scams from screenshots
</h2>

<p class="page-sub">
Upload a screenshot of messages, emails, or chats. 
AI will extract text and detect scam patterns instantly.
</p>
""", unsafe_allow_html=True)

# ---------------------------------
# FILE UPLOAD
# ---------------------------------
uploaded_file = st.file_uploader(
    "Upload Screenshot",
    type=["png", "jpg", "jpeg"]
)

# ---------------------------------
# PROCESS IMAGE
# ---------------------------------
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Screenshot", use_container_width=True)

    if st.button("Analyze Screenshot"):

        with st.spinner("Extracting text and analyzing..."):
            label, score, extracted_text, reasons = predict_screenshot(image)

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
        # EXTRACTED TEXT
        # ---------------------------------
        st.markdown("### 📝 Extracted Text")
        st.text_area("", extracted_text, height=150)

        # ---------------------------------
        # REASONS
        # ---------------------------------
        if reasons:
            st.markdown("### 🔍 Why this result?")
            for r in reasons:
                st.write(f"- {r}")

# ---------------------------------
# SAMPLE TEST INFO
# ---------------------------------
st.markdown("""
### 🧪 Tips for testing
- Upload WhatsApp scam messages
- Try OTP / bank fraud screenshots
- Try job scam or lottery screenshots
""")

# ---------------------------------
# FOOTER
# ---------------------------------
show_footer()

