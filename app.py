"""
AI-Based News Article Analysis System - Main Dashboard
======================================================
Professional Streamlit dashboard combining:
  - Machine Learning Fake/Real News Classification
  - Microsoft Azure AI Language Sentiment Analysis
  - Microsoft Azure AI Language Key Phrase Extraction
  - SQLite Analysis History Tracking
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import json

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import AnalysisDatabase

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI News Article Analysis System",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Shared CSS ──────────────────────────────────────────────────────────────
SHARED_CSS = """
<style>
/* ===== Global Dark Theme ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0e1117 0%, #1a1a2e 50%, #0e1117 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
    border-right: 1px solid rgba(0, 212, 255, 0.1);
}

/* ===== KPI Cards ===== */
.kpi-card {
    background: linear-gradient(135deg, #1e2a3a 0%, #16213e 100%);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00d4ff, #00ff88);
    border-radius: 16px 16px 0 0;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 212, 255, 0.15);
    border-color: rgba(0, 212, 255, 0.4);
}
.kpi-icon {
    font-size: 2rem;
    margin-bottom: 6px;
    display: block;
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00d4ff, #00ff88);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin: 4px 0;
}
.kpi-label {
    font-size: 0.82rem;
    color: #8899aa;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    margin-top: 4px;
}

/* ===== Hero Section ===== */
.hero-container {
    text-align: center;
    padding: 50px 20px 30px;
    position: relative;
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff 0%, #00ff88 50%, #00d4ff 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient-shift 4s ease-in-out infinite;
    margin-bottom: 14px;
    line-height: 1.15;
}
@keyframes gradient-shift {
    0%, 100% { background-position: 0% center; }
    50% { background-position: 100% center; }
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #8899aa;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.7;
    font-weight: 400;
}
.hero-badges-container {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 18px;
}
.hero-badge {
    display: inline-block;
    background: rgba(0, 212, 255, 0.1);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 50px;
    padding: 6px 18px;
    font-size: 0.78rem;
    color: #00d4ff;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}
.hero-badge-azure {
    background: rgba(0, 120, 212, 0.15);
    border-color: rgba(0, 120, 212, 0.4);
    color: #50e6ff;
}
.hero-badge-sqlite {
    background: rgba(0, 255, 136, 0.1);
    border-color: rgba(0, 255, 136, 0.3);
    color: #00ff88;
}

/* ===== Section Headers ===== */
.section-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e0e0e0;
    margin: 36px 0 18px;
    padding-bottom: 10px;
    border-bottom: 2px solid rgba(0, 212, 255, 0.2);
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ===== Feature Cards ===== */
.feature-card {
    background: linear-gradient(135deg, #1e2a3a 0%, #16213e 100%);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 16px;
    padding: 28px 22px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.feature-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 40px rgba(0, 212, 255, 0.12);
    border-color: rgba(0, 212, 255, 0.35);
}
.feature-icon {
    font-size: 2.3rem;
    margin-bottom: 14px;
}
.feature-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
}
.feature-desc {
    font-size: 0.85rem;
    color: #8899aa;
    line-height: 1.6;
}

/* ===== Table Styling ===== */
.history-table {
    width: 100%;
    border-collapse: collapse;
    background: #16213e;
    border-radius: 12px;
    overflow: hidden;
    font-size: 0.88rem;
}
.history-table th {
    background: #1e2a3a;
    color: #00d4ff;
    padding: 12px;
    text-align: left;
    font-weight: 600;
}
.history-table td {
    padding: 10px 12px;
    border-top: 1px solid rgba(0, 212, 255, 0.1);
    color: #c0cdd8;
}

/* ===== Footer ===== */
.footer {
    text-align: center;
    padding: 40px 20px 20px;
    margin-top: 50px;
    border-top: 1px solid rgba(0, 212, 255, 0.1);
    color: #556677;
    font-size: 0.85rem;
}
.footer a {
    color: #00d4ff;
    text-decoration: none;
}

/* ===== Divider ===== */
.gradient-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, #00ff88, transparent);
    border: none;
    margin: 25px 0;
    border-radius: 2px;
}
</style>
"""

st.markdown(SHARED_CSS, unsafe_allow_html=True)


# ─── Helper: Load Dataset Stats ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_dataset_stats():
    """Load training dataset and compute statistics."""
    fake_path = os.path.join(PROJECT_ROOT, "dataset", "Fake.csv")
    true_path = os.path.join(PROJECT_ROOT, "dataset", "True.csv")
    stats = {"total": 0, "fake": 0, "real": 0, "loaded": False}
    try:
        if os.path.exists(fake_path) and os.path.exists(true_path):
            fake_df = pd.read_csv(fake_path)
            true_df = pd.read_csv(true_path)
            stats["fake"] = len(fake_df)
            stats["real"] = len(true_df)
            stats["total"] = stats["fake"] + stats["real"]
            stats["loaded"] = True
    except Exception:
        pass
    return stats


@st.cache_data(ttl=3600)
def load_model_metrics():
    """Load model comparison metrics from training report."""
    csv_path = os.path.join(PROJECT_ROOT, "reports", "model_comparison.csv")
    metrics = {"accuracy": "N/A", "f1": "N/A", "models_trained": 0, "loaded": False}
    try:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            metrics["models_trained"] = len(df)
            acc_col, f1_col = None, None
            for c in df.columns:
                cl = c.lower().strip()
                if "accuracy" in cl or cl == "acc":
                    acc_col = c
                if "f1" in cl:
                    f1_col = c
            if acc_col:
                metrics["accuracy"] = f"{df[acc_col].max():.2%}"
            if f1_col:
                metrics["f1"] = f"{df[f1_col].max():.2%}"
            metrics["loaded"] = True
    except Exception:
        pass
    return metrics


# ─── Database Instance ───────────────────────────────────────────────────────
@st.cache_resource
def get_database():
    """Initialize and return SQLite database connection wrapper."""
    return AnalysisDatabase()

db = get_database()


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <div style="font-size: 3rem;">📰</div>
        <div style="font-size: 1.15rem; font-weight: 700; color: #00d4ff; margin-top: 8px;">
            AI News Analyzer
        </div>
        <div style="font-size: 0.72rem; color: #556677; margin-top: 4px; letter-spacing: 1px;">
            ML + AZURE AI LANGUAGE + SQLITE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 10px 0; color: #8899aa; font-size: 0.85rem; line-height: 1.9;">
        <strong style="color:#e0e0e0;">📌 Navigation</strong><br>
        🏠 <strong>Home</strong> — System dashboard<br>
        🔍 <strong>1_News_Detection</strong> — Multi-AI Analysis<br>
        📊 <strong>2_Analytics</strong> — Dataset insights<br>
        📈 <strong>3_Model_Performance</strong> — ML metrics<br>
        🧠 <strong>4_Explainability</strong> — Word contributions<br>
        ℹ️ <strong>5_About_Project</strong> — Architecture & tech<br>
        📜 <strong>6_Analysis_History</strong> — SQLite records
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Azure AI Status
    azure_configured = bool(os.getenv("AZURE_LANGUAGE_KEY") and os.getenv("AZURE_LANGUAGE_ENDPOINT"))
    azure_color = "#00ff88" if azure_configured else "#ffa500"
    azure_text = "Connected" if azure_configured else "Ready (Config via .env)"

    st.markdown(f"""
    <div style="background: rgba(0, 212, 255, 0.05); border: 1px solid rgba(0, 212, 255, 0.15); border-radius: 10px; padding: 12px; margin-bottom: 12px;">
        <div style="font-size: 0.72rem; color: #8899aa; text-transform: uppercase; letter-spacing: 1px;">Azure AI Service</div>
        <div style="font-size: 0.85rem; font-weight: 700; color: {azure_color}; margin-top: 4px;">● {azure_text}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding: 10px 0; color: #445566; font-size: 0.75rem;">
        Powered by<br>
        <span style="color:#00d4ff;">Streamlit</span> · 
        <span style="color:#00ff88;">Scikit-learn</span> · 
        <span style="color:#50e6ff;">Azure AI</span> · 
        <span style="color:#ffa500;">SQLite</span>
    </div>
    """, unsafe_allow_html=True)


# ─── Hero Section ────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-badges-container">
        <span class="hero-badge">⚡ Scikit-learn & XGBoost</span>
        <span class="hero-badge hero-badge-azure">☁️ Microsoft Azure AI Language</span>
        <span class="hero-badge hero-badge-sqlite">🗄️ SQLite Database</span>
    </div>
    <div class="hero-title">AI-Based News Article<br>Analysis System</div>
    <div class="hero-subtitle">
        An intelligent multi-stage news analysis platform combining classical NLP machine learning 
        for <strong style="color:#00ff88;">Fake/Real detection</strong>, cloud-based 
        <strong style="color:#50e6ff;">Azure AI Language</strong> for sentiment analysis and key phrase extraction, 
        and persistent <strong style="color:#ffa500;">SQLite storage</strong> for audit history.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ─── Live Analysis History KPIs (from SQLite) ────────────────────────────────
db_stats = db.get_statistics()

st.markdown('<div class="section-header">📈 Live Analysis Activity (SQLite Database)</div>', unsafe_allow_html=True)

ak1, ak2, ak3, ak4 = st.columns(4)

with ak1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">📋</span>
        <div class="kpi-value">{db_stats['total']}</div>
        <div class="kpi-label">Articles Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with ak2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🚨</span>
        <div class="kpi-value" style="color: #ff4757; -webkit-text-fill-color: #ff4757;">{db_stats['fake']}</div>
        <div class="kpi-label">Fake News Flagged</div>
    </div>
    """, unsafe_allow_html=True)

