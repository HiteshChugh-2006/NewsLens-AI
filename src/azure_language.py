"""
Azure AI Language Integration Module
======================================

Provides :class:`AzureLanguageAnalyzer` for sentiment analysis and
key phrase extraction using Microsoft Azure AI Language service.

Requires environment variables:
    AZURE_LANGUAGE_ENDPOINT  – The Azure AI Language resource endpoint URL
    AZURE_LANGUAGE_KEY       – The API key for the resource
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def _load_env_file() -> None:
    """Attempt to load .env file using python-dotenv if available."""
    try:
        from dotenv import load_dotenv
        env_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
        )
        if os.path.exists(env_path):
            load_dotenv(env_path)
            logger.info("Loaded environment variables from .env file.")
    except ImportError:
        pass  # python-dotenv not installed; rely on system env vars


# Try to load .env on module import
_load_env_file()


class AzureLanguageAnalyzer:
    """Wrapper for Azure AI Language — sentiment analysis and key phrase extraction.

    Parameters
    ----------
    endpoint : str or None
        Azure AI Language endpoint URL. If *None*, reads from
        ``AZURE_LANGUAGE_ENDPOINT`` environment variable.
    key : str or None
        Azure AI Language API key. If *None*, reads from
        ``AZURE_LANGUAGE_KEY`` environment variable.

    Attributes
    ----------
    is_configured : bool
        Whether valid credentials are available.
    configuration_message : str
        Human-readable status message about the configuration.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        key: Optional[str] = None,
    ) -> None:
        self._endpoint = endpoint or os.environ.get("AZURE_LANGUAGE_ENDPOINT", "").strip()
        self._key = key or os.environ.get("AZURE_LANGUAGE_KEY", "").strip()
        self._client = None
        self.is_configured: bool = False
        self.configuration_message: str = ""

        self._initialize_client()

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def _initialize_client(self) -> None:
        """Try to create the Azure Text Analytics client."""
        if not self._endpoint or not self._key:
            self.configuration_message = (
                "Azure AI Language credentials are not configured.\n\n"
                "Please set the following environment variables:\n"
                "  AZURE_LANGUAGE_ENDPOINT=https://<your-resource>.cognitiveservices.azure.com/\n"
                "  AZURE_LANGUAGE_KEY=<your-api-key>\n\n"
                "You can create a free Azure AI Language resource at:\n"
                "  https://portal.azure.com → Create a resource → AI + Machine Learning → Language"
            )
            logger.warning("Azure AI Language credentials not found.")
            return

        try:
            from azure.ai.textanalytics import TextAnalyticsClient
            from azure.core.credentials import AzureKeyCredential

            self._client = TextAnalyticsClient(
                endpoint=self._endpoint,
                credential=AzureKeyCredential(self._key),
            )
            self.is_configured = True
            self.configuration_message = "Azure AI Language is configured and ready."
            logger.info("Azure AI Language client initialized successfully.")
        except ImportError:
            self.configuration_message = (
                "The azure-ai-textanalytics package is not installed.\n"
                "Install it with: pip install azure-ai-textanalytics"
            )
            logger.error("azure-ai-textanalytics package not installed.")
        except Exception as e:
            self.configuration_message = (
                f"Failed to initialize Azure AI Language client: {str(e)}"
            )
            logger.exception("Azure AI Language client initialization failed.")

    # ------------------------------------------------------------------
    # Sentiment Analysis
    # ------------------------------------------------------------------

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze the emotional tone of the given text.

        Parameters
        ----------
        text : str
            The text to analyze.

        Returns
        -------
        dict
            ``sentiment``         – overall sentiment (positive/negative/neutral/mixed)
            ``confidence_scores`` – {positive, negative, neutral} floats
            ``success``           – whether the API call succeeded
            ``error``             – error message if the call failed, else None
        """
        if not self.is_configured or self._client is None:
            return {
                "sentiment": None,
                "confidence_scores": None,
                "success": False,
                "error": self.configuration_message,
            }

        if not text or not text.strip():
            return {
                "sentiment": None,
                "confidence_scores": None,
                "success": False,
                "error": "Empty text provided.",
            }

        try:
            # Azure API accepts a list of documents
            response = self._client.analyze_sentiment(documents=[text])[0]

            if response.is_error:
                return {
                    "sentiment": None,
                    "confidence_scores": None,
                    "success": False,
                    "error": f"Azure API error: {response.error.message}",
                }

            result = {
                "sentiment": response.sentiment,
                "confidence_scores": {
                    "positive": response.confidence_scores.positive,
                    "negative": response.confidence_scores.negative,
                    "neutral": response.confidence_scores.neutral,
                },
                "success": True,
                "error": None,
            }
            logger.info("Sentiment analysis complete: %s", result["sentiment"])
            return result

        except Exception as e:
            logger.exception("Sentiment analysis failed.")
            return {
                "sentiment": None,
                "confidence_scores": None,
                "success": False,
                "error": f"Sentiment analysis error: {str(e)}",
            }

    # ------------------------------------------------------------------
    # Key Phrase Extraction
    # ------------------------------------------------------------------

    def extract_key_phrases(self, text: str) -> Dict[str, Any]:
        """Extract important phrases from the given text.

        Parameters
        ----------
        text : str
            The text to analyze.

        Returns
        -------
        dict
            ``key_phrases`` – list of extracted key phrases (strings)
            ``success``     – whether the API call succeeded
            ``error``       – error message if the call failed, else None
        """
        if not self.is_configured or self._client is None:
            return {
                "key_phrases": [],
                "success": False,
                "error": self.configuration_message,
            }

        if not text or not text.strip():
            return {
                "key_phrases": [],
                "success": False,
                "error": "Empty text provided.",
            }

        try:
            # Azure has a 5,120 character limit per document
            truncated_text = text[:5120] if len(text) > 5120 else text

            response = self._client.extract_key_phrases(documents=[truncated_text])[0]

            if response.is_error:
                return {
                    "key_phrases": [],
                    "success": False,
                    "error": f"Azure API error: {response.error.message}",
                }

            result = {
                "key_phrases": list(response.key_phrases),
                "success": True,
                "error": None,
            }
            logger.info(
                "Key phrase extraction complete: %d phrases found.",
                len(result["key_phrases"]),
            )
            return result

        except Exception as e:
            logger.exception("Key phrase extraction failed.")
            return {
                "key_phrases": [],
                "success": False,
                "error": f"Key phrase extraction error: {str(e)}",
            }

    # ------------------------------------------------------------------
    # Combined Analysis
    # ------------------------------------------------------------------

    def analyze(self, text: str) -> Dict[str, Any]:
        """Run both sentiment analysis and key phrase extraction.

        Parameters
        ----------
        text : str
            The text to analyze.

        Returns
        -------
        dict
            Combined results with keys ``sentiment_result`` and
            ``key_phrases_result``.
        """
        return {
            "sentiment_result": self.analyze_sentiment(text),
            "key_phrases_result": self.extract_key_phrases(text),
        }
