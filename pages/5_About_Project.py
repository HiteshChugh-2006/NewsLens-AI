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
                Trained on 44,898 verified articles with TF-IDF vectorization to classify news as <strong>Real</strong> or <strong>Fake</strong> with 99.81% accuracy.
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

st.markdown("""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 26px; text-align: center; box-shadow: 0 2px 8px rgba(15,23,42,0.03);">

<div style="display: flex; flex-direction: column; align-items: center; gap: 14px;">

<!-- Input -->
<div style="background: rgba(16, 185, 129, 0.1); border: 2px solid #059669; padding: 12px 36px; border-radius: 12px; color: #047857; font-weight: 800; font-size: 1.05rem;">
    📰 Input News Article Text
</div>

<div style="color: #94A3B8; font-size: 1.2rem; font-weight: 700;">⬇ Parallel Processing Branches</div>

<!-- Parallel Branches -->
<div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; width: 100%;">

    <!-- Branch A: ML -->
    <div style="flex: 1; min-width: 280px; background: rgba(16, 185, 129, 0.04); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 16px;">
        <div style="color: #047857; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">🤖 Classical ML Pipeline</div>
        <div style="font-size: 0.82rem; color: #475569; line-height: 1.55;">
            1. Text cleaning & normalization<br>
            2. NLTK Lemmatization & Stopwords<br>
            3. TF-IDF Matrix (50,000 features)<br>
            4. Inference via Best Model (XGBoost)<br>
            <strong style="color: #047857;">Output: FAKE / REAL + Confidence</strong>
        </div>
    </div>

    <!-- Branch B: Azure AI -->
    <div style="flex: 1; min-width: 280px; background: rgba(0, 120, 212, 0.04); border: 1px solid rgba(0, 120, 212, 0.25); border-radius: 12px; padding: 16px;">
        <div style="color: #0078D4; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">☁️ Microsoft Azure AI Language</div>
        <div style="font-size: 0.82rem; color: #475569; line-height: 1.55;">
            1. Authenticate with Cognitive Endpoint<br>
            2. Sentiment Analysis API<br>
            3. Key Phrase Extraction API<br>
            4. Truncation & batch guards<br>
            <strong style="color: #0078D4;">Output: Sentiment Scores + Salient Tags</strong>
        </div>
    </div>

</div>

<div style="color: #94A3B8; font-size: 1.2rem; font-weight: 700;">⬇ Persistence & Interface</div>

<!-- Storage & UI -->
<div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; width: 100%;">
    <div style="flex: 1; background: rgba(217, 119, 6, 0.06); border: 1px solid rgba(217, 119, 6, 0.3); border-radius: 10px; padding: 12px; font-weight: 600; color: #D97706;">
        🗄️ SQLite Database (news_analysis.db)<br>
        <span style="font-size: 0.75rem; color: #64748B; font-weight: 400;">Parameterized SQL Storage & History Tracking</span>
    </div>
    <div style="flex: 1; background: rgba(5, 150, 105, 0.06); border: 1px solid rgba(5, 150, 105, 0.3); border-radius: 10px; padding: 12px; font-weight: 600; color: #047857;">
        📱 Streamlit Dashboard UI<br>
        <span style="font-size: 0.75rem; color: #64748B; font-weight: 400;">Microsoft Fluent Layouts, Plotly Visuals, Explainability</span>
    </div>
</div>

</div>
</div>
""", unsafe_allow_html=True)


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
            • <strong>TF-IDF Vectorizer:</strong> 50,000 unigram/bigram features.<br>
            • <strong>Champion Model:</strong> XGBoost with 99.81% accuracy & calibrated probabilities.<br>
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
        "name": "Logistic Regression",
        "icon": "📐",
        "color": "#047857",
        "desc": "Linear model applying the sigmoid function. Highly interpretable for sparse TF-IDF spaces with fast inference.",
        "pros": ["Direct word coefficients", "Fast training and inference", "Resilient to noise"],
        "cons": ["Linear decision boundary only"],
    },
    {
        "name": "Multinomial Naive Bayes",
        "icon": "📊",
        "color": "#0D9488",
        "desc": "Probabilistic model based on Bayes' Theorem. Suited for word frequencies and text counts.",
        "pros": ["Minimal training time", "Strong NLP baseline", "No hyperparameter sensitivity"],
        "cons": ["Violates word independence in natural text"],
    },
    {
        "name": "Linear SVC",
        "icon": "🎯",
        "color": "#0078D4",
        "desc": "Support Vector Machine with linear kernel that finds maximum-margin hyperplane separating classes.",
        "pros": ["Strong generalization on text", "Memory efficient (uses support vectors)"],
        "cons": ["Requires CalibratedClassifierCV for probabilities"],
    },
    {
        "name": "XGBoost Classifier (Best)",
        "icon": "🚀",
        "color": "#059669",
        "desc": "Gradient boosted decision trees sequentially minimizing residual errors. Top performer on benchmark.",
        "pros": ["Captures non-linear relationships", "Peak 99.81% accuracy", "Built-in regularization"],
        "cons": ["Higher training compute cost"],
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