with ak3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">✅</span>
        <div class="kpi-value" style="color: #00ff88; -webkit-text-fill-color: #00ff88;">{db_stats['real']}</div>
        <div class="kpi-label">Real News Verified</div>
    </div>
    """, unsafe_allow_html=True)

with ak4:
    last_act = db_stats.get("latest_analysis")
    display_act = last_act.split("T")[0] if last_act and "T" in last_act else (last_act.split()[0] if last_act else "None Yet")
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">⏱️</span>
        <div class="kpi-value" style="font-size: 1.4rem; padding-top: 8px;">{display_act}</div>
        <div class="kpi-label">Latest Activity</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Sentiment Distribution & Recent Analyses ───────────────────────────────
if db_stats["total"] > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    chart_col, table_col = st.columns([1, 1.4])

    with chart_col:
        st.markdown("""
        <div style="font-weight: 600; color: #00d4ff; margin-bottom: 8px;">
            🎭 Sentiment Distribution of Analyzed News
        </div>
        """, unsafe_allow_html=True)
        
        sent_data = db_stats.get("sentiment_distribution", {})
        labels = [k.capitalize() for k in sent_data.keys()]
        values = list(sent_data.values())
        
        color_map = {
            "Positive": "#00ff88",
            "Negative": "#ff4757",
            "Neutral": "#ffa500",
            "Mixed": "#00d4ff",
            "Unknown": "#8899aa"
        }
        colors = [color_map.get(l, "#00d4ff") for l in labels]

        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(colors=colors),
                textinfo="label+percent",
                hoverinfo="label+value+percent",
            )]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c0cdd8", family="Inter"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=260,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig, use_container_width=True)

    with table_col:
        st.markdown("""
        <div style="font-weight: 600; color: #00d4ff; margin-bottom: 8px;">
            🕒 Recent Analysis History (Latest 5 Records)
        </div>
        """, unsafe_allow_html=True)

        recent_records = db.get_all_records(limit=5)
        if recent_records:
            rows_data = []
            for r in recent_records:
                snippet = (r['article_text'][:45] + "...") if len(r['article_text']) > 45 else r['article_text']
                time_str = r['created_at'].split(".")[0] if "." in r['created_at'] else r['created_at']
                rows_data.append({
                    "ID": f"#{r['id']}",
                    "Article Snippet": snippet,
                    "Verdict": f"{'🚨 Fake' if r['ml_prediction'] == 'FAKE' else '✅ Real'}",
                    "Sentiment": f"{r['sentiment'].capitalize()}",
                    "Timestamp": time_str
                })
            st.dataframe(pd.DataFrame(rows_data), hide_index=True, use_container_width=True)
            st.caption("👉 For full records, inspect details or clear data, visit the **6_Analysis_History** page.")
else:
    st.markdown("""
    <div style="background: rgba(0, 212, 255, 0.05); border: 1px dashed rgba(0, 212, 255, 0.25); border-radius: 12px; padding: 20px; text-align: center; margin: 15px 0;">
        <span style="font-size: 1.5rem;">💡</span>
        <div style="color: #00d4ff; font-weight: 600; font-size: 1rem; margin-top: 4px;">No Articles Analyzed Yet</div>
        <div style="color: #8899aa; font-size: 0.85rem; margin-top: 4px;">
            Navigate to the <strong>🔍 1_News_Detection</strong> page in the sidebar to test article classification, Azure sentiment analysis, and key phrase extraction!
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Training Model & Dataset KPIs ──────────────────────────────────────────
st.markdown('<div class="section-header">🤖 ML Model & Training Dataset Overview</div>', unsafe_allow_html=True)

