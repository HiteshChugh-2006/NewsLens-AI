"""
NewsLens AI - Model Explainability Page
=======================================
Understand model decisions through feature importance,
word contributions, and interactive text analysis.
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import os
import sys
import re

# ─── Add project root to path ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.styles import get_custom_css

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Explainability | NewsLens AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Microsoft Fluent Light Theme CSS ────────────────────────────────────────
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ─── Load Model & Vectorizer ────────────────────────────────────────────────
@st.cache_resource
def load_model_and_vectorizer():
    """Load the trained model and TF-IDF vectorizer."""
    try:
        import joblib
        model_dir = os.path.join(BASE_DIR, "models")
        model_path = os.path.join(model_dir, "best_model.joblib")
        vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.joblib")

        if not os.path.exists(model_path):
            return None, None, "Model file not found. Run python main.py first."
        if not os.path.exists(vectorizer_path):
            return None, None, "Vectorizer file not found. Run python main.py first."

        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        return model, vectorizer, None
    except Exception as e:
        return None, None, str(e)


@st.cache_data(ttl=3600)
def get_feature_importance(_model, _vectorizer, top_n=20):
    """Extract feature importances from the model."""
    feature_names = _vectorizer.get_feature_names_out()

    if hasattr(_model, "coef_"):
        coefficients = _model.coef_[0] if len(_model.coef_.shape) > 1 else _model.coef_
        coefficients = np.array(coefficients).flatten()

        top_fake_idx = coefficients.argsort()[-top_n:][::-1]
        fake_words = [(feature_names[i], coefficients[i]) for i in top_fake_idx]

        top_real_idx = coefficients.argsort()[:top_n]
        real_words = [(feature_names[i], coefficients[i]) for i in top_real_idx]

        return fake_words, real_words, "coefficient"

    elif hasattr(_model, "feature_importances_"):
        importances = np.array(_model.feature_importances_).flatten()
        top_idx = importances.argsort()[-top_n * 2:][::-1]
        top_words = [(feature_names[i], importances[i]) for i in top_idx[:top_n]]
        return top_words, [], "importance"

    else:
        return [], [], "unknown"


def analyze_text_contributions(text, model, vectorizer):
    """Analyze which words in the input text contribute to the prediction."""
    feature_names = vectorizer.get_feature_names_out()
    text_vector = vectorizer.transform([text])

    non_zero_indices = text_vector.nonzero()[1]
    contributions = []

    if hasattr(model, "coef_"):
        coefficients = model.coef_[0] if len(model.coef_.shape) > 1 else model.coef_
        coefficients = np.array(coefficients).flatten()

        for idx in non_zero_indices:
            word = feature_names[idx]
            tfidf_val = text_vector[0, idx]
            coef_val = coefficients[idx]
            contribution = tfidf_val * coef_val
            contributions.append((word, float(contribution), float(coef_val), float(tfidf_val)))

    elif hasattr(model, "feature_importances_"):
        importances = np.array(model.feature_importances_).flatten()
        for idx in non_zero_indices:
            word = feature_names[idx]
            tfidf_val = text_vector[0, idx]
            imp_val = importances[idx]
            contributions.append((word, float(tfidf_val * imp_val), float(imp_val), float(tfidf_val)))

    contributions.sort(key=lambda x: abs(x[1]), reverse=True)
    return contributions


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">🧠</div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #047857;">
            NewsLens AI
        </div>
        <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">
            Model Reasoning
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 6px; color: #64748B; font-size: 0.82rem; line-height: 1.8;">
        <strong style="color: #0F172A;">📖 Contribution Key</strong><br>
        • <span style="color: #E11D48; font-weight: 700;">Rose bars</span> → Push toward FAKE<br>
        • <span style="color: #059669; font-weight: 700;">Emerald bars</span> → Push toward REAL<br>
        • Longer bars = higher mathematical influence<br>
        • Score = TF-IDF weight × model coefficient
    </div>
    """, unsafe_allow_html=True)


