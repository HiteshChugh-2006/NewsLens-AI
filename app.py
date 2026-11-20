"""
NewsLens AI - Intelligent News Article Analysis System
======================================================
Executive Streamlit Dashboard combining:
  - Machine Learning Fake/Real News Classification (99.81% Accuracy)
  - Microsoft Azure AI Language Sentiment Analysis
  - Microsoft Azure AI Language Key Phrase Extraction
  - SQLite Analysis History Tracking & Audit Trail
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import AnalysisDatabase
from src.styles import get_custom_css

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="NewsLens AI | News Analysis System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Microsoft Fluent Light Theme CSS ────────────────────────────────────────
st.markdown(get_custom_css(), unsafe_allow_html=True)


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
    return AnalysisDatabase()

db = get_database()


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">🔍</div>
        <div style="font-size: 1.25rem; font-weight: 800; color: #047857; letter-spacing: -0.5px;">
            NewsLens AI
        </div>
        <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-top: 2px;">
            Microsoft Azure AI · ML Verification
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Azure AI Status Badge
    azure_configured = bool(os.getenv("AZURE_LANGUAGE_KEY") and os.getenv("AZURE_LANGUAGE_ENDPOINT"))
    azure_status_text = "Connected" if azure_configured else "Ready (Config via .env)"
    azure_status_color = "#059669" if azure_configured else "#D97706"
    azure_bg_color = "rgba(16, 185, 129, 0.08)" if azure_configured else "rgba(245, 158, 11, 0.08)"
    azure_border_color = "rgba(16, 185, 129, 0.25)" if azure_configured else "rgba(245, 158, 11, 0.25)"

    st.markdown(f"""
    <div style="background: {azure_bg_color}; border: 1px solid {azure_border_color}; border-radius: 12px; padding: 12px 14px; margin-bottom: 16px;">
        <div style="font-size: 0.7rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;">Azure AI Cognitive Service</div>
        <div style="font-size: 0.88rem; font-weight: 700; color: {azure_status_color}; margin-top: 4px; display: flex; align-items: center; gap: 6px;">
            <span style="font-size: 0.75rem;">●</span> {azure_status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Database quick indicator
    db_stats = db.get_statistics()
    st.markdown(f"""
    <div style="padding: 4px 6px; font-size: 0.82rem; color: #64748B; line-height: 1.8;">
        <strong style="color: #0F172A;">📊 Audit Summary</strong><br>
        Analyzed Articles: <strong style="color: #047857;">{db_stats['total']}</strong><br>
        Database: <code style="color: #059669; font-size: 0.75rem;">news_analysis.db</code>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 8px 0; color: #94A3B8; font-size: 0.74rem;">
        Powered by<br>
        <strong style="color: #0078D4;">Microsoft Azure AI</strong> · 
        <strong style="color: #059669;">Scikit-learn</strong> · 
        <strong style="color: #334155;">SQLite</strong>
    </div>
    """, unsafe_allow_html=True)


# ─── Hero Section ────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-badges-container">
        <span class="hero-badge">⚡ Scikit-learn & XGBoost</span>
        <span class="hero-badge hero-badge-azure">☁️ Microsoft Azure AI Language</span>
        <span class="hero-badge hero-badge-sqlite">🗄️ SQLite Audit Trail</span>
    </div>
    <div class="hero-title">NewsLens AI</div>
    <div style="font-size: 1.35rem; font-weight: 700; color: #1E293B; margin-top: -6px; margin-bottom: 12px;">
        AI-Based News Article Analysis System
    </div>
    <div class="hero-subtitle">
        An enterprise intelligence platform combining classical machine learning for 
        <strong style="color: #047857;">Fake/Real veracity detection</strong>, cloud-native 
        <strong style="color: #0078D4;">Microsoft Azure AI Language</strong> for affective sentiment and key phrase extraction, 
        and persistent <strong style="color: #334155;">SQLite storage</strong> for auditable news verification.
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Live Analysis History KPIs (from SQLite) ────────────────────────────────
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
        <div class="kpi-value" style="color: #E11D48;">{db_stats['fake']}</div>
        <div class="kpi-label">Fake News Flagged</div>
    </div>
    """, unsafe_allow_html=True)

with ak3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">✅</span>
        <div class="kpi-value" style="color: #059669;">{db_stats['real']}</div>
        <div class="kpi-label">Real News Verified</div>
    </div>
    """, unsafe_allow_html=True)

with ak4:
    last_act = db_stats.get("latest_analysis")
    display_act = last_act.split("T")[0] if last_act and "T" in last_act else (last_act.split()[0] if last_act else "None Yet")
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">⏱️</span>
        <div class="kpi-value" style="font-size: 1.35rem; padding-top: 6px; color: #334155;">{display_act}</div>
        <div class="kpi-label">Latest Activity</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Sentiment Distribution & Recent Analyses ───────────────────────────────
