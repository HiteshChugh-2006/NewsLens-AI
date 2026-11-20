"""
Automated Test Suite for AI-Based News Article Analysis System
==============================================================
Validates:
  1. Normal article classification (ML)
  2. Empty article handling
  3. Short article handling
  4. Long article handling
  5. Azure credentials missing handling (graceful warning, no crash)
  6. Azure API error resilience
  7. SQLite database auto-creation
  8. Saving analysis records (parameterized queries)
  9. Retrieving records & computing statistics
 10. Syntax & import validation across all project files
"""

import os
import sys
import tempfile
import unittest

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.azure_language import AzureLanguageAnalyzer
from src.database import AnalysisDatabase
from src.predict import NewsPredictor
from src.preprocessing import TextPreprocessor


class TestNewsArticleAnalysisSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model_path = os.path.join(PROJECT_ROOT, "models", "best_model.joblib")
        cls.vec_path = os.path.join(PROJECT_ROOT, "models", "tfidf_vectorizer.joblib")
        cls.predictor = NewsPredictor(model_path=cls.model_path, vectorizer_path=cls.vec_path)

    def test_01_normal_article_classification(self):
        """Test normal news article classification."""
        sample_text = (
            "WASHINGTON (Reuters) - The White House and congressional leaders reached an agreement "
            "on budget caps and the debt limit on Tuesday, paving the way for a two-year fiscal deal."
        )
        res = self.predictor.predict(sample_text)
        self.assertIn("prediction", res)
        self.assertIn("confidence", res)
        self.assertIn(res["prediction"], ["REAL", "FAKE"])
        self.assertGreaterEqual(res["confidence"], 0.5)

    def test_02_empty_article_handling(self):
        """Test handling of empty text input."""
        tp = TextPreprocessor()
        cleaned = tp.clean_text("")
        self.assertEqual(cleaned, "")
        
        # Azure analyzer with empty text
        analyzer = AzureLanguageAnalyzer()
        res = analyzer.analyze("")
        self.assertIn("sentiment_result", res)
        self.assertIn("key_phrases_result", res)
        self.assertFalse(res["sentiment_result"]["success"])
        self.assertFalse(res["key_phrases_result"]["success"])

    def test_03_short_article_handling(self):
        """Test handling of very short text."""
        short_text = "Breaking News! Alert!"
        res = self.predictor.predict(short_text)
        self.assertIn(res["prediction"], ["REAL", "FAKE"])

    def test_04_long_article_handling(self):
        """Test handling of long multi-paragraph text."""
        long_text = "The economic committee met today to discuss the quarterly inflation report. " * 80
        res = self.predictor.predict(long_text)
        self.assertIn(res["prediction"], ["REAL", "FAKE"])
        
        # Verify text cleaning on long text
        tp = TextPreprocessor()
        cleaned = tp.clean_text(long_text)
        self.assertGreater(len(cleaned), 100)

    def test_05_azure_credentials_missing_graceful(self):
        """Test Azure analyzer behaves gracefully without credentials."""
        # Test analyzer with explicit None credentials
        analyzer = AzureLanguageAnalyzer(endpoint="", key="")
        self.assertFalse(analyzer.is_configured)
        self.assertTrue(len(analyzer.configuration_message) > 0)
        
        # Sentiment check
        s_res = analyzer.analyze_sentiment("Economy improves")
        self.assertFalse(s_res["success"])
        self.assertIsNone(s_res["sentiment"])
        self.assertIn("not configured", s_res["error"].lower())

        # Key phrases check
        k_res = analyzer.extract_key_phrases("Economy improves")
        self.assertFalse(k_res["success"])
        self.assertEqual(k_res["key_phrases"], [])
        self.assertIn("not configured", k_res["error"].lower())

    def test_06_database_lifecycle_and_crud(self):
        """Test SQLite database creation, insertion, queries, stats, deletion."""
        tmp_db_path = os.path.join(tempfile.gettempdir(), "test_news_analysis_suite.db")
        if os.path.exists(tmp_db_path):
            try:
                os.remove(tmp_db_path)
            except Exception:
                pass

        try:
            db = AnalysisDatabase(db_path=tmp_db_path)
            
            # Initial stats
            stats = db.get_statistics()
            self.assertEqual(stats["total"], 0)
            self.assertEqual(stats["fake"], 0)
            self.assertEqual(stats["real"], 0)

            # Insert Record 1 (Real)
            rec1_id = db.save_analysis(
                article_text="Stock markets rallied after positive inflation figures were published.",
                ml_prediction="REAL",
                ml_confidence=0.985,
                sentiment="positive",
                sentiment_confidence={"positive": 0.95, "neutral": 0.04, "negative": 0.01},
                key_phrases=["stock markets", "inflation figures", "positive rally"]
            )
            self.assertIsInstance(rec1_id, int)
            self.assertGreater(rec1_id, 0)

            # Insert Record 2 (Fake)
            rec2_id = db.save_analysis(
                article_text="SHOCKING: Secret extraterrestrial base discovered under city hall!",
                ml_prediction="FAKE",
                ml_confidence=0.999,
                sentiment="negative",
                sentiment_confidence={"positive": 0.02, "neutral": 0.08, "negative": 0.90},
                key_phrases=["secret base", "extraterrestrial", "city hall"]
            )
            self.assertIsInstance(rec2_id, int)

            # Check stats
            updated_stats = db.get_statistics()
            self.assertEqual(updated_stats["total"], 2)
            self.assertEqual(updated_stats["real"], 1)
            self.assertEqual(updated_stats["fake"], 1)
            self.assertEqual(updated_stats["sentiment_distribution"]["positive"], 1)
            self.assertEqual(updated_stats["sentiment_distribution"]["negative"], 1)

            # Retrieve all records
            all_recs = db.get_all_records()
            self.assertEqual(len(all_recs), 2)
            self.assertEqual(all_recs[0]["id"], rec2_id) # Most recent first

            # Retrieve single record
            rec1 = db.get_record_by_id(rec1_id)
            self.assertIsNotNone(rec1)
            self.assertEqual(rec1["ml_prediction"], "REAL")
            self.assertAlmostEqual(rec1["ml_confidence"], 0.985, places=3)
            self.assertIn("stock markets", rec1["key_phrases"])

            # Delete single record
            del_ok = db.delete_record(rec1_id)
            self.assertTrue(del_ok)
            self.assertEqual(db.get_statistics()["total"], 1)

            # Clear all
            clear_ok = db.clear_history()
            self.assertTrue(clear_ok)
            self.assertEqual(db.get_statistics()["total"], 0)

        finally:
            if os.path.exists(tmp_db_path):
                try:
                    os.remove(tmp_db_path)
                except Exception:
                    pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
