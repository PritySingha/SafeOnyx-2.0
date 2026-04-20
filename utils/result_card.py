"""
result_card.py — Shared result rendering for all SafeOnyx pages.
"""
import streamlit as st


def _verdict_class(label: str) -> str:
    l = label.lower()
    if l in ("scam", "phishing", "spam"):
        return "verdict-danger"
    if l in ("suspicious", "medium"):
        return "verdict-warn"
    return "verdict-safe"


def _bar_class(risk: int) -> str:
    if risk >= 60:
        return "risk-fill-danger"
    if risk >= 35:
        return "risk-fill-warn"
    return "risk-fill-safe"


def _risk_color(risk: int) -> str:
    if risk >= 60:
        return "#EF4444"
    if risk >= 35:
        return "#F59E0B"
    return "#22C55E"


def render_result(result: dict, show_extracted: bool = False):
    """
    Render a result card given a result dict.
    Keys: prediction, risk_score, message, [extracted_text], [triggers], [features]
    """
    label = result.get("prediction", "Unknown")
    risk  = result.get("risk_score", 0)
    msg   = result.get("message", "")

    if label == "Error":
        st.error(msg or "An error occurred.")
        return

    verdict_cls = _verdict_class(label)
    bar_cls     = _bar_class(risk)
    risk_color  = _risk_color(risk)

    st.markdown(f"""
    <div class="result-card">
      <div class="result-header">
        <div>
          <div class="result-label">ANALYSIS RESULT</div>
          <div class="result-verdict {verdict_cls}">{label}</div>
        </div>
        <div class="risk-circle-wrap">
          <div class="risk-pct" style="color:{risk_color}">{risk}%</div>
          <div class="risk-pct-label">Risk Score</div>
        </div>
      </div>

      <div class="risk-bar-track">
        <div class="risk-bar-fill {bar_cls}" style="width:{risk}%"></div>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:11px;color:var(--text-faint);margin-bottom:16px;">
        <span>0% Safe</span><span>50% Suspicious</span><span>100% Scam</span>
      </div>

      {'<div class="result-message">' + msg + '</div>' if msg else ''}
    </div>
    """, unsafe_allow_html=True)

    # Extracted text (screenshot page)
    if show_extracted and result.get("extracted_text"):
        st.markdown("**Extracted Text (OCR)**")
        st.markdown(f"""
        <div class="extracted-text-box">{result['extracted_text']}</div>
        """, unsafe_allow_html=True)

    # Keyword triggers
    triggers = result.get("triggers", [])
    if triggers:
        st.markdown(
            "**Detected signals:** " +
            " ".join(f"`{t}`" for t in triggers),
            unsafe_allow_html=False
        )

    # URL features table
    features = result.get("features", {})
    if features:
        with st.expander("📊 URL Feature Breakdown"):
            col1, col2 = st.columns(2)
            items = list(features.items())
            mid   = len(items) // 2
            for k, v in items[:mid]:
                col1.metric(k.replace("_", " ").title(), v)
            for k, v in items[mid:]:
                col2.metric(k.replace("_", " ").title(), v)
