import streamlit as st
import base64
from pathlib import Path


def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""


def show_navbar(active_page="Home"):
    logo_path = Path("assets/logo.png")
    logo_base64 = get_base64_of_image(logo_path)

    st.markdown("""
    <style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"]      { display: none !important; }
    .block-container               { padding-top: 80px !important; }
    </style>
    """, unsafe_allow_html=True)

    navbar_html = f"""
    <style>
    .safeonyx-nav {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(12, 11, 20, 0.95);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        z-index: 999999;
        padding: 0.75rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        font-family: 'Inter', sans-serif;
    }}
    .nav-brand {{
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
    }}
    .nav-brand img {{
        height: 36px;
        filter: drop-shadow(0 0 6px rgba(130,80,200,0.4));
    }}
    .nav-brand-text {{ display: flex; flex-direction: column; }}
    .nav-brand-name {{
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.12em;
        color: #e8e0f8;
    }}
    .nav-brand-tagline {{
        font-size: 9px;
        color: #6b5a9e;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}
    .nav-links {{
        display: flex;
        gap: 0.3rem;
        flex-wrap: wrap;
    }}
    .nav-links a {{
        text-decoration: none;
        color: #7a80a0;
        font-size: 13px;
        padding: 6px 12px;
        border-radius: 8px;
        transition: 0.2s;
    }}
    .nav-links a:hover {{
        background: rgba(130,80,200,0.1);
        color: #e0daf5;
    }}
    .nav-links a.active {{
        background: rgba(130,80,200,0.2);
        color: #c4b5f7;
    }}
    </style>

    <div class="safeonyx-nav">
        <div class="nav-brand">
            <img src="data:image/png;base64,{logo_base64}" alt="SafeOnyx Logo">
            <div class="nav-brand-text">
                <span class="nav-brand-name">SAFEONYX</span>
                <span class="nav-brand-tagline">AI Scam Detection</span>
            </div>
        </div>
        <div class="nav-links">
            <a href="/" target="_self" class="{'active' if active_page == 'Home' else ''}">🏠 Home</a>
            <a href="/sms" target="_self" class="{'active' if active_page == 'SMS' else ''}">📱 SMS</a>
            <a href="/email" target="_self" class="{'active' if active_page == 'Email' else ''}">📧 Email</a>
            <a href="/url" target="_self" class="{'active' if active_page == 'URL' else ''}">🔗 URL</a>
            <a href="/screenshot" target="_self" class="{'active' if active_page == 'Screenshot' else ''}">📸 Screenshot</a>
        </div>
    </div>

    <script>
        // Move navbar out of Streamlit's stacked div into document body
        // so position:fixed works relative to the viewport, not a parent
        const nav = window.parent.document.querySelector('.safeonyx-nav');
        if (nav && nav.parentElement !== window.parent.document.body) {{
            window.parent.document.body.appendChild(nav);
        }}
        // Also inject the style into parent document head
        const style = nav ? nav.previousElementSibling : null;
        if (style && style.tagName === 'STYLE') {{
            window.parent.document.head.appendChild(style);
        }}
    </script>
    """

    st.markdown(navbar_html, unsafe_allow_html=True)