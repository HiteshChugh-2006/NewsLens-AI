# 🔍 NewsLens AI: AI-Based News Article Analysis System
### Powered by Microsoft Azure AI Language & Machine Learning

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Microsoft Azure](https://img.shields.io/badge/Microsoft%20Azure-AI%20Language-0078D4?style=for-the-badge&logo=microsoft-azure)](https://azure.microsoft.com/en-us/products/ai-services/ai-language)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9-orange?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.1-green?style=for-the-badge&logo=xgboost)](https://xgboost.readthedocs.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.67-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

An enterprise-grade, multi-tier news article intelligence and veracity evaluation platform. Combines high-performance, debiased classical Natural Language Processing (LinearSVC achieving **99.08% peak accuracy**) with cloud-native **Microsoft Azure AI Language Cognitive Services** (document-level sentiment distributions and key phrase extraction) and an ACID-compliant **SQLite audit persistence layer**.

Developed as an academic capstone project aligned with the **Microsoft Certified: Azure AI Fundamentals (AI-901)** global curriculum.

---

## 🎯 Executive Overview & Objectives

Modern digital disinformation is rarely just factually incorrect text; it is frequently packaged with emotionally charged sentiment, clickbait rhetoric, and deceptive editorial framing. Traditional fake news classifiers only yield a binary label without explaining narrative sentiment or underlying topics.

**NewsLens AI** resolves these limitations by unifying three complementary dimensions of content evaluation:

1. **Supervised Veracity Classification (Offline ML)**: High-dimensional TF-IDF vectorization (40,000 sublinear unigram/bigram features) with five benchmarked classifiers (LinearSVC, Logistic Regression, Soft Voting Ensemble, XGBoost, and Multinomial Naive Bayes).
2. **Publisher Debiasing Engine**: Automated regular expression sanitization pipeline that strips wire agency datelines (`Reuters`, `AP`), author watermarks, and social media handles from training corpora—preventing catastrophic "Clever Hans" artifact leakage and restoring genuine out-of-domain generalization.
3. **Microsoft Azure AI Language (Sentiment & Key Phrases)**: Cloud-native cognitive service evaluating document emotional polarity (Positive, Neutral, Negative confidence distributions) strictly independently from truthfulness, alongside automated salient entity and topic discovery.
4. **Persistent Audit Database (`news_analysis.db`)**: Local, zero-configuration, ACID-compliant relational SQLite database tracking every evaluated article with parameterized SQL queries, serialized JSON confidence payloads, and microsecond audit timestamps.
5. **Microsoft Fluent Multi-Page Interface**: A modern 6-page web dashboard adhering to Microsoft Fluent Design principles (emerald accents `#059669`, clean cards, responsive Plotly charts, and linear feature explainability).

---

## 📐 Multi-Tier System Architecture

```
                                ┌───────────────────────────┐
                                │    User Article Input     │
                                │ (Direct Paste or Samples) │
                                └─────────────┬─────────────┘
                                              │
                   ┌──────────────────────────┴──────────────────────────┐
                   │                                                     │
                   ▼                                                     ▼
    [ Classical Machine Learning Branch ]             [ Microsoft Azure AI Language Branch ]
┌───────────────────────────────────────┐             ┌────────────────────────────────────┐
│ 1. Regex Publisher Debiasing Engine   │             │ 1. AzureKeyCredential & Endpoint   │
│    (Strips datelines, credits, marks) │             │ 2. Word-Boundary Truncation Guard  │
│ 2. NLTK Tokenization & Lemmatization  │             │    (Strict 5,000 character limit)  │
│ 3. 40,000-dim Sublinear TF-IDF Matrix │             │ 3. azure-ai-textanalytics Client   │
│ 4. Calibrated Model Inference:        │             │ 4. Parallel Cognitive Service APIs:│
│    • LinearSVC (Champion: 99.08%)     │             │    • analyze_sentiment()           │
│    • Logistic Regression (98.49%)     │             │    • extract_key_phrases()         │
│    • Soft Voting Ensemble (98.42%)    │             │                                    │
│ Output: FAKE/REAL + Confidence Score  │             │ Output: Tone Scores + Salient Tags │
└──────────────────┬────────────────────┘             └─────────────────┬──────────────────┘
                   │                                                     │
                   └──────────────────────────┬──────────────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │     Consolidated Analysis       │
                             └────────────────┬────────────────┘
                                              │
                   ┌──────────────────────────┴──────────────────────────┐
                   ▼                                                     ▼
   ┌───────────────────────────────┐                     ┌───────────────────────────────┐
   │   SQLite Database Storage     │                     │     Streamlit Dashboard       │
   │   (`news_analysis.db`)        │                     │  (Microsoft Fluent Light UI)  │
   │                               │                     │                               │
   │ • Parameterized SQL INSERT    │                     │ • Real-Time Probability Gauge │
   │ • JSON Serialized Confidences │                     │ • Azure Sentiment Stacked Bar │
   │ • Microsecond Timestamps      │                     │ • Salient Entity Phrase Tags  │
   │ • Historical Query & Audit    │                     │ • Word Attribution Breakdown  │
   └───────────────────────────────┘                     └───────────────────────────────┘
```

---

## 📊 Empirical Model Performance Benchmarks

All models were evaluated on the **ISOT Fake News Dataset** (44,898 articles) following regularized publisher debiasing using an 80/20 train/test split (8,980 unseen test articles) under 5-fold cross-validation:

| Machine Learning Algorithm | Test Accuracy | Precision | Recall | F1-Score | ROC-AUC | 5-Fold CV F1 | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LinearSVC (Platt Calibrated) 🏆** | **99.08%** | **0.9908** | **0.9915** | **0.9912** | **0.9993** | **0.9910** | **< 2 ms** |
| **Logistic Regression (L2)** | **98.49%** | 0.9872 | 0.9838 | 0.9855 | 0.9983 | 0.9849 | < 1 ms |
| **Soft Voting Ensemble (Meta)** | **98.42%** | 0.9867 | 0.9830 | 0.9848 | 0.9982 | 0.9839 | ~ 4 ms |
| **XGBoost Classifier (hist)** | **95.53%** | 0.9555 | 0.9593 | 0.9574 | 0.9901 | 0.9561 | ~ 15 ms |
| **Multinomial Naive Bayes** | **95.12%** | 0.9514 | 0.9555 | 0.9535 | 0.9882 | 0.9552 | < 1 ms |

---

## 🛡️ Publisher Debiasing & Out-of-Domain Generalization

Standard ISOT models suffer from catastrophic "Clever Hans" watermark leakage: because authentic articles begin with `(Reuters) -`, naive models use the agency name as a shortcut. When evaluated against authentic contemporary news lacking wire datelines, un-debiased models falsely flag real news as fake.

Our regex-driven sanitization pipeline excises wire headers, author watermarks, and agency stop words:

| Test News Article Snippet | Actual Status | Before Debiasing | After Debiasing (NewsLens AI) |
| :--- | :---: | :---: | :---: |
| *India made history on 23 August 2023 when Chandrayaan-3 successfully touched down on the lunar south pole...* | **REAL (ISRO News)** | ❌ FAKE (99.8% False Certainty) | **✅ REAL (72.9% Calibrated Confidence)** |
| *The House passed a comprehensive $1.9 trillion relief package delivering direct assistance to families...* | **REAL (Policy Record)** | ✅ REAL (99.9% Confidence) | **✅ REAL (99.4% Calibrated Confidence)** |
| *BREAKING: Secret underground alien military base discovered beneath city hall! Whistleblowers confirm...* | **FAKE (Conspiracy)** | ❌ FAKE (99.9% Confidence) | **❌ FAKE (99.9% Calibrated Confidence)** |

---

## 📁 Repository Structure

```
NewsLens-AI/
│
├── dataset/                         # Training Corpus (44,898 articles)
│   ├── Fake.csv                     # 23,481 Fake news records
│   └── True.csv                     # 21,417 Real news records (Reuters)
│
├── models/                          # Serialized Model & Vectorizer Artifacts
│   ├── best_model.joblib            # Champion Calibrated LinearSVC Model
│   ├── tfidf_vectorizer.joblib      # 40,000-feature TF-IDF Vectorizer
│   ├── logistic_regression.joblib
│   ├── soft_voting_ensemble.joblib
│   ├── multinomial_nb.joblib
│   └── xgboost_classifier.joblib
│
├── reports/                         # Performance Visualizations & Evaluation Data
│   ├── model_comparison.csv         # Verified multi-metric comparison table
│   ├── confusion_matrix_*.png       # Confusion matrices for all classifiers
│   ├── roc_curve_*.png              # ROC curves with AUC values
│   ├── feature_importance_*.png     # Top salient word attribution charts
│   └── model_comparison.png         # Multi-metric comparative bar chart
│
├── pages/                           # Streamlit Multi-Page UI Modules
│   ├── 1_News_Detection.py          # 🔍 Live Multi-AI Analysis (ML + Azure + DB)
│   ├── 2_Analytics.py               # 📊 Training dataset analytics & class distributions
│   ├── 3_Model_Performance.py       # 📈 Interactive model benchmark comparison
│   ├── 4_Explainability.py          # 🧠 Word attribution & feature weights
│   ├── 5_About_Project.py           # ℹ️ Architecture flowcharts & documentation
│   └── 6_Analysis_History.py        # 🗄️ SQLite audit record inspector & management
│
├── src/                             # Core Backend Logic
│   ├── __init__.py
│   ├── azure_language.py            # Azure AI Language SDK client wrapper
│   ├── database.py                  # SQLite AnalysisDatabase class with parameterized SQL
│   ├── feature_engineering.py       # FeatureEngineer TF-IDF vectorizer class
│   ├── predict.py                   # NewsPredictor class with explainability
│   ├── preprocessing.py             # TextPreprocessor class with debiasing regexes
│   ├── styles.py                    # Microsoft Fluent Light Theme CSS injection
│   └── train.py                     # 5-fold cross-validation training pipeline
│
├── docs/                            # Official Academic Documentation
│   ├── Industrial_Internship_Report.docx # Official Chandigarh University Word Report (27 pages)
│   ├── INDUSTRIAL_INTERNSHIP_REPORT.md   # Complete Markdown report draft
│   └── PROJECT_REPORT.md                 # Detailed technical specifications
│
├── app.py                           # Application entrypoint & executive dashboard
├── build_standard_cu_report.py      # Automated generator for university Word report
├── main.py                          # End-to-end model training pipeline script
├── news_analysis.db                 # ACID-compliant local SQLite audit database
├── test_system.py                   # Automated test suite (10 validation scenarios)
├── requirements.txt                 # Pinned project dependencies
├── .env.example                     # Environment template for Azure credentials
└── README.md                        # Project documentation
```

---

## ⚡ Quickstart Guide

### 1. Clone the Repository & Set Up Environment

```bash
git clone https://github.com/HiteshChugh-2006/CodeAlpha_Fake-News-Detection-System.git
cd CodeAlpha_Fake-News-Detection-System

# Create and activate Python virtual environment
python -m venv .venv
source .venv/bin/activate       # On Linux/macOS
.venv\Scripts\activate          # On Windows (PowerShell)

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Microsoft Azure AI Language Credentials (Optional)

Create a `.env` file in the root directory (based on `.env.example`):

```ini
AZURE_LANGUAGE_ENDPOINT=https://<your-language-resource>.cognitiveservices.azure.com/
AZURE_LANGUAGE_KEY=<your-azure-api-secret-key>
```

> **Note:** If Azure credentials are not provided, NewsLens AI automatically activates **Graceful Offline Mode**. Machine learning classification, explainability, and SQLite logging remain 100% operational.

### 3. Launch the Streamlit Web Application

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

### 4. Execute the Automated Test Suite

```bash
python test_system.py
```

Validates all 10 unit and integration test scenarios (ML inference, out-of-domain debiasing, edge cases, Azure fallbacks, and SQLite CRUD operations).

---

## 🎓 Academic Project Report (Chandigarh University)

This project includes the official **Chandigarh University Industrial Internship Report** formatted in accordance with university template guidelines:

- **Word Document:** [`docs/Industrial_Internship_Report.docx`](docs/Industrial_Internship_Report.docx)
- **Formatting Standards:** A4 paper, Times New Roman 12pt, 1.5 line spacing, 18pt bold chapter headings.
- **Main Content Ceiling:** **Strictly 27 pages** (conforming to the university's 25 to 30 page ceiling).
- **Weekly Report:** Prescribed **Appendix 5** tabular layout across 6 weeks (30 daily entries) documenting real certification learning and technical implementation without fabricated attendance.

---

## 👤 Author & Certification Context

- **Candidate:** Hitesh Chugh
- **Program:** Bachelor of Engineering in Computer Science & Engineering (AIML)
- **Institution:** Department of Computer Science & Engineering, University Institute of Engineering, Chandigarh University, Gharuan
- **Certification Curriculum:** Aligned with [Microsoft Certified: Azure AI Fundamentals (AI-901)](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/)
- **GitHub:** [@HiteshChugh-2006](https://github.com/HiteshChugh-2006)
- **LinkedIn:** [Hitesh Chugh](https://www.linkedin.com/in/hitesh-chugh-a80170320/)
