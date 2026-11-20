"""
AI-Based News Article Analysis - Analysis History Page
======================================================
View, search, inspect, and manage stored article analysis history
from the local SQLite database (news_analysis.db).
"""

import streamlit as st
import pandas as pd
import os
import sys
import json

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import AnalysisDatabase

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analysis History | AI News Analyzer",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Shared CSS ──────────────────────────────────────────────────────────────
SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0e1117 0%, #1a1a2e 50%, #0e1117 100%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
    border-right: 1px solid rgba(0, 212, 255, 0.1);
}
.kpi-card {
    background: linear-gradient(135deg, #1e2a3a 0%, #16213e 100%);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 16px; padding: 22px 20px; text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.05);
    position: relative; overflow: hidden;
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #00d4ff, #00ff88); border-radius: 16px 16px 0 0;
}
.kpi-value { font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(135deg, #00d4ff, #00ff88);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.kpi-label { font-size: 0.82rem; color: #8899aa; text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 600; margin-top: 4px; }
.section-header { font-size: 1.4rem; font-weight: 700; color: #e0e0e0;
    margin: 32px 0 16px; padding-bottom: 10px;
    border-bottom: 2px solid rgba(0, 212, 255, 0.2); }
.gradient-divider { height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, #00ff88, transparent);
    border: none; margin: 25px 0; border-radius: 2px; }

/* Detail Card */
.detail-card {
    background: linear-gradient(135deg, #1e2a3a 0%, #16213e 100%);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 16px; padding: 24px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.25);
    margin: 16px 0;
}

/* Badges */
.badge-fake {
    background: rgba(255, 71, 87, 0.2);
    color: #ff4757;
    border: 1px solid rgba(255, 71, 87, 0.5);
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
}
.badge-real {
    background: rgba(0, 255, 136, 0.2);
    color: #00ff88;
    border: 1px solid rgba(0, 255, 136, 0.5);
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
}

/* Phrase tag */
.phrase-tag {
    display: inline-block;
    padding: 5px 14px;
    margin: 4px;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 500;
    background: rgba(0, 212, 255, 0.1);
    color: #00d4ff;
    border: 1px solid rgba(0, 212, 255, 0.25);
}
</style>
"""

st.markdown(SHARED_CSS, unsafe_allow_html=True)

# ─── Initialize Database ─────────────────────────────────────────────────────
@st.cache_resource
def get_database():
    return AnalysisDatabase()

db = get_database()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <div style="font-size: 3rem;">📜</div>
        <div style="font-size: 1.15rem; font-weight: 700; color: #00d4ff; margin-top: 8px;">
            Analysis History
        </div>
        <div style="font-size: 0.72rem; color: #556677; margin-top: 4px; letter-spacing: 1px;">
            SQLITE AUDIT TRAIL
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 10px 0; color: #8899aa; font-size: 0.85rem; line-height: 1.8;">
        This page queries the local <strong style="color:#00d4ff;">news_analysis.db</strong> SQLite database.
        <br><br>
        All records store:
        <ul style="padding-left: 18px; margin-top: 6px;">
            <li>Input news article</li>
            <li>ML classification & confidence</li>
            <li>Azure sentiment & scores</li>
            <li>Azure extracted key phrases</li>
            <li>Timestamp</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    if st.button("🔄 Refresh Database Records", use_container_width=True):
        st.rerun()


# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 20px 0 10px;">
    <div style="font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #00ff88);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        📜 Analysis History Log
    </div>
    <div style="color: #8899aa; font-size: 1rem; margin-top: 6px;">
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
        <span class="kpi-value" style="color:#ff4757; -webkit-text-fill-color:#ff4757;">{stats['fake']}</span>
        <div class="kpi-label">Fake Flagged</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-value" style="color:#00ff88; -webkit-text-fill-color:#00ff88;">{stats['real']}</span>
        <div class="kpi-label">Real Verified</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    last_ts = stats.get("latest_analysis")
    display_ts = last_ts.split(".")[0] if last_ts else "None"
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-value" style="font-size: 1.25rem; padding-top: 10px;">{display_ts}</span>
        <div class="kpi-label">Latest Timestamp</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Records Table & Search ──────────────────────────────────────────────────
all_records = db.get_all_records()

if not all_records:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="detail-card" style="text-align: center; padding: 40px 20px;">
        <span style="font-size: 3rem;">📭</span>
        <div style="font-size: 1.3rem; font-weight: 700; color: #00d4ff; margin-top: 12px;">
            No Analysis Records in SQLite Database
        </div>
        <div style="color: #8899aa; font-size: 0.95rem; max-width: 600px; margin: 10px auto 20px;">
            Whenever you run an article analysis on the <strong>1_News_Detection</strong> page, 
            the complete result (ML prediction, sentiment, and key phrases) is automatically stored here.
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
        search_query = st.text_input("Search in Article Text:", placeholder="Type a keyword to filter...")

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

    st.markdown(f"**Showing {len(filtered_records)} of {len(all_records)} total records**")

    # Build display table
    table_rows = []
    for r in filtered_records:
        snippet = (r["article_text"][:70] + "...") if len(r["article_text"]) > 70 else r["article_text"]
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
            <div class="detail-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <div style="font-size: 1.25rem; font-weight: 700; color: #00d4ff;">
                        Record #{record['id']} — Details
                    </div>
                    <div style="font-size: 0.85rem; color: #8899aa;">
                        🕒 Stored At: <strong style="color: #e0e0e0;">{record['created_at']}</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            dcol1, dcol2 = st.columns(2)

            with dcol1:
                st.markdown("""
                <div style="font-weight: 700; color: #00ff88; margin-bottom: 8px;">
                    🤖 Machine Learning Prediction
                </div>
                """, unsafe_allow_html=True)

                pred_badge = "badge-fake" if record["ml_prediction"] == "FAKE" else "badge-real"
                pred_label = "🚨 FAKE NEWS" if record["ml_prediction"] == "FAKE" else "✅ REAL NEWS"
                conf_val = f"{record['ml_confidence']:.2%}" if record["ml_confidence"] is not None else "N/A"

                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.2); padding: 14px; border-radius: 10px; margin-bottom: 12px;">
                    <div>Prediction: <span class="{pred_badge}">{pred_label}</span></div>
                    <div style="margin-top: 8px; color: #8899aa;">Confidence: <strong style="color: #e0e0e0;">{conf_val}</strong></div>
                </div>
                """, unsafe_allow_html=True)

            with dcol2:
                st.markdown("""
                <div style="font-weight: 700; color: #50e6ff; margin-bottom: 8px;">
                    ☁️ Azure AI Language Sentiment
                </div>
                """, unsafe_allow_html=True)

                sent_name = record["sentiment"].capitalize()
                conf_obj = record.get("sentiment_confidence") or {}
                
                pos_sc = f"{conf_obj.get('positive', 0):.2%}" if isinstance(conf_obj, dict) else "N/A"
                neu_sc = f"{conf_obj.get('neutral', 0):.2%}" if isinstance(conf_obj, dict) else "N/A"
                neg_sc = f"{conf_obj.get('negative', 0):.2%}" if isinstance(conf_obj, dict) else "N/A"

                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.2); padding: 14px; border-radius: 10px; margin-bottom: 12px;">
                    <div>Overall Sentiment: <strong style="color: #00d4ff;">{sent_name}</strong></div>
                    <div style="margin-top: 8px; font-size: 0.82rem; color: #8899aa;">
                        Positive: <span style="color:#00ff88;">{pos_sc}</span> | 
                        Neutral: <span style="color:#ffa500;">{neu_sc}</span> | 
                        Negative: <span style="color:#ff4757;">{neg_sc}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Key Phrases
            st.markdown("""
            <div style="font-weight: 700; color: #ffa500; margin-top: 10px; margin-bottom: 8px;">
                🔑 Extracted Key Phrases
            </div>
            """, unsafe_allow_html=True)

            if record.get("key_phrases"):
                phrases_html = "".join([f'<span class="phrase-tag">{p}</span>' for p in record["key_phrases"]])
                st.markdown(f"<div>{phrases_html}</div>", unsafe_allow_html=True)
            else:
                st.caption("No key phrases extracted for this record.")

            # Full Article Text
            st.markdown("""
            <div style="font-weight: 700; color: #00d4ff; margin-top: 18px; margin-bottom: 8px;">
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
    st.markdown('<div class="section-header" style="color: #ff4757; border-color: rgba(255,71,87,0.3);">⚠️ Database Management</div>', unsafe_allow_html=True)

    with st.expander("🚨 Clear All Analysis Records"):
        st.warning("This action is irreversible. All records stored in `news_analysis.db` will be permanently removed.")
        confirm_check = st.checkbox("Yes, I understand and want to wipe all stored analysis history.")
        if st.button("Permanently Clear Database", type="primary", disabled=not confirm_check):
            db.clear_history()
            st.success("Analysis history cleared successfully.")
            st.rerun()


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer" style="text-align: center; padding: 40px 20px 20px; margin-top: 50px; border-top: 1px solid rgba(0, 212, 255, 0.1); color: #556677; font-size: 0.85rem;">
    <div style="margin-bottom: 8px;">
        <span style="color: #00d4ff;">📰 AI-Based News Article Analysis System</span> · <span style="color: #00ff88;">v2.0.0</span>
    </div>
    <div>
        Persistent storage powered by SQLite · news_analysis.db
    </div>
</div>
""", unsafe_allow_html=True)
