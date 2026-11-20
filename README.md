# 📰 AI-Based News Article Analysis System Using Microsoft Azure AI

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Microsoft Azure](https://img.shields.io/badge/Microsoft%20Azure-AI%20Language-0078D4?style=for-the-badge&logo=microsoft-azure)](https://azure.microsoft.com/en-us/products/ai-services/ai-language)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3-orange?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-green?style=for-the-badge&logo=xgboost)](https://xgboost.readthedocs.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

An end-to-end multi-tier intelligence platform designed for news credibility assessment, affective tone analysis, and thematic extraction. Developed as an enhanced academic project for the **Industrial Internship Examination** aligned with the **Microsoft Certified: Azure AI Fundamentals (AI-901)** curriculum.

---

## 🎯 Executive Summary & Objectives

Modern digital misinformation is rarely just false text; it is frequently packaged with charged sentiment, sensational phrasing, and deceptive editorial framing. Traditional fake news classifiers only yield a binary label without explaining narrative sentiment or underlying topics.

This project enhances an existing high-accuracy Machine Learning Fake News Detection System into a comprehensive **AI-Based News Article Analysis System** by combining:

1. **Classical Machine Learning Classifier**: TF-IDF feature extraction with an ensemble of evaluated algorithms (Logistic Regression, Multinomial Naive Bayes, Linear SVC, and XGBoost achieving 99.81% accuracy) to predict whether news is **REAL** or **FAKE**.
2. **Microsoft Azure AI Language (Sentiment Analysis)**: Cloud Cognitive Service analyzing document-level emotional polarity (Positive, Neutral, Negative) and confidence scores, treated strictly independently from truthfulness.
3. **Microsoft Azure AI Language (Key Phrase Extraction)**: Cloud Cognitive Service automatically isolating the salient entities, keywords, and topics of the article.
4. **Local SQLite Database (`news_analysis.db`)**: Persistent, zero-configuration, ACID-compliant audit database storing all inputs, ML predictions, Azure sentiment confidences, and extracted keywords with parameterized SQL queries.
5. **Interactive Streamlit Dashboard**: A professional 6-page dark-mode web dashboard featuring interactive Plotly visualizations, live SQLite KPI tracking, word-level explainability, and database record inspection.

---

## 📐 System Architecture

The following diagram illustrates the flow from article ingestion to dual-path AI inference, persistence, and presentation:

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
  │ 1. NLTK Text Cleaning & Tokenization  │             │ 1. Authenticate with Endpoint & Key│
  │ 2. Stopword Removal & Lemmatization   │             │ 2. Payload Validation & Truncation │
  │ 3. 50,000-dim TF-IDF Feature Mapping  │             │ 3. azure-ai-textanalytics Client   │
  │ 4. Calibrated Model Inference         │             │ 4. Parallel Service Calls:         │
  │    (XGBoost / LinearSVC / LogReg)     │             │    • analyze_sentiment()           │
  │                                       │             │    • extract_key_phrases()         │
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
     │   (`news_analysis.db`)        │                     │   (Multi-Page UI & Plotly)    │
     │                               │                     │                               │
     │ • Parameterized INSERT        │                     │ • Real-time Prediction Gauges │
     │ • JSON Confidence Dicts       │                     │ • Azure Sentiment Stacked Bar │
     │ • Audit Timestamps            │                     │ • Interactive Phrase Tags     │
     │ • CRUD & Historical Analytics │                     │ • Word-Level Feature Bar Chart│
     └───────────────────────────────┘                     └───────────────────────────────┘
```

---

## 📁 Repository Structure

```
CodeAlpha_Fake-News-Detection-System/
│
├── dataset/                    # Training Corpus (44,898 articles)
│   ├── Fake.csv                # 23,481 Fake news records
│   └── True.csv                # 21,417 Real news records (Reuters)
│
├── models/                     # Trained Model & Vectorizer Artifacts
│   ├── best_model.joblib       # Serialized best model (XGBClassifier)
│   ├── tfidf_vectorizer.joblib # Serialized TF-IDF vectorizer (50k features)
│   ├── logistic_regression.joblib
│   ├── multinomial_nb.joblib
│   └── linear_svc.joblib
│
├── reports/                    # Generated Performance & Metric Reports
│   ├── model_comparison.csv    # Accuracy, Precision, Recall, F1, ROC-AUC
│   ├── confusion_matrix_*.png  # Model confusion matrices
│   ├── roc_curve_*.png         # ROC-AUC curves
│   └── model_comparison.png    # Bar chart performance comparison
│
├── pages/                      # Streamlit Multi-Page Application
│   ├── 1_News_Detection.py     # 🔍 Unified Analysis (ML + Azure + DB)
│   ├── 2_Analytics.py          # 📊 Training dataset analytics & word clouds
│   ├── 3_Model_Performance.py  # 📈 Comprehensive model comparison metrics
│   ├── 4_Explainability.py     # 🧠 Word attribution & feature importance
│   ├── 5_About_Project.py      # ℹ️ System architecture & exam specifications
│   └── 6_Analysis_History.py   # 📜 SQLite audit records log & inspector
│
├── src/                        # Modular Source Code
│   ├── __init__.py             # Package init & version metadata (v2.0.0)
│   ├── azure_language.py       # ☁️ Azure AI Language SDK Client wrapper
│   ├── database.py             # 🗄️ SQLite Database Manager & parameterized queries
│   ├── preprocessing.py        # NLTK text cleaning, normalization, lemmatization
│   ├── feature_engineering.py  # TF-IDF vectorization logic
│   ├── train.py                # Hyperparameter tuning (GridSearchCV) & 5-fold CV
│   ├── evaluate.py             # Model evaluation & report generator
│   └── predict.py              # Inference pipeline & word contribution engine
│
├── app.py                      # 🏠 Main Dashboard & SQLite live activity summary
├── main.py                     # ML pipeline training orchestrator
├── test_system.py              # 🧪 Automated 10-point test suite
├── news_analysis.db            # Auto-generated SQLite database (git-ignored)
├── .env.example                # Azure AI credential configuration template
├── .gitignore                  # Git ignore rules (.env, *.db, *.log, .venv/)
├── requirements.txt            # Project dependencies
└── README.md                   # Complete documentation
```

---

## ☁️ Microsoft Azure AI Language Setup Guide

This application integrates with **Azure AI Language** (part of Azure Cognitive Services). Follow these step-by-step instructions to create and configure your credentials.

### Step 1: Create an Azure Account
- If you do not have an account, sign up at [azure.microsoft.com/free](https://azure.microsoft.com/free/).
- Students can also register through [Azure for Students](https://azure.microsoft.com/en-us/free/students/) (provides \$100 credit without requiring a credit card).

### Step 2: Create a Language Resource in Azure Portal
1. Sign in to the [Azure Portal](https://portal.azure.com/).
2. In the top search bar, type **Language service** and select **Language services**.
3. Click **+ Create** / **Create language resource**.
4. Configure the basic settings:
   - **Subscription**: Select your active subscription.
   - **Resource Group**: Select an existing resource group or click *Create new* (e.g., `rg-news-analysis`).
   - **Region**: Choose a region close to you (e.g., `East US` or `Central India`).
   - **Name**: Enter a unique name (e.g., `lang-news-analysis-prod`).
   - **Pricing Tier**: Select **Free F0** (5,000 text records/month at zero cost) or **Standard S** if F0 is already used.
5. Review and click **Create**. Wait for deployment to complete (takes ~1-2 minutes).

### Step 3: Retrieve Endpoint URL and API Key
1. Once deployed, click **Go to resource**.
2. In the left navigation menu, under the **Resource Management** group, click **Keys and Endpoint**.
3. You will see:
   - **KEY 1** and **KEY 2** (e.g., `a1b2c3d4e5f6...`)
   - **Endpoint** (e.g., `https://lang-news-analysis-prod.cognitiveservices.azure.com/`)
4. Copy **KEY 1** and the **Endpoint URL**.

### Step 4: Configure Local Environment Variables
1. In your project root directory, locate `.env.example`.
2. Create a copy of `.env.example` named `.env`:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and paste your actual Azure values:
   ```env
   AZURE_LANGUAGE_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
   AZURE_LANGUAGE_KEY=your_actual_32_character_azure_key_here
   ```
4. **Security Note**: The `.env` file is already listed in `.gitignore`. Never commit your API key or endpoint to GitHub or share it in public channels.

### Step 5: Offline / Fallback Capability
If Azure credentials are not provided or network is offline:
- The system will **not crash**.
- The ML Fake/Real classification and SQLite logging will continue to function seamlessly.
- An alert card in the UI will notify the user: `Azure AI Language credentials not configured. ML classification is fully operational.`

---

## 🗄️ SQLite Database Design

The local SQLite database (`news_analysis.db`) is automatically initialized on the first launch of the application.

### Table Schema: `news_history`

| Column Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique analysis identifier |
| `article_text` | `TEXT` | `NOT NULL` | The full analyzed news article content |
| `ml_prediction` | `TEXT` | `NOT NULL` | ML classification result (`FAKE` or `REAL`) |
| `ml_confidence` | `REAL` | `NOT NULL` | Prediction probability (between `0.0` and `1.0`) |
| `sentiment` | `TEXT` | `NOT NULL` | Azure tone (`positive`, `neutral`, `negative`, etc.) |
| `sentiment_confidence` | `TEXT` | `NULL` | JSON string containing positive, neutral, negative scores |
| `key_phrases` | `TEXT` | `NULL` | JSON string array of extracted key phrases |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | UTC timestamp of the analysis event |

### Security & Integrity Features:
- **Parameterized Queries**: All SQL executions use `?` placeholders, preventing SQL Injection vulnerabilities.
- **JSON Serialization**: Complex nested objects (`sentiment_confidence` dict, `key_phrases` list) are safely serialized and deserialized via `json.dumps()` and `json.loads()`.
- **Automatic Initialization**: Table creation uses `CREATE TABLE IF NOT EXISTS`.

---

## 🚀 Installation & Running Guide

### 1. Clone the Repository
```bash
git clone https://github.com/HiteshChugh-2006/CodeAlpha_Fake-News-Detection-System.git
cd CodeAlpha_Fake-News-Detection-System
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Azure Credentials (Optional but Recommended)
```bash
cp .env.example .env
# Edit .env with your Azure Endpoint and Key
```

### 5. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```
Open your web browser and navigate to `http://localhost:8501`.

---

## 🧪 Automated Testing Suite

To execute the automated 10-point test suite covering ML prediction, text boundary conditions, Azure client handling, and SQLite database operations:

```bash
python test_system.py
```

### Tested Scenarios:
1. Normal news article classification with confidence scores.
2. Empty article handling & edge case normalization.
3. Short article classification resilience.
4. Long article multi-paragraph processing.
5. Missing Azure credentials graceful degradation.
6. Azure error containment without unhandled exceptions.
7. SQLite database auto-creation and schema verification.
8. Saving analysis records with parameterized SQL.
9. Retrieving records, ID lookup, statistics aggregation, and deletion.
10. Multi-page syntax and import compatibility.

---

## 📊 Machine Learning Model Benchmarks

Trained on the **ISOT Fake News Dataset** (44,898 articles from Reuters and flagged sources):

| Model Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **XGBoost Classifier (Best)** | **99.81%** | **99.80%** | **99.81%** | **99.81%** | **0.9998** |
| Linear SVC (Calibrated) | 99.53% | 99.52% | 99.53% | 99.53% | 0.9996 |
| Logistic Regression | 98.74% | 98.73% | 98.74% | 98.74% | 0.9984 |
| Multinomial Naive Bayes | 95.22% | 95.28% | 95.22% | 95.21% | 0.9891 |

---

## ⚠️ Limitations & Future Scope

### Limitations:
- **Corpus Domain**: The ML classifier is trained primarily on US political and general world news (2015–2018). Novel terminology from very recent events may rely heavily on Azure Key Phrases rather than historical TF-IDF weights.
- **Language**: Current TF-IDF vectorizer and NLTK lemmatizers are optimized for English text.
- **Azure Quota**: The Azure Free F0 tier allows 5,000 text records/month with a rate limit of 10 calls/second.

### Future Scope:
- **Transformer Fine-Tuning**: Integration of DistilBERT or RoBERTa for contextual embeddings.
- **Multilingual Support**: Expanding Azure AI Language multi-language capabilities for global news.
- **Live News Feed Scraping**: Automated RSS feed ingestion with continuous background analysis.
- **Fact-Checking Knowledge Graph**: Direct cross-referencing with claim-review APIs (Google Fact Check Tools).

---

## 👤 Author & Academic Context

- **Student Name**: Hitesh Chugh
- **Curriculum Alignment**: Microsoft Certified: Azure AI Fundamentals (AI-901)
- **Project Purpose**: Industrial Internship Examination Project
- **GitHub**: [@HiteshChugh-2006](https://github.com/HiteshChugh-2006)
- **LinkedIn**: [Hitesh Chugh](https://www.linkedin.com/in/hitesh-chugh-a80170320/)

---

## 📜 License & Acknowledgments

This project is open-source under the MIT License. Special thanks to the **University Industrial Internship Mentors** and the **Microsoft Learn** curriculum for guidance on Azure Cognitive Services and Machine Learning deployment.
