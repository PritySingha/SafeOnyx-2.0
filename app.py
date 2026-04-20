import streamlit as st
from navbar import show_navbar
from footer import show_footer

st.set_page_config(
    page_title="SafeOnyx",
    page_icon="assets/logo.png",
    layout="wide"
)

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

show_navbar("Home")

# HERO TOP BADGE
st.markdown("""
<div class="eyebrow">
    <div class="eyebrow-dot"></div>
    <span>AI Powered Scam Detection</span>
</div>
""", unsafe_allow_html=True)

# HERO SECTION
st.markdown("""
<div class="hero-layout">
    <div>
        <h1>
            Stay safe online.<br>
            <em>Detect scams</em><br>
            instantly.
        </h1>
        <p class="hero-sub">
            SafeOnyx helps you identify online scams in real time —
            from SMS, emails, URLs, and screenshots using AI-powered models.
        </p>
        <div class="hero-actions">
            <a href="/sms" target="_self" class="btn-main">Detect SMS →</a>
            <a href="/screenshot" target="_self" class="btn-light">Detect Screenshot →</a>
        </div>
    </div>
    <div class="hero-card">
        <div class="hero-card-title">Recent Checks</div>
        <div class="mini-stat">
            <div>
                <div class="mini-stat-label">SMS</div>
                <div class="mini-stat-type">"Win ₹5000 now!"</div>
            </div>
            <span class="risk-badge risk-high">Scam</span>
        </div>
        <div class="mini-stat">
            <div>
                <div class="mini-stat-label">URL</div>
                <div class="mini-stat-type">paypal-login-secure.ru</div>
            </div>
            <span class="risk-badge risk-high">Scam</span>
        </div>
        <div class="mini-stat">
            <div>
                <div class="mini-stat-label">Email</div>
                <div class="mini-stat-type">Bank verification request</div>
            </div>
            <span class="risk-badge risk-med">Suspicious</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# TRUST STRIP
st.markdown("""
<div class="trust-strip">
    <div class="trust-item">Real-time Detection</div>
    <div class="trust-item">Multi-Model AI</div>
    <div class="trust-item">Explainable Results</div>
    <div class="trust-item">Privacy First</div>
</div>
""", unsafe_allow_html=True)

# SECTION DIVIDER
st.markdown("""
<div style="border-top:1px solid rgba(255,255,255,0.06);margin:68px 0 0;padding-top:48px;"></div>
""", unsafe_allow_html=True)

# FEATURES SECTION
st.markdown("""
<div class="section-label">Capabilities</div>
<h2>What SafeOnyx offers</h2>
<p class="section-desc">
    AI-powered tools to detect scams across multiple platforms instantly and accurately.
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="grid-3">
    <div class="card-clean featured">
        <h3>Screenshot Detection</h3>
        <p>
            Upload screenshots of chats, emails, or messages.
            AI extracts text and detects scam patterns instantly.
        </p>
        <div class="response-box">
            <div class="response-box-label">Accuracy</div>
            <div class="response-big">~95<span class="response-unit">%</span></div>
        </div>
    </div>
    <div class="card-clean">
        <h3>SMS Detection</h3>
        <p>Detect fraud messages like lottery scams, OTP fraud, and fake job offers.</p>
    </div>
    <div class="card-clean">
        <h3>Email Analysis</h3>
        <p>Identify phishing emails and suspicious communication instantly.</p>
    </div>
    <div class="card-clean">
        <h3>URL Checker</h3>
        <p>Analyze links for phishing, fake domains, and malicious patterns.</p>
    </div>
    <div class="card-clean">
        <h3>Explainable AI</h3>
        <p>Understand WHY something is marked as scam with clear reasons.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# PERFORMANCE SECTION
st.markdown("""
<div style="border-top:1px solid rgba(255,255,255,0.06);margin:68px 0 0;padding-top:48px;"></div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-label">Model Performance</div>
<h2>Detection Accuracy</h2>
<p class="section-desc">
    Optimized models trained on real-world scam datasets with high precision and recall.
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stats-row">
    <div class="stat-box featured">
        <div class="big">95<span style="font-size:22px;color:#a878f0">%</span></div>
        <div class="stat-unit">Overall Accuracy</div>
        <div class="stat-sub">Across all detection models</div>
    </div>
    <div class="stat-box">
        <div class="big">94%</div>
        <div class="stat-unit">Precision</div>
    </div>
    <div class="stat-box">
        <div class="big">85%</div>
        <div class="stat-unit">Recall</div>
    </div>
    <div class="stat-box">
        <div class="big">89%</div>
        <div class="stat-unit">F1-score</div>
    </div>
</div>
""", unsafe_allow_html=True)

show_footer()