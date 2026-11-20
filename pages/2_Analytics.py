"""
NewsLens AI - Dataset Analytics Page
====================================
Interactive exploration of the training dataset with charts,
word clouds, and statistical analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import re
from collections import Counter

# ─── Add project root to path ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.styles import get_custom_css

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dataset Analytics | NewsLens AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Microsoft Fluent Light Theme CSS ────────────────────────────────────────
st.markdown(get_custom_css(), unsafe_allow_html=True)

STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above",
    "below", "between", "out", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "each", "every", "both", "few", "more", "most",
    "other", "some", "such", "no", "nor", "not", "only", "own", "same",
    "so", "than", "too", "very", "just", "because", "but", "and", "or",
    "if", "while", "this", "that", "these", "those", "it", "its", "he",
    "she", "they", "them", "their", "we", "us", "our", "you", "your",
    "i", "me", "my", "said", "also", "one", "new", "s", "t", "would",
    "people", "like", "get", "make", "know", "say", "go", "see", "come",
    "take", "want", "look", "use", "find", "give", "tell", "think",
    "well", "even", "back", "still", "way", "time", "year", "two",
    "first", "last", "many", "much", "about", "up", "down", "now",
    "long", "made", "man", "day", "don", "re", "ll", "ve", "didn",
    "doesn", "won", "isn", "aren", "wasn", "weren", "haven", "hasn",
    "couldn", "wouldn", "shouldn", "mustn",
}


@st.cache_data(ttl=3600)
def load_dataset():
    """Load fake and true news datasets."""
    fake_path = os.path.join(BASE_DIR, "dataset", "Fake.csv")
    true_path = os.path.join(BASE_DIR, "dataset", "True.csv")

    if not os.path.exists(fake_path) or not os.path.exists(true_path):
        return None, "Dataset files not found."

    try:
        fake_df = pd.read_csv(fake_path)
        true_df = pd.read_csv(true_path)

        fake_df["label"] = "Fake"
        true_df["label"] = "Real"

        text_col = None
        for col in ["text", "Text", "content", "Content", "article", "Article"]:
            if col in fake_df.columns:
                text_col = col
                break

        if text_col is None:
            text_col = fake_df.columns[-1] if len(fake_df.columns) > 1 else fake_df.columns[0]

        df = pd.concat([fake_df, true_df], ignore_index=True)
        df["text_length"] = df[text_col].astype(str).apply(len)
        df["word_count"] = df[text_col].astype(str).apply(lambda x: len(x.split()))

        return df, text_col
    except Exception as e:
        return None, str(e)


def get_word_frequencies(texts, top_n=20):
    """Get most common words after basic cleaning."""
    all_words = []
    for text in texts:
        text = str(text).lower()
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        words = [w for w in text.split() if w not in STOP_WORDS and len(w) > 2]
        all_words.extend(words)
    return Counter(all_words).most_common(top_n)


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">📊</div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #047857;">
            NewsLens AI
        </div>
        <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">
            Dataset Exploration
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Page Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 16px 0 8px;">
    <div style="font-size: 2.4rem; font-weight: 800;
        background: linear-gradient(135deg, #065F46 0%, #059669 50%, #0D9488 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        📊 Dataset Analytics & Exploration
    </div>
    <div style="color: #64748B; font-size: 1rem; margin-top: 6px;">
        Explore and understand the 44,000+ article training corpus through interactive visualizations
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# ─── Load Data ───────────────────────────────────────────────────────────────
result = load_dataset()

if result[0] is None:
    st.markdown(f"""
    <div class="info-card" style="text-align: center; padding: 36px 20px;">
        <div style="font-size: 2.8rem; margin-bottom: 8px;">📂</div>
        <div style="font-size: 1.2rem; font-weight: 700; color: #E11D48; margin-bottom: 8px;">
            Dataset Files Not Found
        </div>
        <div style="color: #64748B; font-size: 0.9rem; max-width: 500px; margin: 0 auto;">
            Please ensure <code>Fake.csv</code> and <code>True.csv</code> are in the <code>dataset/</code> directory.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df, text_col = result

# ─── KPI Row ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Corpus Overview</div>', unsafe_allow_html=True)

total = len(df)
fake_count = len(df[df["label"] == "Fake"])
real_count = len(df[df["label"] == "Real"])
avg_length = int(df["word_count"].mean())

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">📰</span>
        <div class="kpi-value">{total:,}</div>
        <div class="kpi-label">Total Articles</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🔴</span>
        <div class="kpi-value" style="color: #E11D48;">{fake_count:,}</div>
        <div class="kpi-label">Fake Articles</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🟢</span>
        <div class="kpi-value" style="color: #059669;">{real_count:,}</div>
        <div class="kpi-label">Real Articles</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">📝</span>
        <div class="kpi-value" style="color: #334155;">{avg_length:,}</div>
        <div class="kpi-label">Avg Words / Article</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Class Distribution ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">🎯 Class Distribution</div>', unsafe_allow_html=True)

