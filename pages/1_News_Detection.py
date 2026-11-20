"""
AI-Based News Article Analysis - Real-Time Analysis Page
=========================================================
Analyze any news article with:
  - ML-powered Fake/Real classification
  - Azure AI Language sentiment analysis
  - Azure AI Key Phrase extraction
  - Automatic SQLite history saving
"""

import streamlit as st
import plotly.graph_objects as go
import os
import sys
import random

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analyze News | AI News Analyzer",
    page_icon="🔍",
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
    border-radius: 16px; padding: 28px 24px; text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.05);
    position: relative; overflow: hidden;
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #00d4ff, #00ff88); border-radius: 16px 16px 0 0;
}
.kpi-value { font-size: 2.4rem; font-weight: 800;
    background: linear-gradient(135deg, #00d4ff, #00ff88);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.kpi-label { font-size: 0.85rem; color: #8899aa; text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 600; margin-top: 4px; }
.section-header { font-size: 1.5rem; font-weight: 700; color: #e0e0e0;
    margin: 40px 0 20px; padding-bottom: 12px;
    border-bottom: 2px solid rgba(0, 212, 255, 0.2); }
.gradient-divider { height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, #00ff88, transparent);
    border: none; margin: 30px 0; border-radius: 2px; }

/* Prediction badges */
.prediction-badge {
    display: inline-flex; align-items: center; gap: 12px;
    padding: 20px 40px; border-radius: 16px; font-size: 2rem; font-weight: 800;
    letter-spacing: 2px; text-transform: uppercase;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.fake-badge {
    background: linear-gradient(135deg, #ff4757, #ff6b81);
    color: #fff; border: 2px solid rgba(255,71,87,0.5);
    box-shadow: 0 8px 32px rgba(255,71,87,0.3);
}
.real-badge {
    background: linear-gradient(135deg, #00ff88, #00d4ff);
    color: #0e1117; border: 2px solid rgba(0,255,136,0.5);
    box-shadow: 0 8px 32px rgba(0,255,136,0.3);
}

/* Word tags */
.word-tag {
    display: inline-block; padding: 6px 16px; margin: 4px;
    border-radius: 50px; font-size: 0.85rem; font-weight: 600;
    background: rgba(0, 212, 255, 0.12); color: #00d4ff;
    border: 1px solid rgba(0, 212, 255, 0.3);
    transition: all 0.2s ease;
}
.word-tag:hover { background: rgba(0, 212, 255, 0.25); transform: scale(1.05); }
.word-tag-fake {
    background: rgba(255, 71, 87, 0.12); color: #ff4757;
    border-color: rgba(255, 71, 87, 0.3);
}
.word-tag-real {
    background: rgba(0, 255, 136, 0.12); color: #00ff88;
    border-color: rgba(0, 255, 136, 0.3);
}

/* Sentiment colours */
.sentiment-positive { color: #00ff88; }
.sentiment-negative { color: #ff4757; }
.sentiment-neutral { color: #ffa500; }
.sentiment-mixed { color: #a855f7; }

/* Key phrase tags */
.keyphrase-tag {
    display: inline-block; padding: 8px 18px; margin: 4px;
    border-radius: 50px; font-size: 0.88rem; font-weight: 600;
    background: rgba(168, 85, 247, 0.12); color: #a855f7;
    border: 1px solid rgba(168, 85, 247, 0.3);
    transition: all 0.2s ease;
}
.keyphrase-tag:hover { background: rgba(168, 85, 247, 0.25); transform: scale(1.05); }

/* Result card */
.result-card {
    background: linear-gradient(135deg, #1e2a3a 0%, #16213e 100%);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 20px; padding: 40px; text-align: center;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

/* Azure status badge */
.azure-status {
    display: inline-block; padding: 6px 16px; border-radius: 50px;
    font-size: 0.8rem; font-weight: 600; letter-spacing: 0.5px;
}
.azure-connected { background: rgba(0,255,136,0.12); color: #00ff88;
    border: 1px solid rgba(0,255,136,0.3); }
.azure-disconnected { background: rgba(255,165,0,0.12); color: #ffa500;
    border: 1px solid rgba(255,165,0,0.3); }
</style>
"""

st.markdown(SHARED_CSS, unsafe_allow_html=True)

# ─── Add project root to path ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ─── Load ML Model ──────────────────────────────────────────────────────────
@st.cache_resource
def load_predictor():
    """Load the NewsPredictor with trained model."""
    try:
        from src.predict import NewsPredictor
        model_dir = os.path.join(BASE_DIR, "models")
        model_path = os.path.join(model_dir, "best_model.joblib")
        vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.joblib")
        predictor = NewsPredictor(model_path=model_path, vectorizer_path=vectorizer_path)
        return predictor, None
    except Exception as e:
        return None, str(e)


@st.cache_resource
def load_azure_analyzer():
    """Load the Azure Language Analyzer."""
    try:
        from src.azure_language import AzureLanguageAnalyzer
        analyzer = AzureLanguageAnalyzer()
        return analyzer
    except Exception as e:
        return None


@st.cache_resource
def load_database():
    """Load the analysis database."""
    try:
        from src.database import AnalysisDatabase
        db = AnalysisDatabase()
        return db
    except Exception:
        return None


# ─── Sample Articles ────────────────────────────────────────────────────────
SAMPLE_ARTICLES = {
    "🟢 Real News Example": [
        "WASHINGTON (Reuters) - The Federal Reserve announced on Wednesday that it would raise interest rates "
        "by 0.25 percentage points, citing persistent inflation concerns. Fed Chair Jerome "
        "Powell stated during the press conference that the central bank remains committed "
        "to achieving its 2% inflation target. Markets reacted with modest gains as "
        "investors had largely anticipated the move.",

        "LONDON (Reuters) - Global markets rallied on Friday following a strong jobs report "
        "from the United States. European indices closed up by more than 1.5%, led by "
        "technology and healthcare sectors. Analysts say the positive sentiment could "
        "continue into next week depending on upcoming corporate earnings calls.",

        "NEW YORK (Reuters) - The city council voted unanimously to approve the new "
        "infrastructure spending package. The $4 billion initiative will focus on repairing "
        "aging bridges, upgrading the public transit system, and expanding broadband access "
        "in underserved communities. Construction is slated to begin early next year."
    ],
    "🔴 Fake News Example": [
        "BREAKING: Scientists at a secret underground lab have discovered that drinking "
        "bleach can cure all known diseases! The government has been hiding this miracle "
        "cure for decades to protect Big Pharma profits. Share this before they delete it! "
        "Thousands of doctors have been silenced for trying to reveal the truth. Wake up!",

        "SHOCKING: The President was caught on hot mic admitting that the earth is actually "
        "flat! Insiders say that NASA has been faking satellite images for years to keep "
        "the public completely blind. Read the leaked documents here before the deep state "
        "takes this page offline. You won't believe what else they're hiding!",

        "EXCLUSIVE: Top politicians are secretly using taxpayer money to build luxury "
        "bunkers on Mars! A whistleblower who recently escaped from a top-secret facility "
        "provided us with blurry photos of the spaceships. The mainstream media is completely "
        "ignoring this massive story because they are in on the conspiracy."
    ],
    "🟡 Ambiguous Example": [
        "A new study published online claims that a popular vitamin supplement may have "
        "unexpected health benefits that doctors don't want you to know about. The research, "
        "which has not been peer-reviewed, suggests that taking high doses could reverse "
        "aging. Several wellness influencers have already started promoting the findings.",
    ],
}


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <div style="font-size: 3rem;">🔍</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #00d4ff;">Analyze News</div>
        <div style="font-size: 0.75rem; color: #556677; margin-top: 4px;">AI-POWERED ANALYSIS</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Azure status indicator
    azure_analyzer = load_azure_analyzer()
    if azure_analyzer and azure_analyzer.is_configured:
        st.markdown("""
        <div style="text-align:center; margin-bottom: 16px;">
            <span class="azure-status azure-connected">☁️ Azure AI Connected</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; margin-bottom: 16px;">
            <span class="azure-status azure-disconnected">☁️ Azure AI Not Configured</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 8px 0; color: #8899aa; font-size: 0.82rem; line-height: 1.8;">
        <strong style="color:#e0e0e0;">💡 Tips</strong><br>
        • Paste a complete article for best results<br>
        • Longer texts give more reliable predictions<br>
        • Sentiment ≠ Fake/Real (independent analyses)<br>
        • Check the confidence score
    </div>
    """, unsafe_allow_html=True)


# ─── Page Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 30px 0 10px;">
    <div style="font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #00ff88);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        🔍 AI-Powered News Analysis
    </div>
    <div style="color: #8899aa; font-size: 1rem; margin-top: 8px;">
        ML Classification · Azure AI Sentiment · Key Phrase Extraction
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# ─── Check Model Availability ───────────────────────────────────────────────
predictor, load_error = load_predictor()
db = load_database()

if predictor is None:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2d1b1b, #1a1a2e);
        border: 1px solid rgba(255, 71, 87, 0.3); border-radius: 16px;
        padding: 40px; text-align: center; margin: 20px 0;">
        <div style="font-size: 3rem; margin-bottom: 16px;">⚠️</div>
        <div style="font-size: 1.3rem; font-weight: 700; color: #ff4757; margin-bottom: 12px;">
            Model Not Found
        </div>
        <div style="color: #8899aa; font-size: 0.95rem; line-height: 1.7; max-width: 500px; margin: 0 auto;">
            The trained model has not been loaded yet. Please run <code style="color:#00d4ff;">python main.py</code>
            first to train the model and generate the necessary files.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if load_error:
        with st.expander("🔧 Error Details"):
            st.code(load_error)

# ─── Sample Articles ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📋 Quick Test with Sample Articles</div>', unsafe_allow_html=True)

sample_cols = st.columns(3)
for i, (label, texts) in enumerate(SAMPLE_ARTICLES.items()):
    with sample_cols[i]:
        if st.button(label, key=f"sample_{i}", use_container_width=True):
            st.session_state.news_input = random.choice(texts)

# ─── Input Area ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">✍️ Enter News Article</div>', unsafe_allow_html=True)

news_text = st.text_area(
    "Paste your news article here:",
    height=200,
    placeholder="Enter or paste a news article to analyze...",
    key="news_input",
    label_visibility="collapsed",
)

col_btn, col_clear = st.columns([3, 1])
with col_btn:
    analyze_btn = st.button(
        "🚀 Analyze Article",
        type="primary",
        use_container_width=True,
        disabled=(predictor is None),
    )
with col_clear:
    if st.button("🗑️ Clear", use_container_width=True):
        st.rerun()


# ─── Analysis ────────────────────────────────────────────────────────────────
if analyze_btn and news_text.strip() and predictor is not None:
    with st.spinner("🔄 Analyzing article..."):
        try:
            # ═══════════════════════════════════════════════════════════
            # STEP 1: ML Prediction (existing functionality)
            # ═══════════════════════════════════════════════════════════
            result = predictor.predict(news_text)
            prediction = result.get("prediction", "Unknown")
            confidence = result.get("confidence", 0.0)
            probabilities = result.get("probabilities", {})

            is_fake = prediction.upper() in ["FAKE", "1", 1]
            label_text = "FAKE NEWS" if is_fake else "REAL NEWS"
            badge_class = "fake-badge" if is_fake else "real-badge"
            icon = "🚫" if is_fake else "✅"
            conf_pct = confidence * 100 if confidence <= 1 else confidence

            # ═══════════════════════════════════════════════════════════
            # STEP 2: Azure AI Language Analysis
            # ═══════════════════════════════════════════════════════════
            sentiment_result = None
            key_phrases_result = None

            if azure_analyzer and azure_analyzer.is_configured:
                azure_results = azure_analyzer.analyze(news_text)
                sentiment_result = azure_results["sentiment_result"]
                key_phrases_result = azure_results["key_phrases_result"]

            # ═══════════════════════════════════════════════════════════
            # STEP 3: Save to Database
            # ═══════════════════════════════════════════════════════════
            if db:
                db.save_analysis(
                    article_text=news_text,
                    ml_prediction=prediction,
                    ml_confidence=confidence,
                    sentiment=(
                        sentiment_result["sentiment"]
                        if sentiment_result and sentiment_result["success"]
                        else None
                    ),
                    sentiment_confidence=(
                        sentiment_result["confidence_scores"]
                        if sentiment_result and sentiment_result["success"]
                        else None
                    ),
                    key_phrases=(
                        key_phrases_result["key_phrases"]
                        if key_phrases_result and key_phrases_result["success"]
                        else None
                    ),
                )

            # ═══════════════════════════════════════════════════════════
            # DISPLAY RESULTS
            # ═══════════════════════════════════════════════════════════
            st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

            # ── SECTION A: ML Prediction Result ──
            st.markdown('<div class="section-header">🤖 ML Classification Result</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card">
                <div style="margin-bottom: 20px;">
                    <span class="prediction-badge {badge_class}">
                        {icon} {label_text}
                    </span>
                </div>
                <div style="color: #8899aa; font-size: 0.95rem;">
                    Confidence: <strong style="color: #00d4ff;">{conf_pct:.1f}%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Gauge + Probabilities row
            mc1, mc2 = st.columns(2)

            with mc1:
                gauge_color = "#ff4757" if is_fake else "#00ff88"
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=conf_pct,
                    number={"suffix": "%", "font": {"size": 42, "color": "#e0e0e0"}},
                    title={"text": "Confidence Score", "font": {"size": 16, "color": "#8899aa"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#556677",
                                 "tickfont": {"color": "#556677"}},
                        "bar": {"color": gauge_color, "thickness": 0.3},
                        "bgcolor": "#1e2a3a",
                        "borderwidth": 0,
                        "steps": [
                            {"range": [0, 50], "color": "rgba(255,71,87,0.1)"},
                            {"range": [50, 75], "color": "rgba(255,165,0,0.1)"},
                            {"range": [75, 100], "color": "rgba(0,255,136,0.1)"},
                        ],
                        "threshold": {
                            "line": {"color": "#00d4ff", "width": 3},
                            "thickness": 0.8,
                            "value": conf_pct,
                        },
                    },
                ))
                fig_gauge.update_layout(
                    height=300, margin=dict(t=60, b=20, l=40, r=40),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#e0e0e0"},
                )
                st.plotly_chart(fig_gauge, use_container_width=True)

            with mc2:
                if probabilities:
                    prob_fake = probabilities.get("FAKE", 0)
                    prob_real = probabilities.get("REAL", 0)
                    pf = prob_fake * 100 if prob_fake <= 1 else prob_fake
                    pr = prob_real * 100 if prob_real <= 1 else prob_real
                else:
                    pf, pr = (conf_pct, 100 - conf_pct) if is_fake else (100 - conf_pct, conf_pct)

                fig_bar = go.Figure()
                fig_bar.add_trace(go.Bar(
                    x=[pr], y=["Prediction"], orientation="h",
                    name="Real", marker_color="#00ff88",
                    text=[f"{pr:.1f}%"], textposition="inside",
                    textfont={"size": 14, "color": "#0e1117", "family": "Inter"},
                ))
                fig_bar.add_trace(go.Bar(
                    x=[pf], y=["Prediction"], orientation="h",
                    name="Fake", marker_color="#ff4757",
                    text=[f"{pf:.1f}%"], textposition="inside",
                    textfont={"size": 14, "color": "#ffffff", "family": "Inter"},
                ))
                fig_bar.update_layout(
                    barmode="stack", template="plotly_dark", height=300,
                    title={"text": "Class Probabilities", "font": {"size": 16, "color": "#8899aa"}},
                    margin=dict(t=60, b=20, l=20, r=20),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=True, legend=dict(orientation="h", y=-0.15,
                        font={"color": "#8899aa"}),
                    yaxis=dict(visible=False),
                    xaxis=dict(visible=False, range=[0, 100]),
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            # ── Important Words ──
            st.markdown('<div class="section-header">🔤 Key Influential Words</div>', unsafe_allow_html=True)
            try:
                important_words = predictor.get_important_words(news_text, top_n=15)
                if important_words:
                    words_html = ""
                    for item in important_words:
                        if isinstance(item, dict):
                            word = item.get("word", "")
                            score = item.get("score", 0)
                            direction = item.get("direction", "")
                            tag_class = "word-tag-fake" if direction == "fake" else "word-tag-real"
                            words_html += f'<span class="word-tag {tag_class}">{word} ({score:.3f})</span>'
                        elif isinstance(item, (list, tuple)):
                            word, score = item[0], item[1]
                            tag_class = "word-tag-fake" if is_fake else "word-tag-real"
                            words_html += f'<span class="word-tag {tag_class}">{word} ({score:.3f})</span>'
                        else:
                            tag_class = "word-tag-fake" if is_fake else "word-tag-real"
                            words_html += f'<span class="word-tag {tag_class}">{item}</span>'

                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1e2a3a, #16213e);
                        border: 1px solid rgba(0, 212, 255, 0.15); border-radius: 16px;
                        padding: 24px; text-align: center;">
                        <div style="color: #8899aa; font-size: 0.85rem; margin-bottom: 16px;
                            text-transform: uppercase; letter-spacing: 1px;">
                            Words that most influenced the ML prediction
                        </div>
                        <div>{words_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No important words could be extracted for this article.")
            except Exception as e:
                st.info("Word importance analysis is not available for this model type.")

            # ═══════════════════════════════════════════════════════════
            # SECTION B: Azure AI Sentiment Analysis
            # ═══════════════════════════════════════════════════════════
            st.markdown('<div class="section-header">💭 Azure AI Sentiment Analysis</div>', unsafe_allow_html=True)

            if sentiment_result and sentiment_result["success"]:
                sentiment = sentiment_result["sentiment"]
                scores = sentiment_result["confidence_scores"]

                # Sentiment colour mapping
                sentiment_colors = {
                    "positive": "#00ff88",
                    "negative": "#ff4757",
                    "neutral": "#ffa500",
                    "mixed": "#a855f7",
                }
                sentiment_icons = {
                    "positive": "😊",
                    "negative": "😟",
                    "neutral": "😐",
                    "mixed": "🤔",
                }
                s_color = sentiment_colors.get(sentiment, "#8899aa")
                s_icon = sentiment_icons.get(sentiment, "❓")

                sc1, sc2 = st.columns([1, 2])

                with sc1:
                    st.markdown(f"""
                    <div class="result-card" style="padding: 30px;">
                        <div style="font-size: 3rem; margin-bottom: 12px;">{s_icon}</div>
                        <div style="font-size: 1.8rem; font-weight: 800; color: {s_color};
                            text-transform: uppercase; letter-spacing: 2px;">
                            {sentiment}
                        </div>
                        <div style="color: #8899aa; font-size: 0.85rem; margin-top: 8px;">
                            Overall Sentiment
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with sc2:
                    # Sentiment confidence bar chart
                    fig_sent = go.Figure()
                    fig_sent.add_trace(go.Bar(
                        x=[scores["positive"] * 100],
                        y=["Sentiment"],
                        orientation="h",
                        name="Positive",
                        marker_color="#00ff88",
                        text=[f"Positive: {scores['positive']*100:.1f}%"],
                        textposition="inside",
                        textfont={"size": 12, "color": "#0e1117"},
                    ))
                    fig_sent.add_trace(go.Bar(
                        x=[scores["neutral"] * 100],
                        y=["Sentiment"],
                        orientation="h",
                        name="Neutral",
                        marker_color="#ffa500",
                        text=[f"Neutral: {scores['neutral']*100:.1f}%"],
                        textposition="inside",
                        textfont={"size": 12, "color": "#0e1117"},
                    ))
                    fig_sent.add_trace(go.Bar(
                        x=[scores["negative"] * 100],
                        y=["Sentiment"],
                        orientation="h",
                        name="Negative",
                        marker_color="#ff4757",
                        text=[f"Negative: {scores['negative']*100:.1f}%"],
                        textposition="inside",
                        textfont={"size": 12, "color": "#ffffff"},
                    ))
                    fig_sent.update_layout(
                        barmode="stack", template="plotly_dark", height=200,
                        title={"text": "Sentiment Confidence Scores", "font": {"size": 14, "color": "#8899aa"}},
                        margin=dict(t=50, b=20, l=20, r=20),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        showlegend=True,
                        legend=dict(orientation="h", y=-0.3, font={"color": "#8899aa"}),
                        yaxis=dict(visible=False),
                        xaxis=dict(visible=False, range=[0, 100]),
                    )
                    st.plotly_chart(fig_sent, use_container_width=True)

                # Disclaimer
                st.markdown("""
                <div style="background: rgba(0, 212, 255, 0.06); border: 1px solid rgba(0, 212, 255, 0.15);
                    border-radius: 12px; padding: 14px 20px; margin-top: 12px; color: #8899aa; font-size: 0.82rem;">
                    ℹ️ <strong>Note:</strong> Sentiment analysis is independent from fake news detection.
                    A negative article is not necessarily fake, and a positive article is not necessarily real.
                    Sentiment measures emotional tone, not factual accuracy.
                </div>
                """, unsafe_allow_html=True)

            elif sentiment_result and not sentiment_result["success"]:
                st.warning(f"⚠️ Sentiment analysis error: {sentiment_result['error']}")
            else:
                st.info("☁️ Azure AI Language is not configured. Set AZURE_LANGUAGE_ENDPOINT and AZURE_LANGUAGE_KEY environment variables to enable sentiment analysis.")

            # ═══════════════════════════════════════════════════════════
            # SECTION C: Key Phrase Extraction
            # ═══════════════════════════════════════════════════════════
            st.markdown('<div class="section-header">🔑 Azure AI Key Phrase Extraction</div>', unsafe_allow_html=True)

            if key_phrases_result and key_phrases_result["success"]:
                phrases = key_phrases_result["key_phrases"]
                if phrases:
                    phrases_html = "".join(
                        f'<span class="keyphrase-tag">{phrase}</span>'
                        for phrase in phrases
                    )
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1e2a3a, #16213e);
                        border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 16px;
                        padding: 24px; text-align: center;">
                        <div style="color: #8899aa; font-size: 0.85rem; margin-bottom: 16px;
                            text-transform: uppercase; letter-spacing: 1px;">
                            {len(phrases)} Key Phrases Extracted by Azure AI
                        </div>
                        <div>{phrases_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No key phrases were extracted from this article.")

            elif key_phrases_result and not key_phrases_result["success"]:
                st.warning(f"⚠️ Key phrase extraction error: {key_phrases_result['error']}")
            else:
                st.info("☁️ Azure AI Language is not configured. Set AZURE_LANGUAGE_ENDPOINT and AZURE_LANGUAGE_KEY environment variables to enable key phrase extraction.")

            # ── Save confirmation ──
            if db:
                st.markdown("<br>", unsafe_allow_html=True)
                st.success("✅ Analysis saved to database successfully.")

            # ── Full Details Expander ──
            with st.expander("📄 Full Analysis Details"):
                det1, det2 = st.columns(2)
                with det1:
                    st.markdown("**ML Prediction:**")
                    st.write(prediction)
                    st.markdown("**ML Confidence:**")
                    st.write(f"{conf_pct:.2f}%")
                    st.markdown("**Raw Probabilities:**")
                    st.json(probabilities if probabilities else {"info": "Not available"})
                with det2:
                    if sentiment_result and sentiment_result["success"]:
                        st.markdown("**Sentiment:**")
                        st.write(sentiment_result["sentiment"])
                        st.markdown("**Sentiment Scores:**")
                        st.json(sentiment_result["confidence_scores"])
                    if key_phrases_result and key_phrases_result["success"]:
                        st.markdown("**Key Phrases:**")
                        st.write(", ".join(key_phrases_result["key_phrases"]))
                st.markdown("**Input Text Length:**")
                st.write(f"{len(news_text):,} characters | ~{len(news_text.split()):,} words")

        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
            with st.expander("🔧 Error Details"):
                import traceback
                st.code(traceback.format_exc())

elif analyze_btn and not news_text.strip():
    st.warning("⚠️ Please enter some text to analyze.")


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 40px 20px 20px; margin-top: 60px;
    border-top: 1px solid rgba(0, 212, 255, 0.1); color: #556677; font-size: 0.85rem;">
    📰 AI-Based News Article Analysis System · Powered by ML & Azure AI Language
</div>
""", unsafe_allow_html=True)
