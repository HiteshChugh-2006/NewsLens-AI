"""
NewsLens AI - Analysis History Log
==================================
View, search, inspect, and manage stored article analysis history
from the local SQLite database (news_analysis.db).
"""

import streamlit as st
import pandas as pd
import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import AnalysisDatabase
from src.styles import get_custom_css

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analysis History | NewsLens AI",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Microsoft Fluent Light Theme CSS ────────────────────────────────────────
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ─── Initialize Database ─────────────────────────────────────────────────────
@st.cache_resource
def get_database():
    return AnalysisDatabase()

db = get_database()


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">📜</div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #047857;">
            NewsLens AI
        </div>
        <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">
            SQLite Audit Trail
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 4px; color: #64748B; font-size: 0.82rem; line-height: 1.7;">
        Querying local database:
        <br><code style="color: #047857; font-weight: 600;">news_analysis.db</code>
        <br><br>
        <strong>Stored Attributes:</strong>
        <ul style="padding-left: 18px; margin-top: 4px;">
            <li>Article body & preview</li>
            <li>ML classification & confidence</li>
            <li>Azure sentiment & tone distribution</li>
            <li>Extracted thematic key phrases</li>
            <li>Audit timestamp</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    if st.button("🔄 Refresh Database", use_container_width=True):
        st.rerun()


# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 16px 0 8px;">
    <div style="font-size: 2.4rem; font-weight: 800;
        background: linear-gradient(135deg, #065F46 0%, #059669 50%, #0D9488 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        📜 Analysis History & Audit Log
    </div>
    <div style="color: #64748B; font-size: 1rem; margin-top: 6px;">
        Auditable database records of all processed news articles with ML and Azure AI Language outputs
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ─── KPI Cards ───────────────────────────────────────────────────────────────
stats = db.get_statistics()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-value">{stats['total']}</span>
        <div class="kpi-label">Total Analyses</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-value" style="color:#E11D48;">{stats['fake']}</span>
        <div class="kpi-label">Fake Flagged</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-value" style="color:#059669;">{stats['real']}</span>
        <div class="kpi-label">Real Verified</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    last_ts = stats.get("latest_analysis")
    display_ts = last_ts.split(".")[0] if last_ts else "None"
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-value" style="font-size: 1.25rem; padding-top: 6px; color: #334155;">{display_ts}</span>
        <div class="kpi-label">Latest Timestamp</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Records Table & Search ──────────────────────────────────────────────────
all_records = db.get_all_records()

if not all_records:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card" style="text-align: center; padding: 40px 20px;">
        <span style="font-size: 2.8rem;">📭</span>
        <div style="font-size: 1.25rem; font-weight: 700; color: #047857; margin-top: 10px;">
            No Analysis Records in SQLite Database
        </div>
        <div style="color: #64748B; font-size: 0.9rem; max-width: 580px; margin: 8px auto 16px;">
            Whenever you run an article analysis on the <strong>News Detection</strong> page, 
            the complete output (ML prediction, Azure sentiment, and key phrases) is automatically stored here.
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown('<div class="section-header">🔍 Filter & Search History</div>', unsafe_allow_html=True)

    fcol1, fcol2, fcol3 = st.columns([1, 1, 2])

    with fcol1:
        pred_filter = st.selectbox(
            "Filter by ML Verdict:",
            options=["All", "FAKE", "REAL"],
            index=0
        )

    with fcol2:
        sent_filter = st.selectbox(
            "Filter by Sentiment:",
            options=["All", "positive", "neutral", "negative", "mixed", "not_configured"],
            index=0
        )

    with fcol3:
        search_query = st.text_input("Search Article Keywords:", placeholder="Type a keyword to filter...")

    # Apply filtering
    filtered_records = []
    for r in all_records:
        if pred_filter != "All" and r["ml_prediction"] != pred_filter:
            continue
        if sent_filter != "All" and r["sentiment"] != sent_filter:
            continue
        if search_query and search_query.lower() not in r["article_text"].lower():
            continue
        filtered_records.append(r)

    st.caption(f"Showing **{len(filtered_records)}** of **{len(all_records)}** total stored records")

    # Build display table
    table_rows = []
    for r in filtered_records:
        snippet = (r["article_text"][:65] + "...") if len(r["article_text"]) > 65 else r["article_text"]
        pred_icon = "🚨 Fake" if r["ml_prediction"] == "FAKE" else "✅ Real"
        conf_str = f"{r['ml_confidence']:.1%}" if r["ml_confidence"] is not None else "N/A"
        sent_display = r["sentiment"].capitalize()
        phrases_summary = ", ".join(r["key_phrases"][:3]) if r.get("key_phrases") else "None"
        if len(r.get("key_phrases", [])) > 3:
            phrases_summary += f" (+{len(r['key_phrases'])-3} more)"

        table_rows.append({
            "ID": r["id"],
            "Timestamp": r["created_at"].split(".")[0] if "." in r["created_at"] else r["created_at"],
            "ML Verdict": pred_icon,
            "ML Conf": conf_str,
            "Azure Sentiment": sent_display,
            "Key Phrases": phrases_summary,
            "Article Preview": snippet,
        })

    df_display = pd.DataFrame(table_rows)
    st.dataframe(df_display, hide_index=True, use_container_width=True)


    # ─── Individual Record Inspector ─────────────────────────────────────────
    st.markdown('<div class="section-header">🔎 Inspect Individual Record Details</div>', unsafe_allow_html=True)

    available_ids = [r["id"] for r in filtered_records] if filtered_records else [r["id"] for r in all_records]

    selected_id = st.selectbox(
        "Select Record ID to view complete details:",
        options=available_ids,
        format_func=lambda x: f"Record #{x}"
    )

    if selected_id:
        record = db.get_record_by_id(selected_id)
        if record:
            st.markdown(f"""
            <div class="info-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; border-bottom: 1px solid var(--border-light); padding-bottom: 10px;">
                    <div style="font-size: 1.2rem; font-weight: 800; color: #047857;">
                        Record #{record['id']} — Comprehensive Audit
                    </div>
                    <div style="font-size: 0.82rem; color: #64748B;">
                        🕒 Stored At: <strong style="color: #0F172A;">{record['created_at']}</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            dcol1, dcol2 = st.columns(2)

            with dcol1:
                st.markdown("""
                <div style="font-weight: 700; color: #047857; margin-bottom: 6px;">
                    🤖 Machine Learning Classification
                </div>
                """, unsafe_allow_html=True)

                is_fake = record["ml_prediction"] == "FAKE"
                pred_label = "🚨 FAKE NEWS" if is_fake else "✅ REAL NEWS"
                conf_val = f"{record['ml_confidence']:.2%}" if record["ml_confidence"] is not None else "N/A"
                badge_style = "color: #E11D48; background: #FFF1F2; border: 1px solid #FECDD3;" if is_fake else "color: #047857; background: #ECFDF5; border: 1px solid #A7F3D0;"

                st.markdown(f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 14px; border-radius: 10px; margin-bottom: 12px;">
                    <div>Verdict: <span style="display: inline-block; padding: 3px 12px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; {badge_style}">{pred_label}</span></div>
                    <div style="margin-top: 8px; color: #64748B; font-size: 0.88rem;">Model Confidence: <strong style="color: #0F172A;">{conf_val}</strong></div>
                </div>
                """, unsafe_allow_html=True)

            with dcol2:
                st.markdown("""
                <div style="font-weight: 700; color: #0078D4; margin-bottom: 6px;">
                    ☁️ Microsoft Azure AI Sentiment
                </div>
                """, unsafe_allow_html=True)

                sent_name = record["sentiment"].capitalize()
                conf_obj = record.get("sentiment_confidence") or {}

                pos_sc = f"{conf_obj.get('positive', 0):.2%}" if isinstance(conf_obj, dict) and "positive" in conf_obj else "N/A"
                neu_sc = f"{conf_obj.get('neutral', 0):.2%}" if isinstance(conf_obj, dict) and "neutral" in conf_obj else "N/A"
                neg_sc = f"{conf_obj.get('negative', 0):.2%}" if isinstance(conf_obj, dict) and "negative" in conf_obj else "N/A"

                st.markdown(f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 14px; border-radius: 10px; margin-bottom: 12px;">
                    <div>Overall Tone: <strong style="color: #0078D4;">{sent_name}</strong></div>
                    <div style="margin-top: 8px; font-size: 0.82rem; color: #64748B;">
                        Positive: <span style="color:#059669; font-weight: 600;">{pos_sc}</span> | 
                        Neutral: <span style="color:#D97706; font-weight: 600;">{neu_sc}</span> | 
                        Negative: <span style="color:#E11D48; font-weight: 600;">{neg_sc}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Key Phrases
            st.markdown("""
            <div style="font-weight: 700; color: #D97706; margin-top: 10px; margin-bottom: 6px;">
                🔑 Extracted Key Phrases & Entities
            </div>
            """, unsafe_allow_html=True)

            if record.get("key_phrases"):
                phrases_html = "".join([f'<span class="phrase-tag">{p}</span>' for p in record["key_phrases"]])
                st.markdown(f"<div>{phrases_html}</div>", unsafe_allow_html=True)
            else:
                st.caption("No key phrases extracted for this record.")

            # Full Article Text
            st.markdown("""
            <div style="font-weight: 700; color: #0F172A; margin-top: 16px; margin-bottom: 6px;">
                📄 Full Article Text
            </div>
            """, unsafe_allow_html=True)
            st.text_area(
                "Article Content",
                value=record["article_text"],
                height=180,
                disabled=True,
                label_visibility="collapsed"
            )

            # Action: Delete this record
            del_col1, del_col2 = st.columns([1, 4])
            with del_col1:
                if st.button(f"🗑️ Delete Record #{record['id']}", type="secondary"):
                    db.delete_record(record["id"])
                    st.success(f"Record #{record['id']} deleted successfully.")
                    st.rerun()


    # ─── Clear History Section (Danger Zone) ──────────────────────────────────
    st.markdown('<div class="section-header" style="color: #E11D48; border-color: rgba(225,29,72,0.3);">⚠️ Database Administration</div>', unsafe_allow_html=True)

    with st.expander("🚨 Clear All Analysis Records"):
        st.warning("This action is permanent and cannot be undone. All records stored in `news_analysis.db` will be wiped.")
        confirm_check = st.checkbox("Yes, I understand and want to permanently clear all audit history.")
        if st.button("Permanently Clear Database", type="primary", disabled=not confirm_check):
            db.clear_history()
            st.success("All analysis records cleared successfully.")
            st.rerun()


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 4px; font-weight: 600; color: #0F172A;">
        NewsLens AI · SQLite Audit Engine
    </div>
    <div style="font-size: 0.75rem; color: #94A3B8;">
        ACID compliant storage powered by SQLite3 · news_analysis.db
    </div>
</div>
""", unsafe_allow_html=True)
