"""
NewsLens AI - Model Performance Evaluation Page
================================================
Comprehensive model evaluation with comparison charts,
confusion matrices, ROC curves, and detailed metrics.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import sys
import glob

# ─── Add project root to path ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.styles import get_custom_css

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Model Performance | NewsLens AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Microsoft Fluent Light Theme CSS ────────────────────────────────────────
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ─── Helper Functions ────────────────────────────────────────────────────────
def load_comparison_data():
    """Load model comparison CSV if available (always reads latest from disk)."""
    csv_path = os.path.join(BASE_DIR, "reports", "model_comparison.csv")
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            return df
        except Exception:
            return None
    return None


def find_report_images():
    """Find all generated report images in the reports/ directory."""
    reports_dir = os.path.join(BASE_DIR, "reports")
    if not os.path.exists(reports_dir):
        return {}

    image_patterns = {
        "confusion_matrix": "confusion_matrix_*.png",
        "roc_curve": "roc_curve_*.png",
        "model_comparison": "model_comparison*.png",
        "feature_importance": "feature_importance*.png",
    }

    found = {}
    for key, pattern in image_patterns.items():
        matches = glob.glob(os.path.join(reports_dir, pattern))
        if matches:
            found[key] = sorted(matches)

    return found


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">📈</div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #047857;">
            NewsLens AI
        </div>
        <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">
            Model Benchmarks
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Page Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 16px 0 8px;">
    <div style="font-size: 2.4rem; font-weight: 800;
        background: linear-gradient(135deg, #065F46 0%, #059669 50%, #0D9488 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        📈 Model Performance & Comparative Evaluation
    </div>
    <div style="color: #64748B; font-size: 1rem; margin-top: 6px;">
        Empirical evaluation metrics, confusion matrices, ROC curves, and multi-model benchmark analysis
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# ─── Load Comparison Data ────────────────────────────────────────────────────
df = load_comparison_data()

if df is None or df.empty:
    st.markdown(f"""
    <div class="info-card" style="text-align: center; padding: 36px 20px;">
        <div style="font-size: 2.8rem; margin-bottom: 8px;">📊</div>
        <div style="font-size: 1.2rem; font-weight: 700; color: #E11D48; margin-bottom: 8px;">
            No Evaluation Reports Found
        </div>
        <div style="color: #64748B; font-size: 0.9rem; max-width: 500px; margin: 0 auto;">
            Please run <code>python main.py</code> first to train models and generate the comparison report in <code>reports/model_comparison.csv</code>.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Identify model column and metric columns dynamically
    model_col = None
    for c in df.columns:
        cl = c.lower().strip()
        if cl in ["model_name", "model", "classifier", "name", "algorithm", "modelname"]:
            model_col = c
            break

    if model_col is None:
        # Fallback to the first non-numeric column
        non_numeric = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
        if non_numeric:
            model_col = non_numeric[0]
        elif len(df.columns) > 0:
            model_col = df.columns[0]

    metric_cols = [c for c in df.columns if c != model_col and pd.api.types.is_numeric_dtype(df[c])]

    # Find best model
    best_acc = 0.0
    best_f1 = 0.0
    best_model_name = "N/A"

    acc_col = None
    f1_col = None
    for c in df.columns:
        cl = c.lower().strip()
        if "acc" in cl:
            acc_col = c
        if cl == "f1" or (cl.startswith("f1") and "cv" not in cl):
            f1_col = c

    if f1_col is None:
        for c in df.columns:
            if "f1" in c.lower():
                f1_col = c
                break

    if acc_col:
        best_acc_idx = df[acc_col].idxmax()
        best_acc = df.loc[best_acc_idx, acc_col]
        if model_col:
            best_model_name = str(df.loc[best_acc_idx, model_col])

    if f1_col:
        best_f1 = df[f1_col].max()

    # ─── KPI Row ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🏆 Benchmark Highlights</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">🥇</span>
            <div class="kpi-value" style="font-size: 1.35rem; padding-top: 6px; color: #047857;">{best_model_name}</div>
            <div class="kpi-label">Top Ranked Model</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        acc_str = f"{best_acc:.2%}" if isinstance(best_acc, float) and best_acc <= 1 else f"{best_acc}%"
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">🎯</span>
            <div class="kpi-value">{acc_str}</div>
            <div class="kpi-label">Peak Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        f1_str = f"{best_f1:.2%}" if isinstance(best_f1, float) and best_f1 <= 1 else f"{best_f1}%"
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">⚡</span>
            <div class="kpi-value">{f1_str}</div>
            <div class="kpi-label">Peak F1-Score</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">🤖</span>
            <div class="kpi-value" style="color: #334155;">{len(df)}</div>
            <div class="kpi-label">Models Compared</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Model Comparison Chart ──────────────────────────────────────────
    st.markdown('<div class="section-header">📊 Multi-Metric Comparison</div>', unsafe_allow_html=True)

    if model_col and metric_cols:
        colors = ["#059669", "#0D9488", "#0284C7", "#6366F1", "#D97706", "#E11D48", "#10B981"]

        fig_comp = go.Figure()
        for i, metric in enumerate(metric_cols):
            fig_comp.add_trace(go.Bar(
                name=metric,
                x=df[model_col].tolist(),
                y=df[metric].tolist(),
                marker_color=colors[i % len(colors)],
                text=[f"{v:.4f}" for v in df[metric]],
                textposition="outside",
                textfont=dict(size=11, color="#0F172A", family="Plus Jakarta Sans"),
            ))

        fig_comp.update_layout(
            template="plotly_white", height=450, barmode="group",
            title=dict(text="Model Performance Across Standard Metrics", font=dict(size=16, color="#0F172A", family="Plus Jakarta Sans")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="", tickfont=dict(size=13, color="#0F172A")),
            yaxis=dict(title="Score (0.0 - 1.0)", gridcolor="#E2E8F0",
                      range=[0, max(df[metric_cols].max().max() * 1.15, 1.05)]),
            legend=dict(orientation="h", y=-0.18, font=dict(size=12, color="#64748B")),
            margin=dict(t=50, b=80, l=60, r=20),
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        # Radar chart
        st.markdown('<div class="section-header">🕸️ Performance Radar Profile</div>', unsafe_allow_html=True)

        if len(metric_cols) >= 3:
            fig_radar = go.Figure()
            radar_colors = ["#059669", "#0284C7", "#D97706", "#8B5CF6"]

            for i, idx in enumerate(df.index):
                m_name = df.loc[idx, model_col] if model_col else f"Model {i+1}"
                values = df.loc[idx, metric_cols].tolist()
                values.append(values[0])
                cats = metric_cols + [metric_cols[0]]

                fig_radar.add_trace(go.Scatterpolar(
                    r=values, theta=cats, fill="toself",
                    name=m_name,
                    line=dict(color=radar_colors[i % len(radar_colors)], width=2.5),
                    fillcolor=f"rgba({int(radar_colors[i % len(radar_colors)][1:3], 16)}, "
                              f"{int(radar_colors[i % len(radar_colors)][3:5], 16)}, "
                              f"{int(radar_colors[i % len(radar_colors)][5:7], 16)}, 0.08)",
                ))

            fig_radar.update_layout(
                template="plotly_white", height=450,
                title=dict(text="Radar Dimensional Analysis", font=dict(size=16, color="#0F172A", family="Plus Jakarta Sans")),
                paper_bgcolor="rgba(0,0,0,0)",
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0.9, 1.0], gridcolor="#E2E8F0"),
                    angularaxis=dict(gridcolor="#E2E8F0"),
                ),
                legend=dict(font=dict(size=12, color="#64748B")),
                margin=dict(t=50, b=40, l=60, r=60),
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    # ─── Detailed Metrics Table ──────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Detailed Metrics Benchmark Table</div>', unsafe_allow_html=True)

    def highlight_best(s):
        styles = [""] * len(s)
        try:
            numeric_s = pd.to_numeric(s, errors="coerce")
            if numeric_s.notna().any():
                best_idx = numeric_s.idxmax()
                styles[s.index.get_loc(best_idx)] = (
                    "background-color: rgba(16, 185, 129, 0.15); "
                    "color: #047857; font-weight: 700;"
                )
        except Exception:
            pass
        return styles

    styled_df = df.style.apply(highlight_best, axis=0)
    st.dataframe(styled_df, use_container_width=True, height=220)

    # ─── Per-metric bar charts ───────────────────────────────────────────
    if model_col and len(metric_cols) > 1:
        st.markdown('<div class="section-header">📊 Individual Metric Leaderboards</div>', unsafe_allow_html=True)

        for row_start in range(0, len(metric_cols), 2):
            cols = st.columns(2)
            for j in range(2):
                idx = row_start + j
                if idx < len(metric_cols):
                    metric = metric_cols[idx]
                    with cols[j]:
                        sorted_df = df.sort_values(metric, ascending=True)
                        colors_list = ["#E2E8F0"] * len(sorted_df)
                        colors_list[-1] = "#059669"

                        fig_m = go.Figure(go.Bar(
                            x=sorted_df[metric].tolist(),
                            y=sorted_df[model_col].tolist(),
                            orientation="h",
                            marker_color=colors_list,
                            text=[f"{v:.4f}" for v in sorted_df[metric]],
                            textposition="outside",
                            textfont=dict(size=11, color="#0F172A", family="Plus Jakarta Sans"),
                        ))
                        fig_m.update_layout(
                            template="plotly_white", height=260,
                            title=dict(text=metric, font=dict(size=14, color="#047857", family="Plus Jakarta Sans")),
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            xaxis=dict(gridcolor="#E2E8F0", range=[0.9, 1.02]),
                            yaxis=dict(tickfont=dict(size=11, color="#0F172A")),
                            margin=dict(t=40, b=20, l=120, r=40),
                        )
                        st.plotly_chart(fig_m, use_container_width=True)


