"""
AI-Based News Article Analysis - About Project Page
===================================================
Project overview, multi-tier architecture, tech stack,
Azure AI Language integration, and examination specifications.
"""

import streamlit as st

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="About | AI News Analyzer",
    page_icon="ℹ️",
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
.section-header { font-size: 1.5rem; font-weight: 700; color: #e0e0e0;
    margin: 40px 0 20px; padding-bottom: 12px;
    border-bottom: 2px solid rgba(0, 212, 255, 0.2); }
.gradient-divider { height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, #00ff88, transparent);
    border: none; margin: 30px 0; border-radius: 2px; }

/* Tech badges */
.tech-badge {
    display: inline-block; padding: 8px 18px; margin: 5px;
    border-radius: 50px; font-size: 0.82rem; font-weight: 600;
    background: rgba(0, 212, 255, 0.1); color: #00d4ff;
    border: 1px solid rgba(0, 212, 255, 0.3);
    transition: all 0.2s ease;
}
.tech-badge:hover { background: rgba(0, 212, 255, 0.25); transform: scale(1.05); }
.tech-badge-green { background: rgba(0, 255, 136, 0.1); color: #00ff88;
    border-color: rgba(0, 255, 136, 0.3); }
.tech-badge-green:hover { background: rgba(0, 255, 136, 0.25); }
.tech-badge-orange { background: rgba(255, 165, 0, 0.1); color: #ffa500;
    border-color: rgba(255, 165, 0, 0.3); }
.tech-badge-orange:hover { background: rgba(255, 165, 0, 0.25); }
.tech-badge-red { background: rgba(255, 71, 87, 0.1); color: #ff4757;
    border-color: rgba(255, 71, 87, 0.3); }
.tech-badge-red:hover { background: rgba(255, 71, 87, 0.25); }
.tech-badge-purple { background: rgba(168, 85, 247, 0.1); color: #a855f7;
    border-color: rgba(168, 85, 247, 0.3); }
.tech-badge-purple:hover { background: rgba(168, 85, 247, 0.25); }
.tech-badge-azure { background: rgba(0, 120, 212, 0.18); color: #50e6ff;
    border-color: rgba(0, 120, 212, 0.45); }
.tech-badge-azure:hover { background: rgba(0, 120, 212, 0.3); }