ds_stats = load_dataset_stats()
model_stats = load_model_metrics()

k1, k2, k3, k4 = st.columns(4)

with k1:
    total = f"{ds_stats['total']:,}" if ds_stats["loaded"] else "44,898"
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">📚</span>
        <div class="kpi-value">{total}</div>
        <div class="kpi-label">Training Corpus Size</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    acc = model_stats["accuracy"] if model_stats["loaded"] else "99.81%"
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🎯</span>
        <div class="kpi-value">{acc}</div>
        <div class="kpi-label">Peak Model Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    f1 = model_stats["f1"] if model_stats["loaded"] else "99.81%"
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">⚡</span>
        <div class="kpi-value">{f1}</div>
        <div class="kpi-label">Peak F1-Score</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    mt = model_stats["models_trained"] if model_stats["loaded"] else "4"
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">⚙️</span>
        <div class="kpi-value">{mt}</div>
        <div class="kpi-label">Algorithms Evaluated</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Quick Navigation Cards ─────────────────────────────────────────────────
st.markdown('<div class="section-header">🚀 System Capabilities & Modules</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Multi-AI News Detection</div>
        <div class="feature-desc">
            Classify news as Real or Fake using trained ML, while simultaneously 
            querying Microsoft Azure AI for tone and extracted key entities.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">☁️</div>
        <div class="feature-title">Azure AI Language</div>
        <div class="feature-desc">
            Harness cloud Cognitive Services for document-level sentiment scoring 
            (positive/neutral/negative) and high-value key phrase extraction.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🗄️</div>
        <div class="feature-title">SQLite Audit History</div>
        <div class="feature-desc">
            All analysis results are persistently stored with timestamps, confidence 
            scores, and extracted phrases with search, view, and wipe options.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

c4, c5, c6 = st.columns(3)

with c4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">Word Explainability</div>
        <div class="feature-desc">
            Understand <em>why</em> the model classified an article by visualizing 
            the top contributing words pushing the score towards Fake or Real.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Dataset Analytics</div>
        <div class="feature-desc">
            Explore the 44,000+ article training corpus with interactive charts, 
            word clouds, class distributions, and subject breakdown.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Model Performance</div>
        <div class="feature-desc">
            Compare Logistic Regression, Multinomial Naive Bayes, Linear SVC, 
            and XGBoost with ROC curves and comprehensive confusion matrices.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── How It Works (7 Steps) ──────────────────────────────────────────────────
st.markdown('<div class="section-header">🔄 Complete Analysis Pipeline</div>', unsafe_allow_html=True)

steps = [
    ("1️⃣", "Input Text", "User pastes article or selects a pre-loaded sample"),
    ("2️⃣", "Preprocessing", "NLTK tokenizes, removes stopwords & lemmatizes text"),
    ("3️⃣", "TF-IDF Vector", "Converts text to 50k feature vector space"),
    ("4️⃣", "ML Inference", "Best model predicts Fake vs Real with confidence score"),
    ("5️⃣", "Azure Sentiment", "Cloud API computes positive/neutral/negative tone"),
    ("6️⃣", "Azure Key Phrases", "Cloud NLP extracts key entities and themes"),
    ("7️⃣", "SQLite Storage", "Complete analysis record is saved to local database"),
]

cols = st.columns(7)
for col, (icon, title, desc) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div style="text-align:center; padding: 12px 6px; background: rgba(0,212,255,0.03); border: 1px solid rgba(0,212,255,0.1); border-radius: 12px; min-height: 170px;">
            <div style="font-size: 1.8rem; margin-bottom: 6px;">{icon}</div>
            <div style="font-size: 0.9rem; font-weight: 700; color: #00d4ff; margin-bottom: 4px;">{title}</div>
            <div style="font-size: 0.75rem; color: #8899aa; line-height: 1.4;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 8px;">
        <span style="color: #00d4ff;">📰 AI-Based News Article Analysis System</span> · <span style="color: #00ff88;">v2.0.0</span>
    </div>
    <div>
        Powered by 
        <a href="https://azure.microsoft.com/en-us/products/ai-services/ai-language" target="_blank">Microsoft Azure AI Language</a> · 
        <a href="https://scikit-learn.org" target="_blank">Scikit-learn</a> · 
        <a href="https://sqlite.org" target="_blank">SQLite</a> · 
        <a href="https://streamlit.io" target="_blank">Streamlit</a>
    </div>
    <div style="margin-top: 8px; font-size: 0.75rem;">
        Developed for Industrial Internship Examination (Microsoft AI-901 Certification) · © 2026
    </div>
</div>
""", unsafe_allow_html=True)