# ─── Report Images ───────────────────────────────────────────────────────────
report_images = find_report_images()

if report_images:
    st.markdown('<div class="section-header">🖼️ Exported Evaluation Visualizations</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Confusion Matrices", "ROC Curves", "Comparative Plots"])

    with tabs[0]:
        if "confusion_matrix" in report_images:
            cols = st.columns(min(len(report_images["confusion_matrix"]), 2))
            for i, img_path in enumerate(report_images["confusion_matrix"]):
                with cols[i % len(cols)]:
                    m_label = os.path.basename(img_path).replace("confusion_matrix_", "").replace(".png", "").replace("_", " ").title()
                    st.markdown(f"<div style='font-weight:700; color:#047857; margin-bottom:6px;'>{m_label}</div>", unsafe_allow_html=True)
                    st.image(img_path, use_container_width=True)
        else:
            st.info("No confusion matrix images found.")

    with tabs[1]:
        if "roc_curve" in report_images:
            cols = st.columns(min(len(report_images["roc_curve"]), 2))
            for i, img_path in enumerate(report_images["roc_curve"]):
                with cols[i % len(cols)]:
                    m_label = os.path.basename(img_path).replace("roc_curve_", "").replace(".png", "").replace("_", " ").title()
                    st.markdown(f"<div style='font-weight:700; color:#047857; margin-bottom:6px;'>{m_label}</div>", unsafe_allow_html=True)
                    st.image(img_path, use_container_width=True)
        else:
            st.info("No ROC curve images found.")

    with tabs[2]:
        if "model_comparison" in report_images:
            for img_path in report_images["model_comparison"]:
                st.image(img_path, use_container_width=True)
        else:
            st.info("No comparative plot images found.")


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 4px; font-weight: 600; color: #0F172A;">
        NewsLens AI · Model Evaluation Engine
    </div>
    <div style="font-size: 0.75rem; color: #94A3B8;">
        Cross-validated machine learning performance metrics & classification reports
    </div>
</div>
""", unsafe_allow_html=True)