/* Info cards */
.info-card {
    background: linear-gradient(135deg, #1e2a3a 0%, #16213e 100%);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 16px; padding: 26px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    margin-bottom: 16px;
}

/* Pipeline steps */
.pipeline-step {
    background: linear-gradient(135deg, #1e2a3a, #16213e);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 16px; padding: 22px; text-align: center;
    position: relative; min-height: 190px;
    display: flex; flex-direction: column; justify-content: center;
    transition: all 0.3s ease;
}
.pipeline-step:hover { border-color: rgba(0, 212, 255, 0.4);
    transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,212,255,0.1); }
.pipeline-num {
    position: absolute; top: -13px; left: 50%; transform: translateX(-50%);
    background: linear-gradient(135deg, #00d4ff, #00ff88);
    color: #0e1117; width: 26px; height: 26px; border-radius: 50%;
    font-size: 0.78rem; font-weight: 800; line-height: 26px;
    text-align: center;
}

/* Model cards */
.model-card {
    background: linear-gradient(135deg, #1e2a3a 0%, #16213e 100%);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 16px; padding: 26px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease; min-height: 300px;
}
.model-card:hover { border-color: rgba(0, 212, 255, 0.35);
    transform: translateY(-4px); box-shadow: 0 8px 28px rgba(0,212,255,0.1); }
</style>
"""

st.markdown(SHARED_CSS, unsafe_allow_html=True)


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <div style="font-size: 3rem;">ℹ️</div>
        <div style="font-size: 1.15rem; font-weight: 700; color: #00d4ff;">About System</div>
        <div style="font-size: 0.72rem; color: #556677; margin-top: 4px; letter-spacing: 1px;">AI-901 INTERNSHIP PROJECT</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 8px 0; color: #8899aa; font-size: 0.82rem; line-height: 1.8;">
        <strong style="color:#e0e0e0;">📑 System Outline</strong><br>
        🏗️ Project Overview<br>
        📐 System Architecture<br>
        🛠️ Technology Stack<br>
        ☁️ Azure AI Integration<br>
        🔄 End-to-End Pipeline<br>
        🤖 ML Classifiers<br>
        🗄️ SQLite Audit Design<br>
        🚀 Future Work
    </div>
    """, unsafe_allow_html=True)


# ─── Page Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 24px 0 10px;">
    <div style="font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #00ff88);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        ℹ️ About the News Article Analysis System
    </div>
    <div style="color: #8899aa; font-size: 1rem; margin-top: 8px;">
        Architecture, Azure AI Cognitive Services, Machine Learning, and SQLite Implementation Details
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ─── Project Overview ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🏗️ Project Overview & Objectives</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <div style="color: #e0e0e0; font-size: 1.05rem; line-height: 1.8;">
        The <strong style="color: #00d4ff;">AI-Based News Article Analysis System Using Microsoft Azure AI</strong> 
        is an advanced multi-faceted intelligence platform developed for the Industrial Internship Examination 
        aligned with the <strong style="color:#50e6ff;">Microsoft AI-901 (Azure AI Fundamentals)</strong> certification.
        <br><br>
        Rather than relying solely on a single metric, this system integrates three complementary layers of AI analysis:
    </div>
    <div style="margin-top: 18px; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px;">
        <div style="background: rgba(0,212,255,0.06); padding: 16px; border-radius: 12px; border: 1px solid rgba(0,212,255,0.2);">
            <div style="font-weight: 700; color: #00d4ff; margin-bottom: 6px;">1. Classical ML Classifier</div>
            <div style="color: #8899aa; font-size: 0.85rem; line-height: 1.6;">
                Trained on 44,000+ verified articles with TF-IDF vectorization to classify news as <strong>Real</strong> or <strong>Fake</strong> with 99.81% accuracy.
            </div>
        </div>
        <div style="background: rgba(0,120,212,0.08); padding: 16px; border-radius: 12px; border: 1px solid rgba(0,120,212,0.3);">
            <div style="font-weight: 700; color: #50e6ff; margin-bottom: 6px;">2. Azure AI Sentiment</div>
            <div style="color: #8899aa; font-size: 0.85rem; line-height: 1.6;">
                Cloud-native emotional tone analysis (Positive, Neutral, Negative) independent of truthfulness to detect emotional charge or sensationalism.
            </div>
        </div>
        <div style="background: rgba(0,255,136,0.06); padding: 16px; border-radius: 12px; border: 1px solid rgba(0,255,136,0.2);">
            <div style="font-weight: 700; color: #00ff88; margin-bottom: 6px;">3. Key Phrase Extraction</div>
            <div style="color: #8899aa; font-size: 0.85rem; line-height: 1.6;">
                Azure AI Language extracts salient thematic terms, entities, and subjects from the article to deliver instant executive summaries.
            </div>
        </div>
    </div>
    <div style="margin-top: 18px; padding-top: 14px; border-top: 1px solid rgba(0,212,255,0.15); color: #8899aa; font-size: 0.9rem;">
        🗄️ <strong>Audit Trail:</strong> Every analysis is persisted in an ACID-compliant local <strong>SQLite database</strong> (<code>news_analysis.db</code>) with full timestamps, JSON-serialized confidence scores, and historical record retrieval.
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Architecture Diagram ───────────────────────────────────────────────────
st.markdown('<div class="section-header">📐 Multi-Tier System Architecture</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(135deg, #1e2a3a, #16213e); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 16px; padding: 26px; text-align: center;">

<div style="display: flex; flex-direction: column; align-items: center; gap: 16px;">

<!-- Input -->
<div style="background: rgba(0, 212, 255, 0.15); border: 2px solid #00d4ff; padding: 12px 40px; border-radius: 10px; color: #ffffff; font-weight: 700; font-size: 1.1rem;">
    📰 Input News Article Text
</div>

<div style="color: #8899aa; font-size: 1.4rem;">⬇ (Parallel Processing Branches)</div>

<!-- Parallel Branches -->
<div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; width: 100%;">

    <!-- Branch A: ML -->
    <div style="flex: 1; min-width: 280px; background: rgba(0, 255, 136, 0.05); border: 1px solid rgba(0,255,136,0.3); border-radius: 12px; padding: 18px;">
        <div style="color: #00ff88; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">🤖 Classical ML Pipeline</div>
        <div style="font-size: 0.82rem; color: #c0cdd8; line-height: 1.6;">
            1. Text cleaning & normalization<br>
            2. NLTK Lemmatization & Stopword removal<br>
            3. TF-IDF Matrix Transformation (50k features)<br>
            4. Inference via Best Model (XGBoost / SVM)<br>
            <strong style="color: #00ff88;">Output: Verdict (FAKE / REAL) + Confidence</strong>
        </div>
    </div>

    <!-- Branch B: Azure AI -->
    <div style="flex: 1; min-width: 280px; background: rgba(0, 120, 212, 0.08); border: 1px solid rgba(0,120,212,0.4); border-radius: 12px; padding: 18px;">
        <div style="color: #50e6ff; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">☁️ Microsoft Azure AI Language</div>
        <div style="font-size: 0.82rem; color: #c0cdd8; line-height: 1.6;">
            1. Authenticate with Azure Cognitive Endpoint<br>
            2. Azure Text Analytics Sentiment API<br>
            3. Azure Key Phrase Extraction API<br>
            4. Truncation & batching guards<br>
            <strong style="color: #50e6ff;">Output: Sentiment Scores + Salient Entities</strong>
        </div>
    </div>

</div>

<div style="color: #8899aa; font-size: 1.4rem;">⬇ (Consolidation & Persistence)</div>

<!-- Storage & UI -->
<div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; width: 100%;">
    <div style="flex: 1; background: rgba(255, 165, 0, 0.1); border: 1px solid #ffa500; border-radius: 10px; padding: 14px; font-weight: 600; color: #ffa500;">
        🗄️ SQLite Database (news_analysis.db)<br>
        <span style="font-size: 0.78rem; color: #8899aa; font-weight: 400;">Parameterized SQL Storage & History Tracking</span>
    </div>
    <div style="flex: 1; background: rgba(0, 212, 255, 0.1); border: 1px solid #00d4ff; border-radius: 10px; padding: 14px; font-weight: 600; color: #00d4ff;">
        📱 Streamlit Dashboard UI<br>
        <span style="font-size: 0.78rem; color: #8899aa; font-weight: 400;">Multi-Page Views, Plotly Visuals, Explainability</span>
    </div>
</div>

</div>
</div>
""", unsafe_allow_html=True)

st.code("""
CodeAlpha_Fake-News-Detection-System/
├── app.py                     # 🏠 Main Dashboard & SQLite live activity summary
├── pages/
│   ├── 1_News_Detection.py    # 🔍 Unified Multi-AI analysis (ML + Azure + DB)
│   ├── 2_Analytics.py         # 📊 Dataset exploration & distributions
│   ├── 3_Model_Performance.py # 📈 Model comparison metrics & ROC curves
│   ├── 4_Explainability.py    # 🧠 Word contribution & feature importance
│   ├── 5_About_Project.py     # ℹ️ System architecture & documentation
│   └── 6_Analysis_History.py  # 📜 SQLite audit records log & management
├── src/
│   ├── __init__.py            # Package initialization (v2.0.0)
│   ├── azure_language.py      # ☁️ Microsoft Azure AI Language client wrapper
│   ├── database.py            # 🗄️ SQLite database manager & parameterized queries
│   ├── preprocessing.py       # NLTK text normalization & cleaning
│   ├── feature_engineering.py # TF-IDF vectorization
│   ├── train.py               # Model training with 5-fold CV & GridSearchCV
│   ├── evaluate.py            # Metrics, confusion matrix, ROC curves
│   └── predict.py             # Inference API wrapper
├── models/                    # Serialized joblib artifacts
├── dataset/                   # Training corpus (Fake.csv, True.csv)
├── reports/                   # Model comparison CSV & evaluation charts
├── news_analysis.db           # Local SQLite database (auto-created)
├── .env.example               # Template for Azure endpoint & key
├── requirements.txt           # Dependencies (azure-ai-textanalytics, etc.)
└── README.md                  # Comprehensive project documentation
""", language="text")


# ─── Tech Stack ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🛠️ Integrated Technology Stack</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card" style="text-align: center;">
    <div style="margin-bottom: 14px; color: #8899aa; font-size: 0.85rem; text-transform: uppercase;
        letter-spacing: 1.5px; font-weight: 600;">Technologies & Cloud Frameworks</div>
    <span class="tech-badge-azure">☁️ Microsoft Azure AI Language</span>
    <span class="tech-badge">🐍 Python 3.10+</span>
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
    <div class="info-card" style="min-height: 250px;">
        <div style="color: #50e6ff; font-size: 1.05rem; font-weight: 700; margin-bottom: 10px;">
            ☁️ Azure AI Language
        </div>
        <div style="color: #8899aa; font-size: 0.84rem; line-height: 1.7;">
            Official <strong>azure-ai-textanalytics</strong> SDK providing cloud-managed Natural Language Processing.<br><br>
            • <strong>Sentiment Analysis:</strong> Computes document-level polarity and confidence scores.<br>
            • <strong>Key Phrase Extraction:</strong> Uncovers essential concepts and entities.<br>
            • <strong>Security:</strong> Credential loading via environment variables (.env).
        </div>
    </div>
    """, unsafe_allow_html=True)

with tc2:
    st.markdown("""
    <div class="info-card" style="min-height: 250px;">
        <div style="color: #00ff88; font-size: 1.05rem; font-weight: 700; margin-bottom: 10px;">
            🤖 ML & Feature Engineering
        </div>
        <div style="color: #8899aa; font-size: 0.84rem; line-height: 1.7;">
            <strong>Scikit-learn, XGBoost & NLTK</strong> powering local offline inference.<br><br>
            • <strong>TF-IDF Vectorizer:</strong> 50k features, sublinear scaling, unigram + bigram.<br>
            • <strong>Best Model:</strong> XGBoost with 99.81% accuracy & calibrated probabilities.<br>
            • <strong>Explainability:</strong> Linear coefficient word attribution.
        </div>
    </div>
    """, unsafe_allow_html=True)

with tc3:
    st.markdown("""
    <div class="info-card" style="min-height: 250px;">
        <div style="color: #ffa500; font-size: 1.05rem; font-weight: 700; margin-bottom: 10px;">
            🗄️ Database & Frontend
        </div>
        <div style="color: #8899aa; font-size: 0.84rem; line-height: 1.7;">
            <strong>SQLite3 & Streamlit</strong> delivering reliable storage and modern UI.<br><br>
            • <strong>SQLite:</strong> Parameterized queries, JSON storage for complex structures, zero-config file DB.<br>
            • <strong>Streamlit:</strong> Multi-page interactive UI with Plotly charts and real-time state management.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── ML Pipeline ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔄 Complete 7-Stage Analysis Pipeline</div>', unsafe_allow_html=True)

pipeline_steps = [
    ("1", "📥 Article Input", "User supplies raw news text via direct paste or one-click sample selectors."),
    ("2", "🧹 NLTK Cleaning", "Text undergoes lowercasing, punctuation stripping, stopword removal, and lemmatization."),
    ("3", "🔢 TF-IDF Transformation", "Cleaned text is projected into 50,000-dimensional numerical TF-IDF space."),
    ("4", "🤖 ML Classification", "Best trained classifier (XGBoost / SVM) calculates Fake vs Real probability."),
    ("5", "🎭 Azure Sentiment", "Azure Language evaluates emotional tone (Positive, Neutral, Negative) and confidence."),
    ("6", "🔑 Azure Key Phrases", "Azure Language extracts salient thematic terms and entities from the text."),
    ("7", "🗄️ SQLite Persistence", "Full analysis bundle is saved to news_analysis.db with timestamp and audit metadata."),
]

p_cols = st.columns(4)
for idx, (num, title, desc) in enumerate(pipeline_steps[:4]):
    with p_cols[idx]:
        st.markdown(f"""
        <div class="pipeline-step">
            <div class="pipeline-num">{num}</div>
            <div style="font-size: 0.95rem; font-weight: 700; color: #00d4ff; margin-bottom: 6px;">{title}</div>
            <div style="color: #8899aa; font-size: 0.8rem; line-height: 1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

p_cols2 = st.columns(3)
for idx, (num, title, desc) in enumerate(pipeline_steps[4:]):
    with p_cols2[idx]:
        st.markdown(f"""
        <div class="pipeline-step">
            <div class="pipeline-num">{num}</div>
            <div style="font-size: 0.95rem; font-weight: 700; color: #50e6ff; margin-bottom: 6px;">{title}</div>
            <div style="color: #8899aa; font-size: 0.8rem; line-height: 1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ─── Model Descriptions ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">🤖 Machine Learning Classifiers Evaluated</div>', unsafe_allow_html=True)

models = [
    {
        "name": "Logistic Regression",
        "icon": "📐",
        "color": "#00d4ff",
        "desc": "A linear model applying the sigmoid function to feature combinations. Highly effective and interpretable for sparse TF-IDF spaces.",
        "pros": ["Direct word importance via coefficients", "Extremely fast inference", "Strong baseline on text"],
        "cons": ["Linear decision boundary only"],
    },
    {
        "name": "Multinomial Naive Bayes",
        "icon": "📊",
        "color": "#00ff88",
        "desc": "Probabilistic model based on Bayes' Theorem with feature independence assumptions. Naturally suited to text term frequencies.",
        "pros": ["Minimal training time", "Zero hyperparameter sensitivity", "Strong with small samples"],
        "cons": ["Feature independence assumption is violated in natural prose"],
    },
    {
        "name": "Linear SVC",
        "icon": "🎯",
        "color": "#ffa500",
        "desc": "Maximum-margin hyperplane classifier. Maximizes margin between fake and real news vectors with L2 regularization.",
        "pros": ["Exceptional generalization on high-dimensional text", "Memory efficient"],
        "cons": ["Requires calibration (CalibratedClassifierCV) for probability output"],
    },
    {
        "name": "XGBoost Classifier",
        "icon": "🚀",
        "color": "#a855f7",
        "desc": "Gradient boosted decision tree ensemble. Combines sequential weak learners with shrinkage and regularization.",
        "pros": ["Captures non-linear interactions", "Highest benchmark accuracy (99.81%)", "Resilient to noise"],
        "cons": ["Higher computational cost during training"],
    },
]

model_cols = st.columns(2)
for i, m in enumerate(models):
    with model_cols[i % 2]:
        pros_html = "".join(f'<div style="color:#00ff88; font-size:0.8rem; margin:2px 0;">✅ {p}</div>' for p in m["pros"])
        cons_html = "".join(f'<div style="color:#ff4757; font-size:0.8rem; margin:2px 0;">⚠️ {c}</div>' for c in m["cons"])

        st.markdown(f"""
        <div class="model-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                <span style="font-size: 1.8rem;">{m['icon']}</span>
                <span style="font-size: 1.15rem; font-weight: 700; color: {m['color']};">{m['name']}</span>
            </div>
            <div style="color: #8899aa; font-size: 0.85rem; line-height: 1.6; margin-bottom: 14px;">
                {m['desc']}
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <div style="color: #556677; font-size: 0.72rem; text-transform: uppercase; font-weight: 600;">Advantages</div>
                    {pros_html}
                </div>
                <div>
                    <div style="color: #556677; font-size: 0.72rem; text-transform: uppercase; font-weight: 600;">Trade-offs</div>
                    {cons_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─── Quick Setup Instructions ───────────────────────────────────────────────
st.markdown('<div class="section-header">⚡ Installation & Configuration Guide</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <div style="color: #00d4ff; font-size: 1.05rem; font-weight: 700; margin-bottom: 12px;">
        🚀 Execution Steps
    </div>
    <div style="color: #8899aa; font-size: 0.88rem; line-height: 1.9;">
        <strong>1. Install Requirements:</strong><br>
        <code>pip install -r requirements.txt</code><br><br>
        <strong>2. Configure Azure AI Credentials:</strong><br>
        Create a <code>.env</code> file in the project root based on <code>.env.example</code>:<br>
        <code>AZURE_LANGUAGE_ENDPOINT=https://&lt;your-resource&gt;.cognitiveservices.azure.com/</code><br>
        <code>AZURE_LANGUAGE_KEY=&lt;your-azure-key&gt;</code><br>
        <em>Note: The system works gracefully in offline mode if credentials are absent.</em><br><br>
        <strong>3. Launch Streamlit Application:</strong><br>
        <code>streamlit run app.py</code>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Author & Certification ──────────────────────────────────────────────────
st.markdown('<div class="section-header">👤 Project Details & Examination Metadata</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card" style="text-align: center;">
    <div style="font-size: 2.8rem; margin-bottom: 8px;">🎓</div>
    <div style="font-size: 1.25rem; font-weight: 700; color: #e0e0e0; margin-bottom: 4px;">
        Hitesh Chugh
    </div>
    <div style="color: #00d4ff; font-size: 0.9rem; font-weight: 600; margin-bottom: 4px;">
        Industrial Internship Examination Project
    </div>
    <div style="color: #8899aa; font-size: 0.82rem; margin-bottom: 18px;">
        Curriculum aligned with Microsoft Certified: Azure AI Fundamentals (AI-901)
    </div>
    <div style="display: flex; justify-content: center; gap: 14px; flex-wrap: wrap;">
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
<div style="text-align: center; padding: 40px 20px 20px; margin-top: 50px;
    border-top: 1px solid rgba(0, 212, 255, 0.1);">
    <div style="color: #556677; font-size: 0.85rem; margin-bottom: 8px;">
        <span style="color: #00d4ff;">📰 AI-Based News Article Analysis System</span> · <span style="color: #00ff88;">v2.0.0</span>
    </div>
    <div style="color: #445566; font-size: 0.75rem;">
        Microsoft Azure AI · Scikit-learn · Streamlit · SQLite
    </div>
</div>
""", unsafe_allow_html=True)