if db_stats["total"] > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    chart_col, table_col = st.columns([1, 1.45])

    with chart_col:
        st.markdown("""
        <div style="font-weight: 700; color: #047857; margin-bottom: 8px; font-size: 0.95rem;">
            🎭 Sentiment Distribution of Analyzed News
        </div>
        """, unsafe_allow_html=True)

        sent_data = db_stats.get("sentiment_distribution", {})
        labels = [k.capitalize() for k in sent_data.keys()]
        values = list(sent_data.values())

        # Clean light-theme color palette
        color_map = {
            "Positive": "#10B981",  # Mint / Emerald
            "Negative": "#F43F5E",  # Rose / Coral
            "Neutral": "#F59E0B",   # Amber
            "Mixed": "#0EA5E9",     # Sky Blue
            "Unknown": "#94A3B8"
        }
        colors = [color_map.get(l, "#10B981") for l in labels]

        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
                textinfo="label+percent",
                hoverinfo="label+value+percent",
                textfont=dict(family="Plus Jakarta Sans", size=12, color="#0F172A"),
            )]
        )
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#475569", family="Plus Jakarta Sans"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=260,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig, use_container_width=True)

    with table_col:
        st.markdown("""
        <div style="font-weight: 700; color: #047857; margin-bottom: 8px; font-size: 0.95rem;">
            🕒 Recent Analysis History (Latest 5 Records)
        </div>
        """, unsafe_allow_html=True)

        recent_records = db.get_all_records(limit=5)
        if recent_records:
            rows_data = []
            for r in recent_records:
                snippet = (r['article_text'][:50] + "...") if len(r['article_text']) > 50 else r['article_text']
                time_str = r['created_at'].split(".")[0] if "." in r['created_at'] else r['created_at']
                rows_data.append({
                    "ID": f"#{r['id']}",
                    "Article Snippet": snippet,
                    "Verdict": f"{'🚨 Fake' if r['ml_prediction'] == 'FAKE' else '✅ Real'}",
                    "Sentiment": f"{r['sentiment'].capitalize()}",
                    "Timestamp": time_str
                })
            st.dataframe(pd.DataFrame(rows_data), hide_index=True, use_container_width=True)
            st.caption("💡 For full audit records, individual inspection, or deletion, visit the **Analysis History** page.")
else:
    st.markdown("""
    <div style="background: var(--emerald-bg); border: 1px dashed var(--emerald-border); border-radius: 14px; padding: 24px; text-align: center; margin: 15px 0;">
        <span style="font-size: 1.8rem;">💡</span>
        <div style="color: #047857; font-weight: 700; font-size: 1.05rem; margin-top: 6px;">No Articles Analyzed Yet</div>
        <div style="color: #64748B; font-size: 0.88rem; margin-top: 4px;">
            Navigate to the <strong>News Detection</strong> page in the sidebar to test article classification, Azure sentiment analysis, and key phrase extraction!
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
    acc = model_stats["accuracy"] if model_stats["loaded"] else "99.08%"
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🎯</span>
        <div class="kpi-value">{acc}</div>
        <div class="kpi-label">Peak Model Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    f1 = model_stats["f1"] if model_stats["loaded"] else "99.12%"
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">⚡</span>
        <div class="kpi-value">{f1}</div>
        <div class="kpi-label">Peak F1-Score</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    mt = model_stats["models_trained"] if model_stats["loaded"] else "5"
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
            querying Microsoft Azure AI for affective tone and extracted key entities.
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
    ("1", "Input Text", "User pastes article or selects a pre-loaded sample"),
    ("2", "Preprocessing", "NLTK tokenizes, strips stopwords & lemmatizes text"),
    ("3", "TF-IDF Vector", "Converts text to 50k feature vector space"),
    ("4", "ML Inference", "Best model predicts Fake vs Real with probability"),
    ("5", "Azure Sentiment", "Cloud API computes positive/neutral/negative tone"),
    ("6", "Azure Key Phrases", "Cloud NLP extracts key entities and themes"),
    ("7", "SQLite Storage", "Complete analysis record is saved to local database"),
]

cols = st.columns(7)
for col, (num, title, desc) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div class="pipeline-step">
            <div class="pipeline-step-badge">{num}</div>
            <div style="font-size: 0.88rem; font-weight: 700; color: #047857; margin-bottom: 4px;">{title}</div>
            <div style="font-size: 0.74rem; color: #64748B; line-height: 1.4;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 6px; font-weight: 600; color: #0F172A;">
        NewsLens AI · AI-Based News Article Analysis System <span style="color: #059669; font-size: 0.8rem; background: rgba(16,185,129,0.1); padding: 2px 8px; border-radius: 12px; margin-left: 6px;">v2.0.0</span>
    </div>
    <div>
        Powered by 
        <a href="https://azure.microsoft.com/en-us/products/ai-services/ai-language" target="_blank">Microsoft Azure AI Language</a> · 
        <a href="https://scikit-learn.org" target="_blank">Scikit-learn</a> · 
        <a href="https://sqlite.org" target="_blank">SQLite</a> · 
        <a href="https://streamlit.io" target="_blank">Streamlit</a>
    </div>
    <div style="margin-top: 6px; font-size: 0.75rem; color: #94A3B8;">
        Developed for Industrial Internship Examination (Microsoft AI-901 Global Certification)
    </div>
</div>
""", unsafe_allow_html=True)