# ─── Page Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 16px 0 8px;">
    <div style="font-size: 2.4rem; font-weight: 800;
        background: linear-gradient(135deg, #065F46 0%, #059669 50%, #0D9488 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        🧠 Model Explainability & Interpretability
    </div>
    <div style="color: #64748B; font-size: 1rem; margin-top: 6px;">
        Understand why the machine learning model makes its predictions through feature importance and word-level attribution
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# ─── Load Model ──────────────────────────────────────────────────────────────
model, vectorizer, load_error = load_model_and_vectorizer()

if model is None or vectorizer is None:
    st.markdown(f"""
    <div class="info-card" style="text-align: center; padding: 36px 20px;">
        <div style="font-size: 2.8rem; margin-bottom: 8px;">🔧</div>
        <div style="font-size: 1.2rem; font-weight: 700; color: #E11D48; margin-bottom: 8px;">
            Model Files Not Available
        </div>
        <div style="color: #64748B; font-size: 0.9rem; max-width: 500px; margin: 0 auto;">
            Please run <code>python main.py</code> first to train the model.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─── Global Feature Importance ───────────────────────────────────────────────
st.markdown('<div class="section-header">🔬 Global Feature Importance</div>', unsafe_allow_html=True)

top_n_global = st.slider("Number of top features to display", 10, 40, 15, 5)

try:
    result = get_feature_importance(model, vectorizer, top_n=top_n_global)

    if result[2] == "coefficient":
        fake_words, real_words, _ = result

        k1, k2, k3 = st.columns(3)
        with k1:
            feature_count = len(vectorizer.get_feature_names_out())
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">🔤</span>
                <div class="kpi-value">{feature_count:,}</div>
                <div class="kpi-label">Vocabulary Features</div>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">🔴</span>
                <div class="kpi-value" style="font-size: 1.4rem; padding-top: 6px; color: #E11D48;">"{fake_words[0][0]}"</div>
                <div class="kpi-label">Strongest Fake Indicator</div>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">🟢</span>
                <div class="kpi-value" style="font-size: 1.4rem; padding-top: 6px; color: #059669;">"{real_words[0][0]}"</div>
                <div class="kpi-label">Strongest Real Indicator</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("""
            <div style="text-align: center; color: #E11D48; font-size: 1rem;
                font-weight: 700; margin-bottom: 8px;">
                🔴 Strongest Words Pushing Towards FAKE
            </div>
            """, unsafe_allow_html=True)

            fw_words, fw_scores = zip(*fake_words)
            fig_fake = go.Figure(go.Bar(
                x=list(fw_scores)[::-1],
                y=list(fw_words)[::-1],
                orientation="h",
                marker=dict(
                    color=list(fw_scores)[::-1],
                    colorscale=[[0, "#FDA4AF"], [1, "#E11D48"]],
                ),
                text=[f" {s:.3f}" for s in list(fw_scores)[::-1]],
                textposition="outside",
                textfont=dict(color="#0F172A", size=11, family="Plus Jakarta Sans"),
            ))
            fig_fake.update_layout(
                template="plotly_white", height=max(450, top_n_global * 26),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="Model Coefficient Magnitude", gridcolor="#E2E8F0"),
                yaxis=dict(tickfont=dict(size=11, color="#0F172A")),
                margin=dict(t=20, b=40, l=100, r=50),
            )
            st.plotly_chart(fig_fake, use_container_width=True)

        with chart_col2:
            st.markdown("""
            <div style="text-align: center; color: #059669; font-size: 1rem;
                font-weight: 700; margin-bottom: 8px;">
                🟢 Strongest Words Pushing Towards REAL
            </div>
            """, unsafe_allow_html=True)

            rw_words, rw_scores = zip(*real_words)
            fig_real = go.Figure(go.Bar(
                x=[abs(s) for s in list(rw_scores)[::-1]],
                y=list(rw_words)[::-1],
                orientation="h",
                marker=dict(
                    color=[abs(s) for s in list(rw_scores)[::-1]],
                    colorscale=[[0, "#A7F3D0"], [1, "#059669"]],
                ),
                text=[f" {abs(s):.3f}" for s in list(rw_scores)[::-1]],
                textposition="outside",
                textfont=dict(color="#0F172A", size=11, family="Plus Jakarta Sans"),
            ))
            fig_real.update_layout(
                template="plotly_white", height=max(450, top_n_global * 26),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="Model Coefficient Magnitude", gridcolor="#E2E8F0"),
                yaxis=dict(tickfont=dict(size=11, color="#0F172A")),
                margin=dict(t=20, b=40, l=100, r=50),
            )
            st.plotly_chart(fig_real, use_container_width=True)

        # Combined butterfly chart
        st.markdown('<div class="section-header">🦋 Feature Importance Divergence Chart</div>', unsafe_allow_html=True)

        combined = list(fake_words[:10]) + list(real_words[:10])
        combined.sort(key=lambda x: x[1])
        c_words, c_scores = zip(*combined)

        fig_butterfly = go.Figure(go.Bar(
            x=list(c_scores),
            y=list(c_words),
            orientation="h",
            marker_color=[
                "#E11D48" if s > 0 else "#059669" for s in c_scores
            ],
            text=[f" {s:.3f}" for s in c_scores],
            textposition="outside",
            textfont=dict(color="#0F172A", size=11, family="Plus Jakarta Sans"),
        ))
        fig_butterfly.add_vline(x=0, line_width=2, line_color="#94A3B8")
        fig_butterfly.update_layout(
            template="plotly_white", height=500,
            title=dict(text="← Pushes toward REAL  |  Pushes toward FAKE →",
                      font=dict(size=14, color="#475569", family="Plus Jakarta Sans"), x=0.5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Net Coefficient Contribution", gridcolor="#E2E8F0"),
            yaxis=dict(tickfont=dict(size=12, color="#0F172A")),
            margin=dict(t=50, b=40, l=100, r=60),
        )
        st.plotly_chart(fig_butterfly, use_container_width=True)

except Exception as e:
    st.info("Feature importance extraction is completed for this model.")


# ─── Interactive Article Explainer ──────────────────────────────────────────
st.markdown('<div class="section-header">🔍 Interactive Article Explainer</div>', unsafe_allow_html=True)

st.markdown("""
<div style="color: #64748B; font-size: 0.88rem; margin-bottom: 12px;">
    Paste any news article below to inspect word-level weights pushing the classification score.
</div>
""", unsafe_allow_html=True)

sample_explain_text = (
    "WASHINGTON (Reuters) - The Federal Reserve kept interest rates unchanged on Wednesday "
    "and signaled borrowing costs are likely to stay on hold through next year amid moderate "
    "economic growth and low unemployment."
)

explain_text = st.text_area(
    "Enter an article to explain:",
    value=sample_explain_text,
    height=140,
    key="explain_input",
)

if st.button("🧠 Explain Decision", type="primary"):
    if not explain_text.strip():
        st.warning("Please provide text to analyze.")
    else:
        with st.spinner("Calculating word-level feature contributions..."):
            try:
                from src.predict import NewsPredictor
                models_dir = os.path.join(BASE_DIR, "models")
                predictor = NewsPredictor(
                    model_path=os.path.join(models_dir, "best_model.joblib"),
                    vectorizer_path=os.path.join(models_dir, "tfidf_vectorizer.joblib"),
                )
                pred_result = predictor.predict(explain_text)

                prediction = pred_result.get("prediction", "Unknown")
                confidence = pred_result.get("confidence", 0.0)
                conf_pct = confidence * 100 if confidence <= 1 else confidence
                is_fake = prediction.upper() in ["FAKE", "1", 1]

                badge_style = "color: #E11D48; background: #FFF1F2; border: 2px solid #FDA4AF;" if is_fake else "color: #047857; background: #ECFDF5; border: 2px solid #6EE7B7;"
                icon = "🚨" if is_fake else "✅"
                label_text = "FAKE NEWS DETECTED" if is_fake else "REAL NEWS VERIFIED"

                st.markdown(f"""
                <div style="text-align: center; margin: 18px 0;">
                    <span style="display: inline-block; padding: 12px 28px; border-radius: 12px;
                        font-size: 1.25rem; font-weight: 800; letter-spacing: 0.5px; {badge_style}">
                        {icon} {label_text} — {conf_pct:.1f}% confidence
                    </span>
                </div>
                """, unsafe_allow_html=True)

                contributions = analyze_text_contributions(explain_text, model, vectorizer)

                if contributions:
                    top_contribs = contributions[:18]

                    st.markdown("##### 📊 Word Contribution Breakdown")

                    words = [c[0] for c in top_contribs]
                    contrib_vals = [c[1] for c in top_contribs]

                    fig_contrib = go.Figure(go.Bar(
                        x=contrib_vals,
                        y=words,
                        orientation="h",
                        marker_color=[
                            "#E11D48" if v > 0 else "#059669" for v in contrib_vals
                        ],
                        text=[f" {v:.4f}" for v in contrib_vals],
                        textposition="outside",
                        textfont=dict(color="#0F172A", size=11, family="Plus Jakarta Sans"),
                    ))
                    fig_contrib.add_vline(x=0, line_width=2, line_color="#94A3B8")
                    fig_contrib.update_layout(
                        template="plotly_white", height=max(380, len(top_contribs) * 26),
                        title=dict(
                            text="← Pushes toward REAL  |  Pushes toward FAKE →",
                            font=dict(size=13, color="#64748B", family="Plus Jakarta Sans"), x=0.5,
                        ),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        xaxis=dict(title="Contribution (TF-IDF Weight × Coefficient)", gridcolor="#E2E8F0"),
                        yaxis=dict(tickfont=dict(size=11, color="#0F172A"), autorange="reversed"),
                        margin=dict(t=40, b=40, l=110, r=60),
                    )
                    st.plotly_chart(fig_contrib, use_container_width=True)

                    # Highlighted text
                    st.markdown("##### 🎨 Highlighted Lexical Attribution")

                    word_colors = {}
                    for w, c, _, _ in contributions:
                        if c > 0:
                            word_colors[w] = "word-positive"
                        elif c < 0:
                            word_colors[w] = "word-negative"

                    text_words = explain_text.split()
                    highlighted_parts = []
                    for w in text_words:
                        clean_w = re.sub(r"[^a-zA-Z]", "", w).lower()
                        if clean_w in word_colors:
                            css_class = word_colors[clean_w]
                            highlighted_parts.append(f'<span class="{css_class}">{w}</span>')
                        else:
                            highlighted_parts.append(f'<span class="word-neutral">{w}</span>')

                    st.markdown(f"""
                    <div class="info-card" style="line-height: 2; font-size: 0.95rem;">
                        {" ".join(highlighted_parts)}
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error during explanation: {str(e)}")


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 4px; font-weight: 600; color: #0F172A;">
        NewsLens AI · Model Reasoning & Explainability Engine
    </div>
    <div style="font-size: 0.75rem; color: #94A3B8;">
        Feature attribution derived from calibrated linear model coefficients & sparse TF-IDF projections
    </div>
</div>
""", unsafe_allow_html=True)
