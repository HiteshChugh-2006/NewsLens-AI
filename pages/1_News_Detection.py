"""
NewsLens AI - Real-Time Article Analysis
========================================
Interactive multi-AI news analysis integrating:
  - Supervised Machine Learning Fake/Real Classification
  - Microsoft Azure AI Language Document Sentiment Scoring
  - Microsoft Azure AI Language Key Phrase Extraction
  - Automatic ACID SQLite Persistence
"""

import streamlit as st
import plotly.graph_objects as go
import os
import sys

# ─── Add project root to path ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.styles import get_custom_css

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analyze News | NewsLens AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Shared Microsoft Fluent Light Theme CSS ─────────────────────────────────
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ─── Load ML Model & Services ────────────────────────────────────────────────
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
    except Exception:
        return None


@st.cache_resource
def load_database():
    """Load the SQLite analysis database."""
    try:
        from src.database import AnalysisDatabase
        return AnalysisDatabase()
    except Exception:
        return None


predictor, load_error = load_predictor()
azure_analyzer = load_azure_analyzer()
db = load_database()


# ─── Sample Articles ─────────────────────────────────────────────────────────
SAMPLE_ARTICLES = {
    "🇮🇳 Real Space & Science (Chandrayaan-3)": {
        "text": (
            "India made history on 23 August 2023 when the Chandrayaan-3 lander module "
            "successfully touched down on the lunar south pole, making India the fourth "
            "country in the world to achieve a soft landing on the Moon and the first to reach the southern polar region."
        ),
        "source": "ISRO / Science Editorial - Factual & Historical",
    },
    "🏛️ Real Public Policy & Relief Act": {
        "text": (
            "The House of Representatives passed a comprehensive $1.9 trillion "
            "relief package on Saturday, delivering direct assistance to millions of families and businesses. "
            "The legislation includes direct economic payments, emergency unemployment benefits, "
            "and dedicated funding for vaccine distribution, school infrastructure, and state governments."
        ),
        "source": "Legislative Record - Factual & Neutral",
    },
    "💼 Real Global Financial Markets": {
        "text": (
            "Global markets rallied on Wednesday following the central bank announcement signaling "
            "an end to interest rate hikes. The benchmark S&P 500 gained 1.4% while the tech-heavy Nasdaq "
            "rose 2.0% as investors priced in easing inflationary pressures and steady economic growth."
        ),
        "source": "Financial Bureau - Analytical & Data-Driven",
    },
    "👽 Fake Conspiracy (Underground Base)": {
        "text": (
            "BREAKING SHOCKING DISCOVERY: Secret underground alien military base discovered "
            "directly beneath city hall! Multiple whistleblowers from NASA and the Pentagon fled "
            "after confirming world leaders take direct orders from extraterrestrial entities for four decades. "
            "Share this everywhere before it gets censored and deleted from the internet!"
        ),
        "source": "Flagged Source - Sensational & Unverified",
    },
    "🗳️ Fake Political Rumor (Election Fraud)": {
        "text": (
            "EXPOSED: Bombshell leaks prove corrupt officials secretly shredded over five million "
            "legitimate ballots in three swing states! Anonymous insiders provided indisputable video "
            "evidence showing shredding trucks operating outside counting centers at 3:00 AM."
        ),
        "source": "Flagged Source - Emotionally Charged & Fabricated",
    },
    "💊 Fake Medical Miracle (Health Clickbait)": {
        "text": (
            "Miracle cure found in common household lemon water cures cancer and diabetes instantly! "
            "Big pharma doctors are terrified that you will discover this one secret trick. "
            "Drink this every morning to eliminate all illnesses completely."
        ),
        "source": "Flagged Source - Medical Misinformation",
    },
}


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">🔍</div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #047857;">
            NewsLens AI
        </div>
        <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">
            Live Article Inspector
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Azure AI Status
    if azure_analyzer and azure_analyzer.is_configured:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 12px; margin-bottom: 12px;">
            <div style="font-size: 0.7rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Azure AI Status</div>
            <div style="font-size: 0.88rem; font-weight: 700; color: #059669; margin-top: 3px;">
                ● Connected & Active
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 12px; padding: 12px; margin-bottom: 12px;">
            <div style="font-size: 0.7rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Azure AI Status</div>
            <div style="font-size: 0.88rem; font-weight: 700; color: #D97706; margin-top: 3px;">
                ○ Offline (Config in .env)
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Database quick counter
    if db:
        stats = db.get_statistics()
        st.markdown(f"""
        <div style="padding: 6px; font-size: 0.82rem; color: #64748B; line-height: 1.7;">
            <strong style="color: #0F172A;">🗄️ Database Audit</strong><br>
            Total Records: <strong style="color: #047857;">{stats['total']}</strong><br>
            Fake News: <span style="color: #E11D48; font-weight: 600;">{stats['fake']}</span> | 
            Real: <span style="color: #059669; font-weight: 600;">{stats['real']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="color: #64748B; font-size: 0.8rem; line-height: 1.6;">
        <strong style="color: #0F172A;">ℹ️ Multi-AI Pipeline</strong><br>
        1. <strong>ML Classifier</strong> predicts authenticity<br>
        2. <strong>Azure Language</strong> extracts emotional tone<br>
        3. <strong>Azure Language</strong> extracts key entities<br>
        4. <strong>SQLite</strong> stores complete audit record
    </div>
    """, unsafe_allow_html=True)


