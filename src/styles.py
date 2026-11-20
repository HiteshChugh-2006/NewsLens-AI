"""
NewsLens AI - Microsoft Fluent Design System & Light Theme CSS
==============================================================
Inspired by the Microsoft Streamlit UI Template repository.
Features:
  - Clean light theme canvas (#F8FAFC)
  - Executive emerald accents (#059669, #10B981)
  - Refined white elevated cards with soft shadows
  - Microsoft Fluent typography (Plus Jakarta Sans & Segoe UI)
  - Subtle micro-interactions and transitions
"""

def get_custom_css() -> str:
    return """
<style>
/* ===== Microsoft Fluent & Plus Jakarta Sans Typography ===== */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --primary-emerald: #059669;
    --emerald-light: #10B981;
    --emerald-dark: #047857;
    --emerald-bg: rgba(16, 185, 129, 0.08);
    --emerald-border: rgba(16, 185, 129, 0.25);
    
    --azure-blue: #0078D4;
    --azure-bg: rgba(0, 120, 212, 0.08);
    --azure-border: rgba(0, 120, 212, 0.25);
    
    --rose-accent: #E11D48;
    --rose-bg: rgba(225, 29, 72, 0.08);
    --rose-border: rgba(225, 29, 72, 0.25);
    
    --amber-accent: #D97706;
    --amber-bg: rgba(217, 119, 6, 0.08);
    --amber-border: rgba(217, 119, 6, 0.25);
    
    --purple-accent: #7C3AED;
    --purple-bg: rgba(124, 58, 237, 0.08);
    --purple-border: rgba(124, 58, 237, 0.25);
    
    --bg-canvas: #F8FAFC;
    --bg-card: #FFFFFF;
    --border-light: #E2E8F0;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #94A3B8;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--bg-canvas) !important;
    color: var(--text-primary) !important;
}

/* ===== Sidebar Styling ===== */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid var(--border-light) !important;
    box-shadow: 2px 0 12px rgba(15, 23, 42, 0.03);
}

[data-testid="stSidebarNav"] {
    padding-top: 8px;
}

[data-testid="stSidebarNav"] span {
    font-weight: 500;
    color: var(--text-secondary);
}

[data-testid="stSidebarNav"] a:hover {
    background-color: var(--emerald-bg) !important;
    border-radius: 8px;
}

[data-testid="stSidebarNav"] [aria-current="page"] {
    background-color: var(--emerald-bg) !important;
    border-left: 3px solid var(--primary-emerald) !important;
    border-radius: 4px 8px 8px 4px;
}

[data-testid="stSidebarNav"] [aria-current="page"] span {
    color: var(--emerald-dark) !important;
    font-weight: 700 !important;
}

/* ===== Header cleanup ===== */
[data-testid="stHeader"] {
    background-color: rgba(248, 250, 252, 0.8) !important;
    backdrop-filter: blur(10px);
}

/* ===== Elevated KPI Cards ===== */
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    padding: 22px 18px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.02);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #059669, #10B981, #34D399);
    border-radius: 14px 14px 0 0;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.1), 0 8px 10px -6px rgba(5, 150, 105, 0.04);
    border-color: var(--emerald-border);
}

.kpi-icon {
    font-size: 1.8rem;
    margin-bottom: 6px;
    display: inline-block;
}

.kpi-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: var(--emerald-dark);
    line-height: 1.15;
    margin: 4px 0;
    letter-spacing: -0.5px;
}

.kpi-label {
    font-size: 0.76rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
    margin-top: 4px;
}

/* ===== Hero Section ===== */
.hero-container {
    text-align: center;
    padding: 36px 20px 24px;
    position: relative;
    background: radial-gradient(circle at 50% 0%, rgba(16, 185, 129, 0.09) 0%, transparent 65%);
    border-radius: 20px;
    margin-bottom: 20px;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #065F46 0%, #059669 45%, #0D9488 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
    line-height: 1.15;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-secondary);
    max-width: 760px;
    margin: 0 auto;
    line-height: 1.65;
    font-weight: 400;
}

.hero-badges-container {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 16px;
}

/* ===== Refined Pill Badges ===== */
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--emerald-bg);
    border: 1px solid var(--emerald-border);
    border-radius: 50px;
    padding: 5px 16px;
    font-size: 0.74rem;
    color: var(--emerald-dark);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 700;
}

.hero-badge-azure {
    background: var(--azure-bg);
    border-color: var(--azure-border);
    color: var(--azure-blue);
}

.hero-badge-sqlite {
    background: rgba(100, 116, 139, 0.08);
    border-color: rgba(100, 116, 139, 0.25);
    color: #334155;
}

/* Tech badges */
.tech-badge {
    display: inline-block; padding: 6px 16px; margin: 4px;
    border-radius: 50px; font-size: 0.8rem; font-weight: 600;
    background: var(--emerald-bg); color: var(--emerald-dark);
    border: 1px solid var(--emerald-border);
    transition: all 0.2s ease;
}
.tech-badge:hover { background: rgba(16, 185, 129, 0.18); transform: translateY(-1px); }

.tech-badge-azure { background: var(--azure-bg); color: var(--azure-blue); border-color: var(--azure-border); }
.tech-badge-azure:hover { background: rgba(0, 120, 212, 0.16); }

.tech-badge-green { background: rgba(16, 185, 129, 0.12); color: #047857; border-color: rgba(16, 185, 129, 0.3); }
.tech-badge-green:hover { background: rgba(16, 185, 129, 0.2); }

.tech-badge-orange { background: var(--amber-bg); color: var(--amber-accent); border-color: var(--amber-border); }
.tech-badge-orange:hover { background: rgba(217, 119, 6, 0.16); }

.tech-badge-red { background: var(--rose-bg); color: var(--rose-accent); border-color: var(--rose-border); }
.tech-badge-red:hover { background: rgba(225, 29, 72, 0.16); }

.tech-badge-purple { background: var(--purple-bg); color: var(--purple-accent); border-color: var(--purple-border); }
.tech-badge-purple:hover { background: rgba(124, 58, 237, 0.16); }

/* ===== Section Headers ===== */
.section-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 32px 0 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(16, 185, 129, 0.2);
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ===== Feature & Capability Cards ===== */
.feature-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    padding: 24px 20px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    transition: all 0.25s ease;
    min-height: 190px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}

.feature-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.08), 0 8px 10px -6px rgba(5, 150, 105, 0.03);
    border-color: var(--emerald-border);
}

.feature-icon {
    font-size: 2rem;
    margin-bottom: 12px;
}

.feature-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
}

.feature-desc {
    font-size: 0.84rem;
    color: var(--text-secondary);
    line-height: 1.55;
}

/* ===== Pipeline Step Cards ===== */
.pipeline-step {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 18px 12px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
    transition: all 0.2s ease;
    min-height: 165px;
    position: relative;
}

.pipeline-step:hover {
    border-color: var(--emerald-border);
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(5, 150, 105, 0.06);
}

.pipeline-step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: linear-gradient(135deg, #059669, #10B981);
    color: #FFFFFF;
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 8px;
}

/* Model card */
.model-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 14px; padding: 22px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    transition: all 0.25s ease; min-height: 280px;
}
.model-card:hover {
    border-color: var(--emerald-border);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(5, 150, 105, 0.08);
}

/* ===== Prediction & Verdict Badges ===== */
.prediction-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 18px 36px;
    border-radius: 14px;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    margin: 12px 0;
}

.fake-badge {
    background: #FFF1F2;
    color: #BE123C;
    border: 2px solid #FDA4AF;
    box-shadow: 0 6px 20px rgba(225, 29, 72, 0.12);
}

.real-badge {
    background: #ECFDF5;
    color: #047857;
    border: 2px solid #6EE7B7;
    box-shadow: 0 6px 20px rgba(5, 150, 105, 0.12);
}

/* ===== Word contribution highlighting ===== */
.word-positive {
    background: #FFF1F2; color: #E11D48;
    padding: 2px 6px; border-radius: 4px; font-weight: 600;
    border-bottom: 2px solid #FDA4AF;
}
.word-negative {
    background: #ECFDF5; color: #047857;
    padding: 2px 6px; border-radius: 4px; font-weight: 600;
    border-bottom: 2px solid #6EE7B7;
}
.word-neutral { color: #64748B; }

/* ===== Tags ===== */
.phrase-tag {
    display: inline-flex;
    align-items: center;
    padding: 5px 14px;
    margin: 4px;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 600;
    background: var(--emerald-bg);
    color: var(--emerald-dark);
    border: 1px solid var(--emerald-border);
    transition: all 0.2s ease;
}

.phrase-tag:hover {
    background: rgba(16, 185, 129, 0.16);
    transform: translateY(-1px);
}

.word-tag {
    display: inline-block;
    padding: 4px 12px;
    margin: 3px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
    background: #F1F5F9;
    color: var(--text-primary);
    border: 1px solid var(--border-light);
}

.word-tag-fake {
    background: #FFF1F2;
    color: #BE123C;
    border-color: #FECDD3;
}

.word-tag-real {
    background: #ECFDF5;
    color: #047857;
    border-color: #A7F3D0;
}

/* ===== Detail & Info Containers ===== */
.info-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    margin-bottom: 16px;
}

.sidebar-brand-card {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(248, 250, 252, 0.5) 100%);
    border: 1px solid var(--emerald-border);
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    margin-bottom: 16px;
}

/* ===== Divider ===== */
.gradient-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.3), rgba(0, 120, 212, 0.2), transparent);
    border: none;
    margin: 22px 0;
}

/* ===== Footer ===== */
.footer {
    text-align: center;
    padding: 32px 20px 20px;
    margin-top: 40px;
    border-top: 1px solid var(--border-light);
    color: var(--text-muted);
    font-size: 0.82rem;
}

.footer a {
    color: var(--primary-emerald);
    text-decoration: none;
    font-weight: 500;
}

.footer a:hover {
    text-decoration: underline;
}

/* ===== Streamlit Components Polish ===== */
div[data-testid="stMetricValue"] {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--emerald-dark);
}

.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    border: 1px solid var(--border-light) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    border-color: var(--primary-emerald) !important;
    color: var(--primary-emerald) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #059669 0%, #10B981 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 2px 6px rgba(5, 150, 105, 0.25) !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 16px rgba(5, 150, 105, 0.35) !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border-light);
    border-radius: 10px;
    overflow: hidden;
}
</style>
"""
