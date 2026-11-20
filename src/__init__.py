"""
AI-Based News Article Analysis System
=======================================

An upgraded ML pipeline for detecting fake news articles using NLP,
classical machine learning models (Logistic Regression, Naive Bayes,
Linear SVC, XGBoost), Microsoft Azure AI Language for sentiment
analysis and key phrase extraction, and SQLite for analysis history.

Modules:
    - preprocessing: Text cleaning and normalization
    - feature_engineering: TF-IDF vectorization and vocabulary analysis
    - train: Model training with cross-validation and hyperparameter tuning
    - evaluate: Model evaluation, comparison, and report generation
    - predict: Inference on new articles
    - azure_language: Azure AI Language sentiment & key phrase extraction
    - database: SQLite analysis history storage
"""

from src.preprocessing import TextPreprocessor
from src.feature_engineering import FeatureEngineer
from src.train import ModelTrainer
from src.evaluate import ModelEvaluator
from src.predict import NewsPredictor
from src.azure_language import AzureLanguageAnalyzer
from src.database import AnalysisDatabase

__all__ = [
    "TextPreprocessor",
    "FeatureEngineer",
    "ModelTrainer",
    "ModelEvaluator",
    "NewsPredictor",
    "AzureLanguageAnalyzer",
    "AnalysisDatabase",
]

__version__ = "2.0.0"