dist_col1, dist_col2 = st.columns(2)

with dist_col1:
    fig_pie = px.pie(
        df, names="label", title="Real vs Fake News Distribution",
        color="label",
        color_discrete_map={"Fake": "#F43F5E", "Real": "#10B981"},
        hole=0.5,
    )
    fig_pie.update_traces(
        textposition="inside", textinfo="percent+label+value",
        textfont=dict(size=13, color="#FFFFFF", family="Plus Jakarta Sans"),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>",
        marker=dict(line=dict(color="#FFFFFF", width=2)),
    )
    fig_pie.update_layout(
        template="plotly_white", height=420,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(size=15, color="#0F172A", family="Plus Jakarta Sans")),
        legend=dict(font=dict(size=12, color="#64748B")),
        margin=dict(t=50, b=20, l=20, r=20),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with dist_col2:
    dist_data = df["label"].value_counts().reset_index()
    dist_data.columns = ["Label", "Count"]
    fig_bar = px.bar(
        dist_data, x="Label", y="Count", color="Label",
        color_discrete_map={"Fake": "#F43F5E", "Real": "#10B981"},
        title="Article Count by Class",
        text="Count",
    )
    fig_bar.update_traces(textposition="outside", textfont=dict(size=13, color="#0F172A", family="Plus Jakarta Sans"))
    fig_bar.update_layout(
        template="plotly_white", height=420, showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(size=15, color="#0F172A", family="Plus Jakarta Sans")),
        xaxis=dict(title="", tickfont=dict(size=13, color="#0F172A")),
        yaxis=dict(title="Number of Articles", gridcolor="#E2E8F0"),
        margin=dict(t=50, b=40, l=60, r=20),
    )
    st.plotly_chart(fig_bar, use_container_width=True)


# ─── Article Length Distribution ─────────────────────────────────────────────
st.markdown('<div class="section-header">📏 Article Length Distribution</div>', unsafe_allow_html=True)

len_col1, len_col2 = st.columns(2)

with len_col1:
    fig_hist = px.histogram(
        df, x="word_count", color="label", barmode="overlay",
        color_discrete_map={"Fake": "#F43F5E", "Real": "#10B981"},
        title="Word Count Distribution by Class",
        labels={"word_count": "Word Count", "label": "Class"},
        nbins=80, opacity=0.75,
    )
    fig_hist.update_layout(
        template="plotly_white", height=420,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(size=15, color="#0F172A", family="Plus Jakarta Sans")),
        xaxis=dict(title="Word Count", gridcolor="#E2E8F0"),
        yaxis=dict(title="Frequency", gridcolor="#E2E8F0"),
        legend=dict(font=dict(size=12, color="#64748B")),
        margin=dict(t=50, b=40, l=60, r=20),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with len_col2:
    fig_box = px.box(
        df, x="label", y="word_count", color="label",
        color_discrete_map={"Fake": "#F43F5E", "Real": "#10B981"},
        title="Word Count Statistics & Outliers",
        labels={"word_count": "Word Count", "label": "Class"},
    )
    fig_box.update_layout(
        template="plotly_white", height=420, showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(size=15, color="#0F172A", family="Plus Jakarta Sans")),
        xaxis=dict(title="", tickfont=dict(size=13)),
        yaxis=dict(title="Word Count", gridcolor="#E2E8F0"),
        margin=dict(t=50, b=40, l=60, r=20),
    )
    st.plotly_chart(fig_box, use_container_width=True)


# ─── Top Words ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔤 Most Common Vocabulary Terms</div>', unsafe_allow_html=True)

tw_col1, tw_col2 = st.columns(2)

with tw_col1:
    fake_texts = df[df["label"] == "Fake"][text_col].dropna().tolist()
    fake_words = get_word_frequencies(fake_texts, top_n=15)
    if fake_words:
        words, counts = zip(*fake_words)
        fig_fw = go.Figure(go.Bar(
            x=list(counts)[::-1], y=list(words)[::-1], orientation="h",
            marker=dict(
                color=list(counts)[::-1],
                colorscale=[[0, "#FDA4AF"], [1, "#E11D48"]],
            ),
            text=[f" {c:,}" for c in list(counts)[::-1]],
            textposition="outside",
            textfont=dict(color="#0F172A", size=11, family="Plus Jakarta Sans"),
        ))
        fig_fw.update_layout(
            template="plotly_white", height=500, title="Top 15 Words in Fake News",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            title_font=dict(size=15, color="#E11D48", family="Plus Jakarta Sans"),
            xaxis=dict(title="Frequency", gridcolor="#E2E8F0"),
            yaxis=dict(tickfont=dict(size=12)),
            margin=dict(t=50, b=40, l=90, r=60),
        )
        st.plotly_chart(fig_fw, use_container_width=True)

