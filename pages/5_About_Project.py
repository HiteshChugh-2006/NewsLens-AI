"""
NewsLens AI - About System & Architecture
=========================================
Project overview, multi-tier architecture, tech stack,
Azure AI Language integration, and examination specifications.
"""

import streamlit as st
import os
import sys

# ─── Add project root to path ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.styles import get_custom_css

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="About | NewsLens AI",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Microsoft Fluent Light Theme CSS ────────────────────────────────────────
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">ℹ️</div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #047857;">
            NewsLens AI
        </div>
        <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">
            System Documentation
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Page Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 16px 0 8px;">
    <div style="font-size: 2.4rem; font-weight: 800;
        background: linear-gradient(135deg, #065F46 0%, #059669 50%, #0D9488 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        ℹ️ About NewsLens AI
    </div>
    <div style="color: #64748B; font-size: 1rem; margin-top: 6px;">
        Architecture, Microsoft Azure AI Cognitive Services, Machine Learning, and SQLite Implementation Details
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ─── Project Overview ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🏗️ Project Overview & Objectives</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <div style="color: #0F172A; font-size: 1.05rem; line-height: 1.75;">
        <strong style="color: #047857;">NewsLens AI</strong> is an enterprise-grade news article analysis platform 
        developed for the Industrial Internship Examination aligned with the 
        <strong style="color: #0078D4;">Microsoft Certified: Azure AI Fundamentals (AI-901)</strong> global curriculum.
        <br><br>
        The platform unifies three complementary dimensions of automated content evaluation:
    </div>
    <div style="margin-top: 18px; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px;">
        <div style="background: rgba(16, 185, 129, 0.06); padding: 16px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.25);">
            <div style="font-weight: 700; color: #047857; margin-bottom: 6px;">1. Classical ML Classifier</div>
            <div style="color: #64748B; font-size: 0.84rem; line-height: 1.55;">
                Trained on 44,898 verified articles with TF-IDF vectorization to classify news as <strong>Real</strong> or <strong>Fake</strong> with 99.08% peak accuracy.
            </div>
        </div>
        <div style="background: rgba(0, 120, 212, 0.06); padding: 16px; border-radius: 12px; border: 1px solid rgba(0, 120, 212, 0.25);">
            <div style="font-weight: 700; color: #0078D4; margin-bottom: 6px;">2. Azure AI Sentiment</div>
            <div style="color: #64748B; font-size: 0.84rem; line-height: 1.55;">
                Cloud-native emotional tone analysis (Positive, Neutral, Negative) independent of truthfulness to detect emotional charge or sensationalism.
            </div>
        </div>
        <div style="background: rgba(217, 119, 6, 0.06); padding: 16px; border-radius: 12px; border: 1px solid rgba(217, 119, 6, 0.25);">
            <div style="font-weight: 700; color: #D97706; margin-bottom: 6px;">3. Key Phrase Extraction</div>
            <div style="color: #64748B; font-size: 0.84rem; line-height: 1.55;">
                Azure AI Language extracts salient thematic terms, entities, and subjects from the article to deliver instant executive summaries.
            </div>
        </div>
    </div>
    <div style="margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--border-light); color: #64748B; font-size: 0.88rem;">
        🗄️ <strong>Auditable Record Keeping:</strong> Every analysis is committed to an ACID-compliant local <strong>SQLite database</strong> (<code>news_analysis.db</code>) with full timestamps, JSON-serialized confidence scores, and historical record retrieval.
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Architecture Diagram ───────────────────────────────────────────────────
st.markdown('<div class="section-header">📐 Multi-Tier System Architecture</div>', unsafe_allow_html=True)

# Top Box: Input Article
st.markdown(
    '<div style="background: rgba(16, 185, 129, 0.1); border: 2px solid #059669; '
    'padding: 14px 24px; border-radius: 12px; color: #047857; font-weight: 800; '
    'font-size: 1.05rem; text-align: center; margin-bottom: 14px; box-shadow: 0 2px 6px rgba(5,150,105,0.08);">'
    '📰 Raw Input News Article'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div style="text-align: center; color: #94A3B8; font-size: 1.15rem; font-weight: 700; margin: 4px 0 14px;">'
    '⬇ Dual Parallel Processing Branches ⬇'
    '</div>',
    unsafe_allow_html=True
)

arch_col1, arch_col2 = st.columns(2)
with arch_col1:
    st.markdown(
        '<div style="background: #FFFFFF; border: 1.5px solid rgba(16, 185, 129, 0.35); '
        'border-radius: 14px; padding: 18px 20px; min-height: 195px; box-shadow: 0 2px 8px rgba(15,23,42,0.04);">'
        '<div style="color: #047857; font-weight: 800; font-size: 1.02rem; margin-bottom: 8px;">'
        '🤖 Branch A: Classical Machine Learning'
        '</div>'
        '<div style="font-size: 0.84rem; color: #475569; line-height: 1.65;">'
        '1. <strong>Preprocessing:</strong> Text cleaning, lowercasing & lemmatization<br>'
        '2. <strong>Vectorization:</strong> TF-IDF matrix (40,000 sublinear features)<br>'
        '3. <strong>Inference:</strong> LinearSVC / Soft Voting Ensemble<br>'
        '<span style="display: inline-block; margin-top: 8px; padding: 4px 10px; background: rgba(16,185,129,0.12); color: #047857; font-weight: 700; border-radius: 6px; font-size: 0.8rem;">'
        'Output: FAKE / REAL Classification + Calibrated Confidence'
        '</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

with arch_col2:
    st.markdown(
        '<div style="background: #FFFFFF; border: 1.5px solid rgba(0, 120, 212, 0.35); '
        'border-radius: 14px; padding: 18px 20px; min-height: 195px; box-shadow: 0 2px 8px rgba(15,23,42,0.04);">'
        '<div style="color: #0078D4; font-weight: 800; font-size: 1.02rem; margin-bottom: 8px;">'
        '☁️ Branch B: Microsoft Azure AI Language'
        '</div>'
        '<div style="font-size: 0.84rem; color: #475569; line-height: 1.65;">'
        '1. <strong>Authentication:</strong> Azure Cognitive Endpoint & Secret Key<br>'
        '2. <strong>Sentiment API:</strong> Document-level tone (Pos / Neu / Neg)<br>'
        '3. <strong>Key Phrase API:</strong> Salient entity & thematic phrase extraction<br>'
        '<span style="display: inline-block; margin-top: 8px; padding: 4px 10px; background: rgba(0,120,212,0.12); color: #0078D4; font-weight: 700; border-radius: 6px; font-size: 0.8rem;">'
        'Output: Emotional Tone Scores + Salient Thematic Tags'
        '</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown(
    '<div style="text-align: center; color: #94A3B8; font-size: 1.15rem; font-weight: 700; margin: 14px 0 14px;">'
    '⬇ Persistence & User Interface ⬇'
    '</div>',
    unsafe_allow_html=True
)

arch_col3, arch_col4 = st.columns(2)
with arch_col3:
    st.markdown(
        '<div style="background: #FFFFFF; border: 1.5px solid rgba(217, 119, 6, 0.35); '
        'border-radius: 14px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(15,23,42,0.04);">'
        '<div style="color: #D97706; font-weight: 800; font-size: 0.98rem; margin-bottom: 6px;">'
        '🗄️ SQLite Database (news_analysis.db)'
        '</div>'
        '<div style="font-size: 0.82rem; color: #64748B; line-height: 1.5;">'
        'Parameterized SQL storage, audit logging, multi-metric serialization, and full historical retrieval.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

with arch_col4:
    st.markdown(
        '<div style="background: #FFFFFF; border: 1.5px solid rgba(5, 150, 105, 0.35); '
        'border-radius: 14px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(15,23,42,0.04);">'
        '<div style="color: #047857; font-weight: 800; font-size: 0.98rem; margin-bottom: 6px;">'
        '📱 Streamlit Dashboard UI'
        '</div>'
        '<div style="font-size: 0.82rem; color: #64748B; line-height: 1.5;">'
        'Microsoft Fluent styling, responsive Plotly charts, NLTK explainability, and multi-page routing.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ─── Tech Stack ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🛠️ Technology Stack</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card" style="text-align: center;">
    <div style="margin-bottom: 12px; color: #64748B; font-size: 0.8rem; text-transform: uppercase;
        letter-spacing: 1.2px; font-weight: 700;">Enterprise Frameworks & Cloud Services</div>
    <span class="tech-badge-azure">☁️ Microsoft Azure AI Language</span>
    <span class="tech-badge">🐍 Python 3.11</span>
    <span class="tech-badge-green">📊 Scikit-learn</span>
    <span class="tech-badge-orange">🚀 XGBoost</span>
    <span class="tech-badge-red">📱 Streamlit</span>
    <span class="tech-badge-purple">🗄️ SQLite3</span>
    <span class="tech-badge">📈 Plotly</span>
    <span class="tech-badge-green">📝 NLTK</span>
    <span class="tech-badge-orange">🐼 Pandas</span>
    <span class="tech-badge-red">💾 Joblib</span>
</div>
""", unsafe_allow_html=True)

tc1, tc2, tc3 = st.columns(3)

with tc1:
    st.markdown("""
    <div class="info-card" style="min-height: 230px;">
        <div style="color: #0078D4; font-size: 1rem; font-weight: 700; margin-bottom: 8px;">
            ☁️ Azure AI Language
        </div>
        <div style="color: #64748B; font-size: 0.83rem; line-height: 1.65;">
            Official <strong>azure-ai-textanalytics</strong> SDK providing cloud NLP services.<br><br>
            • <strong>Sentiment Scoring:</strong> Three-way probability distribution (positive, neutral, negative).<br>
            • <strong>Key Phrases:</strong> Automated entity & topic discovery.<br>
            • <strong>Security:</strong> Protected credentials loaded via <code>.env</code>.
        </div>
    </div>
    """, unsafe_allow_html=True)

with tc2:
    st.markdown("""
    <div class="info-card" style="min-height: 230px;">
        <div style="color: #047857; font-size: 1rem; font-weight: 700; margin-bottom: 8px;">
            🤖 ML & Feature Pipeline
        </div>
        <div style="color: #64748B; font-size: 0.83rem; line-height: 1.65;">
            <strong>Scikit-learn, XGBoost & NLTK</strong> powering local offline inference.<br><br>
            • <strong>TF-IDF Vectorizer:</strong> 40,000 sublinear unigram/bigram features with domain debiasing.<br>
            • <strong>Champion Model:</strong> LinearSVC (99.08% Accuracy, 0.9993 ROC-AUC) & Soft Voting Ensemble.<br>
            • <strong>Explainability:</strong> Linear coefficient word attribution.
        </div>
    </div>
    """, unsafe_allow_html=True)

with tc3:
    st.markdown("""
    <div class="info-card" style="min-height: 230px;">
        <div style="color: #D97706; font-size: 1rem; font-weight: 700; margin-bottom: 8px;">
            🗄️ Database & Interface
        </div>
        <div style="color: #64748B; font-size: 0.83rem; line-height: 1.65;">
            <strong>SQLite3 & Streamlit</strong> delivering reliable storage and modern UI.<br><br>
            • <strong>SQLite:</strong> Parameterized SQL, zero-configuration local database.<br>
            • <strong>Streamlit:</strong> Multi-page architecture with Microsoft Fluent design and Plotly charts.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Model Descriptions ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">🤖 Evaluated Machine Learning Classifiers</div>', unsafe_allow_html=True)

models = [
    {
        "name": "Linear SVC (Champion)",
        "icon": "🎯",
        "color": "#059669",
        "desc": "Support Vector Classifier with linear kernel, optimized C=0.8, and CalibratedClassifierCV probability mapping. Peak performer on debiased corpus.",
        "pros": ["Peak 99.08% Test Accuracy", "0.9993 ROC-AUC score", "Excellent generalization without publisher leakage"],
        "cons": ["Requires CalibratedClassifierCV for probability estimation"],
    },
    {
        "name": "Logistic Regression",
        "icon": "📐",
        "color": "#047857",
        "desc": "Linear model applying the sigmoid function with L2 regularization. Highly interpretable for sparse TF-IDF spaces with fast inference.",
        "pros": ["98.49% Test Accuracy", "Direct word coefficient explainability", "Sub-millisecond inference time"],
        "cons": ["Linear decision boundary only"],
    },
    {
        "name": "Soft Voting Ensemble",
        "icon": "🤝",
        "color": "#0078D4",
        "desc": "Meta-estimator aggregating calibrated probabilities across LinearSVC, Logistic Regression, and Multinomial Naive Bayes.",
        "pros": ["98.42% Test Accuracy", "Reduced prediction variance", "Robust consensus across diverse algorithms"],
        "cons": ["Requires multiple model evaluations per inference"],
    },
    {
        "name": "XGBoost Classifier",
        "icon": "🚀",
        "color": "#D97706",
        "desc": "Gradient boosted decision trees sequentially minimizing residual errors with histogram-based tree building.",
        "pros": ["95.53% Test Accuracy", "Captures non-linear feature interactions", "Built-in tree regularization"],
        "cons": ["Higher CPU memory footprint during training"],
    },
    {
        "name": "Multinomial Naive Bayes",
        "icon": "📊",
        "color": "#0D9488",
        "desc": "Probabilistic model based on Bayes' Theorem with Dirichlet prior smoothing. Serves as our strong NLP baseline.",
        "pros": ["95.12% Test Accuracy", "Minimal compute overhead", "No hyperparameter sensitivity"],
        "cons": ["Assumes conditional independence between word tokens"],
    },
]

model_cols = st.columns(2)
for i, m in enumerate(models):
    with model_cols[i % 2]:
        pros_html = "".join(f'<div style="color:#059669; font-size:0.8rem; margin:2px 0;">✅ {p}</div>' for p in m["pros"])
        cons_html = "".join(f'<div style="color:#E11D48; font-size:0.8rem; margin:2px 0;">⚠️ {c}</div>' for c in m["cons"])

        st.markdown(f"""
        <div class="model-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size: 1.6rem;">{m['icon']}</span>
                <span style="font-size: 1.1rem; font-weight: 700; color: {m['color']};">{m['name']}</span>
            </div>
            <div style="color: #64748B; font-size: 0.84rem; line-height: 1.55; margin-bottom: 12px;">
                {m['desc']}
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <div style="color: #94A3B8; font-size: 0.72rem; text-transform: uppercase; font-weight: 700;">Advantages</div>
                    {pros_html}
                </div>
                <div>
                    <div style="color: #94A3B8; font-size: 0.72rem; text-transform: uppercase; font-weight: 700;">Trade-offs</div>
                    {cons_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─── Author & Certification Metadata ─────────────────────────────────────────
st.markdown('<div class="section-header">👤 Academic Context & Author</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card" style="text-align: center;">
    <div style="font-size: 2.6rem; margin-bottom: 6px;">🎓</div>
    <div style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-bottom: 2px;">
        Hitesh Chugh
    </div>
    <div style="color: #047857; font-size: 0.88rem; font-weight: 700; margin-bottom: 4px;">
        Industrial Internship Examination Project
    </div>
    <div style="color: #64748B; font-size: 0.82rem; margin-bottom: 16px;">
        Curriculum aligned with Microsoft Certified: Azure AI Fundamentals (AI-901)
    </div>
    <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
        <a href="https://github.com/HiteshChugh-2006/CodeAlpha_Fake-News-Detection-System" target="_blank" style="text-decoration: none;">
            <span class="tech-badge">🐙 GitHub Repository</span>
        </a>
        <a href="https://www.linkedin.com/in/hitesh-chugh-a80170320/" target="_blank" style="text-decoration: none;">
            <span class="tech-badge tech-badge-green">💼 LinkedIn Profile</span>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 4px; font-weight: 600; color: #0F172A;">
        NewsLens AI · System Architecture & Documentation
    </div>
    <div style="font-size: 0.75rem; color: #94A3B8;">
        Microsoft Azure AI Language · Scikit-learn · Streamlit · SQLite
    </div>
</div>
""", unsafe_allow_html=True)