# ─── Page Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 16px 0 8px;">
    <div style="font-size: 2.4rem; font-weight: 800;
        background: linear-gradient(135deg, #065F46 0%, #059669 50%, #0D9488 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        🔍 Multi-AI News Article Analysis
    </div>
    <div style="color: #64748B; font-size: 1rem; margin-top: 6px;">
        Combine ML-based fake news classification with Microsoft Azure AI Language sentiment scoring and key phrase extraction
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ─── Model Check ─────────────────────────────────────────────────────────────
if predictor is None:
    st.error(f"❌ Failed to load ML model: {load_error}")
    st.info("Please make sure model files exist in the `models/` directory or run `python main.py` to train.")
    st.stop()


# ─── Sample Selection ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">⚡ Load Quick Sample Articles</div>', unsafe_allow_html=True)

sample_cols = st.columns(4)
for i, (name, data) in enumerate(SAMPLE_ARTICLES.items()):
    with sample_cols[i]:
        if st.button(name, use_container_width=True):
            st.session_state["input_text"] = data["text"]
            st.rerun()


# ─── Input Form ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📝 Enter News Article</div>', unsafe_allow_html=True)

default_text = st.session_state.get("input_text", "")

news_text = st.text_area(
    "Paste the full news article text below:",
    value=default_text,
    height=220,
    placeholder="Paste news headline and body text here for comprehensive AI analysis...",
    help="For best results, include both the headline and at least 2-3 paragraphs of article text.",
)

col_count, col_clear, col_btn = st.columns([2, 1, 1.5])

with col_count:
    words = len(news_text.split()) if news_text.strip() else 0
    chars = len(news_text)
    st.caption(f"📊 Article metrics: **{words}** words · **{chars}** characters")

with col_clear:
    if st.button("🗑️ Clear Input", use_container_width=True):
        st.session_state["input_text"] = ""
        st.rerun()

with col_btn:
    analyze_btn = st.button("🚀 Analyze Article", type="primary", use_container_width=True)


# ─── Analysis Execution ──────────────────────────────────────────────────────
if analyze_btn:
    if not news_text.strip():
        st.warning("⚠️ Please enter or paste some news article text before analyzing.")
    elif len(news_text.strip().split()) < 5:
        st.warning("⚠️ Article text is too short. Please provide at least 5 words for a reliable analysis.")
    else:
        with st.spinner("🧠 Running Multi-AI Analysis (ML Classification + Azure Cognitive Services)..."):

            # 1. ML Prediction
            try:
                ml_result = predictor.predict(news_text)
                pred_label = ml_result.get("prediction", "UNKNOWN")
                confidence = ml_result.get("confidence", 0.0)
                probabilities = ml_result.get("probabilities", {})
                is_fake = pred_label == "FAKE"
            except Exception as e:
                st.error(f"Error during ML prediction: {e}")
                pred_label, confidence, probabilities, is_fake = "UNKNOWN", 0.0, {}, False

            # 2. Azure Sentiment & Key Phrases
            sentiment_result = None
            key_phrases_result = None
            if azure_analyzer and azure_analyzer.is_configured:
                try:
                    sentiment_result = azure_analyzer.analyze_sentiment(news_text)
                except Exception as e:
                    sentiment_result = {"success": False, "error": str(e), "sentiment": None, "confidence_scores": None}

                try:
                    key_phrases_result = azure_analyzer.extract_key_phrases(news_text)
                except Exception as e:
                    key_phrases_result = {"success": False, "error": str(e), "key_phrases": []}
            elif azure_analyzer:
                sentiment_result = {"success": False, "error": azure_analyzer.configuration_message, "sentiment": None, "confidence_scores": None}
                key_phrases_result = {"success": False, "error": azure_analyzer.configuration_message, "key_phrases": []}

            # 3. Save to SQLite Database
            saved_record_id = None
            if db:
                try:
                    sent_val = sentiment_result.get("sentiment") if sentiment_result and sentiment_result.get("success") else "not_configured"
                    sent_conf = sentiment_result.get("confidence_scores") if sentiment_result and sentiment_result.get("success") else None
                    phrases_val = key_phrases_result.get("key_phrases", []) if key_phrases_result and key_phrases_result.get("success") else []

                    saved_record_id = db.save_analysis(
                        article_text=news_text,
                        ml_prediction=pred_label,
                        ml_confidence=confidence,
                        sentiment=sent_val or "unknown",
                        sentiment_confidence=sent_conf,
                        key_phrases=phrases_val
                    )
                except Exception:
                    pass

            # ═══════════════════════════════════════════════════════════
            # SECTION A: ML Classification Results
            # ═══════════════════════════════════════════════════════════
            st.markdown('<div class="section-header">🤖 Machine Learning Veracity Verdict</div>', unsafe_allow_html=True)

            badge_class = "fake-badge" if is_fake else "real-badge"
            icon = "🚨" if is_fake else "✅"
            label = "FAKE NEWS DETECTED" if is_fake else "REAL NEWS VERIFIED"
            conf_pct = confidence * 100

            st.markdown(f"""
            <div style="text-align: center; margin: 16px 0;">
                <div class="prediction-badge {badge_class}">
                    <span>{icon}</span>
                    <span>{label}</span>
                </div>
                <div style="color: #64748B; font-size: 0.95rem; margin-top: 6px;">
                    Algorithm: <strong style="color: #0F172A;">XGBoost Classifier</strong> &nbsp;|&nbsp; 
                    Model Confidence: <strong style="color: #047857;">{conf_pct:.1f}%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Gauge + Probabilities row
            mc1, mc2 = st.columns(2)

            with mc1:
                gauge_color = "#E11D48" if is_fake else "#059669"
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=conf_pct,
                    number={"suffix": "%", "font": {"size": 42, "color": "#0F172A", "family": "Plus Jakarta Sans"}},
                    title={"text": "Confidence Level", "font": {"size": 15, "color": "#64748B", "family": "Plus Jakarta Sans"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#CBD5E1", "tickfont": {"color": "#64748B"}},
                        "bar": {"color": gauge_color, "thickness": 0.28},
                        "bgcolor": "#F1F5F9",
                        "borderwidth": 0,
                        "steps": [
                            {"range": [0, 50], "color": "rgba(225,29,72,0.06)"},
                            {"range": [50, 75], "color": "rgba(245,158,11,0.06)"},
                            {"range": [75, 100], "color": "rgba(16,185,129,0.08)"},
                        ],
                        "threshold": {
                            "line": {"color": "#0F172A", "width": 3},
                            "thickness": 0.75,
                            "value": conf_pct,
                        },
                    },
                ))
                fig_gauge.update_layout(
                    template="plotly_white",
                    height=280, margin=dict(t=50, b=20, l=35, r=35),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
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
                    x=[pr], y=["Probability"], orientation="h",
                    name="Real News", marker_color="#10B981",
                    text=[f"Real: {pr:.1f}%"], textposition="inside",
                    textfont={"size": 13, "color": "#FFFFFF", "family": "Plus Jakarta Sans"},
                ))
                fig_bar.add_trace(go.Bar(
                    x=[pf], y=["Probability"], orientation="h",
                    name="Fake News", marker_color="#F43F5E",
                    text=[f"Fake: {pf:.1f}%"], textposition="inside",
                    textfont={"size": 13, "color": "#FFFFFF", "family": "Plus Jakarta Sans"},
                ))
                fig_bar.update_layout(
                    template="plotly_white",
                    barmode="stack", height=280,
                    title={"text": "Class Probability Distribution", "font": {"size": 15, "color": "#64748B", "family": "Plus Jakarta Sans"}},
                    margin=dict(t=50, b=20, l=20, r=20),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=True,
                    legend=dict(orientation="h", y=-0.15, font={"color": "#64748B"}),
                    yaxis=dict(visible=False),
                    xaxis=dict(visible=False, range=[0, 100]),
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            # ── Word Attribution ──
            st.markdown('<div class="section-header">🔤 Influential Vocabulary Terms</div>', unsafe_allow_html=True)
            try:
                important_words = predictor.get_important_words(news_text, top_n=14)
                if important_words:
                    words_html = ""
                    for item in important_words:
                        if isinstance(item, dict):
                            word = item.get("word", "")
                            score = item.get("score", 0)
                            direction = item.get("direction", "")
                            tag_class = "word-tag-fake" if direction == "fake" else "word-tag-real"
                            words_html += f'<span class="word-tag {tag_class}">{word} <em>({score:.2f})</em></span>'
                        elif isinstance(item, (list, tuple)):
                            word, score = item[0], item[1]
                            tag_class = "word-tag-fake" if is_fake else "word-tag-real"
                            words_html += f'<span class="word-tag {tag_class}">{word} <em>({score:.2f})</em></span>'
                        else:
                            tag_class = "word-tag-fake" if is_fake else "word-tag-real"
                            words_html += f'<span class="word-tag {tag_class}">{item}</span>'

                    st.markdown(f"""
                    <div class="info-card" style="text-align: center; padding: 20px;">
                        <div style="color: #64748B; font-size: 0.82rem; margin-bottom: 12px;
                            text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
                            Top TF-IDF words pushing classification towards Real (Emerald) or Fake (Red)
                        </div>
                        <div>{words_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No salient dictionary words could be isolated for this article.")
            except Exception:
                st.info("Word contribution breakdown is not available for this model type.")

            # ═══════════════════════════════════════════════════════════
            # SECTION B: Azure AI Sentiment Analysis
            # ═══════════════════════════════════════════════════════════
            st.markdown('<div class="section-header">💭 Azure AI Language Sentiment Analysis</div>', unsafe_allow_html=True)

            if sentiment_result and sentiment_result.get("success"):
                sentiment = sentiment_result["sentiment"]
                scores = sentiment_result["confidence_scores"]

                sentiment_colors = {
                    "positive": "#059669",
                    "negative": "#E11D48",
                    "neutral": "#D97706",
                    "mixed": "#0284C7",
                }
                sentiment_icons = {
                    "positive": "😊",
                    "negative": "😟",
                    "neutral": "😐",
                    "mixed": "🤔",
                }
                s_color = sentiment_colors.get(sentiment, "#64748B")
                s_icon = sentiment_icons.get(sentiment, "❓")

                sc1, sc2 = st.columns([1, 2.2])

                with sc1:
                    st.markdown(f"""
                    <div class="info-card" style="text-align: center; padding: 28px 18px;">
                        <div style="font-size: 3rem; margin-bottom: 8px;">{s_icon}</div>
                        <div style="font-size: 1.8rem; font-weight: 800; color: {s_color};
                            text-transform: uppercase; letter-spacing: 1px;">
                            {sentiment}
                        </div>
                        <div style="color: #64748B; font-size: 0.82rem; margin-top: 6px; font-weight: 600; text-transform: uppercase;">
                            Overall Tone
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with sc2:
                    fig_sent = go.Figure()
                    fig_sent.add_trace(go.Bar(
                        x=[scores["positive"] * 100],
                        y=["Sentiment"],
                        orientation="h",
                        name="Positive",
                        marker_color="#10B981",
                        text=[f"Positive: {scores['positive']*100:.1f}%"],
                        textposition="inside",
                        textfont={"size": 12, "color": "#FFFFFF", "family": "Plus Jakarta Sans"},
                    ))
                    fig_sent.add_trace(go.Bar(
                        x=[scores["neutral"] * 100],
                        y=["Sentiment"],
                        orientation="h",
                        name="Neutral",
                        marker_color="#F59E0B",
                        text=[f"Neutral: {scores['neutral']*100:.1f}%"],
                        textposition="inside",
                        textfont={"size": 12, "color": "#FFFFFF", "family": "Plus Jakarta Sans"},
                    ))
                    fig_sent.add_trace(go.Bar(
                        x=[scores["negative"] * 100],
                        y=["Sentiment"],
                        orientation="h",
                        name="Negative",
                        marker_color="#F43F5E",
                        text=[f"Negative: {scores['negative']*100:.1f}%"],
                        textposition="inside",
                        textfont={"size": 12, "color": "#FFFFFF", "family": "Plus Jakarta Sans"},
                    ))
                    fig_sent.update_layout(
                        template="plotly_white",
                        barmode="stack", height=180,
                        title={"text": "Azure Sentiment Confidence Distribution", "font": {"size": 14, "color": "#64748B", "family": "Plus Jakarta Sans"}},
                        margin=dict(t=40, b=20, l=15, r=15),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        showlegend=True,
                        legend=dict(orientation="h", y=-0.35, font={"color": "#64748B"}),
                        yaxis=dict(visible=False),
                        xaxis=dict(visible=False, range=[0, 100]),
                    )
                    st.plotly_chart(fig_sent, use_container_width=True)

                st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.2);
                    border-radius: 10px; padding: 12px 18px; margin-top: 10px; color: #475569; font-size: 0.83rem;">
                    💡 <strong>Orthogonal Metric:</strong> Sentiment measures emotional tone, not factual veracity. A tragic real event often registers negative tone, while fabricated clickbait can be overwhelmingly positive.
                </div>
                """, unsafe_allow_html=True)

            elif sentiment_result and not sentiment_result["success"]:
                st.warning(f"⚠️ Azure sentiment error: {sentiment_result['error']}")
            else:
                st.info("☁️ Azure AI Language is not configured. Add credentials in `.env` to enable sentiment scoring.")

            # ═══════════════════════════════════════════════════════════
            # SECTION C: Key Phrase Extraction
            # ═══════════════════════════════════════════════════════════
            st.markdown('<div class="section-header">🔑 Azure AI Key Phrase Extraction</div>', unsafe_allow_html=True)

            if key_phrases_result and key_phrases_result.get("success"):
                phrases = key_phrases_result.get("key_phrases", [])
                if phrases:
                    phrases_html = "".join(
                        f'<span class="phrase-tag">{phrase}</span>'
                        for phrase in phrases
                    )
                    st.markdown(f"""
                    <div class="info-card" style="text-align: center; padding: 22px;">
                        <div style="color: #64748B; font-size: 0.82rem; margin-bottom: 12px;
                            text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
                            {len(phrases)} Salient Phrases & Entities Extracted by Azure AI Language
                        </div>
                        <div>{phrases_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No salient key phrases were extracted from this article.")

            elif key_phrases_result and not key_phrases_result["success"]:
                st.warning(f"⚠️ Azure key phrase error: {key_phrases_result['error']}")
            else:
                st.info("☁️ Azure AI Language is not configured. Add credentials in `.env` to enable key phrase extraction.")

            # ── Save confirmation ──
            if saved_record_id:
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 10px; padding: 12px 18px; margin-top: 16px; color: #047857; font-weight: 600; font-size: 0.88rem;">
                    ✅ Complete analysis saved to SQLite audit database as <strong>Record #{saved_record_id}</strong>.
                </div>
                """, unsafe_allow_html=True)
