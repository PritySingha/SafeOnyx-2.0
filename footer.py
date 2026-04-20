import streamlit as st
import base64
from pathlib import Path


def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""


def show_footer():
    logo_path = Path("assets/logo.png")
    logo_base64 = get_base64_of_image(logo_path)

    footer_html = f"""
    <style>
    .safeonyx-footer {{
        margin-top: 68px;
        padding: 36px 0 22px;
        border-top: 1px solid rgba(255,255,255,0.06);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 20px;
        font-family: 'Inter', sans-serif;
    }}
    .footer-brand {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .footer-brand img {{
        height: 34px;
        filter: drop-shadow(0 0 6px rgba(130,80,200,0.3));
    }}
    .footer-brand-text {{ display: flex; flex-direction: column; }}
    .footer-brand-name {{
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #e8e0f8;
    }}
    .footer-brand-tagline {{
        font-size: 9px;
        letter-spacing: 0.12em;
        color: #6b5a9e;
        text-transform: uppercase;
    }}
    .footer-copy {{
        font-size: 12px;
        color: #363960;
    }}
    @media (max-width: 680px) {{
        .safeonyx-footer {{
            flex-direction: column;
            text-align: center;
        }}
    }}
    </style>

    <div class="safeonyx-footer">
        <div class="footer-brand">
            <img src="data:image/png;base64,{logo_base64}" alt="SafeOnyx">
            <div class="footer-brand-text">
                <span class="footer-brand-name">SAFEONYX</span>
                <span class="footer-brand-tagline">AI Scam Detection</span>
            </div>
        </div>
        <div class="footer-copy">
            © 2026 SafeOnyx • Built for detecting online scams (SMS, Email, URL, Screenshot)
        </div>
    </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)