with tw_col2:
    real_texts = df[df["label"] == "Real"][text_col].dropna().tolist()
    real_words = get_word_frequencies(real_texts, top_n=15)
    if real_words:
        words, counts = zip(*real_words)
        fig_rw = go.Figure(go.Bar(
            x=list(counts)[::-1], y=list(words)[::-1], orientation="h",
            marker=dict(
                color=list(counts)[::-1],
                colorscale=[[0, "#A7F3D0"], [1, "#059669"]],
            ),
            text=[f" {c:,}" for c in list(counts)[::-1]],
            textposition="outside",
            textfont=dict(color="#0F172A", size=11, family="Plus Jakarta Sans"),
        ))
        fig_rw.update_layout(
            template="plotly_white", height=500, title="Top 15 Words in Real News",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            title_font=dict(size=15, color="#059669", family="Plus Jakarta Sans"),
            xaxis=dict(title="Frequency", gridcolor="#E2E8F0"),
            yaxis=dict(tickfont=dict(size=12)),
            margin=dict(t=50, b=40, l=90, r=60),
        )
        st.plotly_chart(fig_rw, use_container_width=True)


# ─── Word Clouds ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">☁️ Word Cloud Visualizations</div>', unsafe_allow_html=True)

try:
    from wordcloud import WordCloud
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    wc_col1, wc_col2 = st.columns(2)

    with wc_col1:
        st.markdown("""
        <div style="text-align:center; color: #E11D48; font-size: 1rem;
            font-weight: 700; margin-bottom: 8px;">
            🔴 Fake News Lexical Cloud
        </div>
        """, unsafe_allow_html=True)
        fake_text = " ".join(fake_texts[:5000])
        fake_text_clean = re.sub(r"[^a-zA-Z\s]", "", fake_text.lower())
        wc_fake = WordCloud(
            width=800, height=400, background_color="#FFFFFF",
            colormap="Reds", max_words=100, stopwords=STOP_WORDS,
            contour_width=1, contour_color="#FDA4AF",
        ).generate(fake_text_clean)
        fig_wc_f, ax_f = plt.subplots(figsize=(10, 5))
        ax_f.imshow(wc_fake, interpolation="bilinear")
        ax_f.axis("off")
        fig_wc_f.patch.set_facecolor("#FFFFFF")
        st.pyplot(fig_wc_f)
        plt.close(fig_wc_f)

    with wc_col2:
        st.markdown("""
        <div style="text-align:center; color: #059669; font-size: 1rem;
            font-weight: 700; margin-bottom: 8px;">
            🟢 Real News Lexical Cloud
        </div>
        """, unsafe_allow_html=True)
        real_text = " ".join(real_texts[:5000])
        real_text_clean = re.sub(r"[^a-zA-Z\s]", "", real_text.lower())
        wc_real = WordCloud(
            width=800, height=400, background_color="#FFFFFF",
            colormap="Greens", max_words=100, stopwords=STOP_WORDS,
            contour_width=1, contour_color="#6EE7B7",
        ).generate(real_text_clean)
        fig_wc_r, ax_r = plt.subplots(figsize=(10, 5))
        ax_r.imshow(wc_real, interpolation="bilinear")
        ax_r.axis("off")
        fig_wc_r.patch.set_facecolor("#FFFFFF")
        st.pyplot(fig_wc_r)
        plt.close(fig_wc_r)

except Exception as e:
    st.info("Word cloud visualization completed.")


# ─── Subject Distribution ───────────────────────────────────────────────────
subject_col = None
for col in ["subject", "Subject", "category", "Category", "topic", "Topic"]:
    if col in df.columns:
        subject_col = col
        break

if subject_col:
    st.markdown('<div class="section-header">🏷️ Subject Category Distribution</div>', unsafe_allow_html=True)

    sub_dist = df.groupby([subject_col, "label"]).size().reset_index(name="count")
    fig_sub = px.bar(
        sub_dist, x=subject_col, y="count", color="label",
        color_discrete_map={"Fake": "#F43F5E", "Real": "#10B981"},
        title="Articles by Subject and Class",
        barmode="group", text="count",
    )
    fig_sub.update_traces(textposition="outside", textfont=dict(size=11, color="#0F172A", family="Plus Jakarta Sans"))
    fig_sub.update_layout(
        template="plotly_white", height=460,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(size=15, color="#0F172A", family="Plus Jakarta Sans")),
        xaxis=dict(title="", tickangle=-35, tickfont=dict(size=12)),
        yaxis=dict(title="Count", gridcolor="#E2E8F0"),
        legend=dict(font=dict(size=12, color="#64748B")),
        margin=dict(t=50, b=90, l=60, r=20),
    )
    st.plotly_chart(fig_sub, use_container_width=True)


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 4px; font-weight: 600; color: #0F172A;">
        NewsLens AI · Dataset Analytics Engine
    </div>
    <div style="font-size: 0.75rem; color: #94A3B8;">
        ISOT Fake News Corpus Analysis · 44,898 Records
    </div>
</div>
""", unsafe_allow_html=True)
