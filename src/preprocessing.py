"""
Text Preprocessing Module
==========================

Provides the :class:`TextPreprocessor` class which cleans and normalises raw
news-article text so it is ready for downstream feature engineering.

Pipeline applied by :meth:`clean_text`:
    1. Lowercase
    2. URL removal
    3. HTML tag removal
    4. Punctuation removal
    5. Digit removal
    6. Tokenization  (``nltk.word_tokenize``)
    7. Stopword removal (NLTK English stopwords)
    8. Lemmatization  (``WordNetLemmatizer``)
"""

from __future__ import annotations

import logging
import re
import string
from typing import List, Optional

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Ensure required NLTK data packages are available
# ---------------------------------------------------------------------------
_NLTK_PACKAGES = ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]


def _download_nltk_data() -> None:
    """Download NLTK resources if they are not already present."""
    for pkg in _NLTK_PACKAGES:
        try:
            nltk.data.find(f"tokenizers/{pkg}" if "punkt" in pkg else pkg)
        except LookupError:
            logger.info("Downloading NLTK resource: %s", pkg)
            nltk.download(pkg, quiet=True)


_download_nltk_data()


# ---------------------------------------------------------------------------
# Pre-compiled regex patterns (compiled once for performance)
# ---------------------------------------------------------------------------
_RE_URL = re.compile(r"https?://\S+|www\.\S+")
_RE_HTML = re.compile(r"<[^>]+>")
_RE_PUNCT = re.compile(f"[{re.escape(string.punctuation)}]")
_RE_DIGITS = re.compile(r"\d+")
_RE_WHITESPACE = re.compile(r"\s+")

# Agency datelines: e.g. "WASHINGTON (Reuters) - ", "SEATTLE/WASHINGTON (Reuters) - ", "(Reuters) - "
_RE_DATELINE = re.compile(
    r"(?:\b[a-zA-Z]{2,20}(?:/[a-zA-Z]{2,20})?\s+)?\((?:Reuters|AP|AFP)\)\s*[-–—:]\s*",
    re.IGNORECASE,
)

# Standalone wire agency references and artifacts
_RE_AGENCY_TOKENS = re.compile(
    r"\b(?:reuters|associated\s+press|bloomberg\s+news|afp\s+news)\b",
    re.IGNORECASE,
)

# Footers, photo credits, and social media watermarks in web scrapings
_RE_WATERMARKS = re.compile(
    r"(?:featured\s+image\s+(?:via)?\s*.*$|image\s+via\s+.*$|photo\s+(?:by|credit)\s*:\s*.*$|"
    r"pic\.twitter\.com/\S+|twitter\.com/\S+|facebook\.com/\S+|instagram\.com/\S+|"
    r"21st\s+century\s+wire|daily\s+caller|breitbart\s+news|infowars)",
    re.IGNORECASE | re.MULTILINE,
)

# Domain stopwords for fake/real news debiasing
DOMAIN_STOPWORDS = {
    "reuters", "reuter", "image", "images", "featured", "via", "photo",
    "pic", "twitter", "tweet", "getty", "century", "wire", "daily",
    "caller", "breitbart", "video", "watch", "post", "facebook", "url",
}


class TextPreprocessor:
    """Reusable text preprocessor with a scikit-learn-style fit/transform API.

    Parameters
    ----------
    remove_stopwords : bool, default True
        Whether to strip English stopwords.
    lemmatize : bool, default True
        Whether to apply WordNet lemmatization.
    min_token_length : int, default 2
        Discard tokens shorter than this after cleaning.

    Examples
    --------
    >>> tp = TextPreprocessor()
    >>> tp.fit()                       # optional – loads resources
    >>> tp.clean_text("Check http://x.com <b>BREAKING</b> news!!1")
    'check breaking news'
    """

    def __init__(
        self,
        remove_stopwords: bool = True,
        lemmatize: bool = True,
        min_token_length: int = 2,
    ) -> None:
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        self.min_token_length = min_token_length

        self._stop_words: Optional[set] = None
        self._lemmatizer: Optional[WordNetLemmatizer] = None
        self._is_fitted: bool = False

    # ------------------------------------------------------------------
    # Fit / Transform API
    # ------------------------------------------------------------------

    def fit(self, X=None, y=None) -> "TextPreprocessor":
        """Initialise internal NLTK resources.

        Parameters are accepted (but ignored) so the object is compatible with
        scikit-learn ``Pipeline``.
        """
        if self.remove_stopwords:
            self._stop_words = set(stopwords.words("english")) | DOMAIN_STOPWORDS
            logger.debug("Loaded %d English + domain stopwords.", len(self._stop_words))
        if self.lemmatize:
            self._lemmatizer = WordNetLemmatizer()
        self._is_fitted = True
        logger.info("TextPreprocessor fitted.")
        return self

    def transform(self, texts: pd.Series) -> pd.Series:
        """Apply :meth:`clean_text` to every element of *texts*.

        Parameters
        ----------
        texts : pd.Series
            Raw text strings.

        Returns
        -------
        pd.Series
            Cleaned text strings.
        """
        if not self._is_fitted:
            self.fit()
        total = len(texts)
        logger.info("Preprocessing %d documents …", total)

        cleaned: List[str] = []
        log_every = max(1, total // 10)
        for idx, text in enumerate(texts):
            cleaned.append(self.clean_text(text))
            if (idx + 1) % log_every == 0:
                logger.info(
                    "  Progress: %d / %d (%.0f%%)",
                    idx + 1,
                    total,
                    (idx + 1) / total * 100,
                )
        logger.info("Preprocessing complete.")
        return pd.Series(cleaned, index=texts.index)

    def fit_transform(self, texts: pd.Series, y=None) -> pd.Series:
        """Convenience wrapper: ``fit`` then ``transform``."""
        return self.fit().transform(texts)

    # ------------------------------------------------------------------
    # Core cleaning logic
    # ------------------------------------------------------------------

    def clean_text(self, text: str) -> str:
        """Clean a single text string.

        Steps applied (in order):
            1. Agency dateline removal (strips "CITY (Reuters) - " / wire prefixes)
            2. Social media, photo credit & publisher watermark removal
            3. Standalone wire agency reference removal
            4. URL removal
            5. HTML tag removal
            6. Lowercase
            7. Punctuation removal
            8. Digit removal
            9. Whitespace collapse & Tokenization
            10. Stopword removal (English + domain debiasing stops)
            11. Lemmatization (WordNet)
            12. Short-token removal
            13. Re-join tokens

        Parameters
        ----------
        text : str
            Raw input text.

        Returns
        -------
        str
            Cleaned, space-joined tokens.
        """
        if not isinstance(text, str) or not text.strip():
            return ""

        # Lazy-fit if the user skipped calling fit()
        if not self._is_fitted:
            self.fit()

        # 1. Remove agency datelines (e.g. "WASHINGTON (Reuters) - ")
        text = _RE_DATELINE.sub(" ", text)

        # 2. Remove footer/image/social media watermarks
        text = _RE_WATERMARKS.sub(" ", text)

        # 3. Remove standalone wire agency tokens
        text = _RE_AGENCY_TOKENS.sub(" ", text)

        # 4. Remove URLs
        text = _RE_URL.sub(" ", text)

        # 5. Remove HTML tags
        text = _RE_HTML.sub(" ", text)

        # 6. Lowercase
        text = text.lower()

        # 7. Remove punctuation
        text = _RE_PUNCT.sub(" ", text)

        # 8. Remove digits
        text = _RE_DIGITS.sub(" ", text)

        # 9. Collapse whitespace then tokenize
        text = _RE_WHITESPACE.sub(" ", text).strip()
        tokens: List[str] = word_tokenize(text)

        # 10. Stopword removal
        if self.remove_stopwords and self._stop_words:
            tokens = [t for t in tokens if t not in self._stop_words]

        # 11. Lemmatization
        if self.lemmatize and self._lemmatizer:
            tokens = [self._lemmatizer.lemmatize(t) for t in tokens]

        # 12. Drop short tokens
        tokens = [t for t in tokens if len(t) >= self.min_token_length]

        return " ".join(tokens)

    # ------------------------------------------------------------------
    # DataFrame helper
    # ------------------------------------------------------------------

    def preprocess_dataframe(
        self,
        df: pd.DataFrame,
        text_column: str = "text",
        output_column: Optional[str] = None,
    ) -> pd.DataFrame:
        """Apply preprocessing to a DataFrame column *in-place*.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame.
        text_column : str
            Name of the column containing raw text.
        output_column : str or None
            Name for the cleaned-text column.  Defaults to
            ``{text_column}_clean``.

        Returns
        -------
        pd.DataFrame
            The same DataFrame with the new cleaned column added.

        Raises
        ------
        ValueError
            If *text_column* is not found in *df*.
        """
        if text_column not in df.columns:
            raise ValueError(
                f"Column '{text_column}' not found in DataFrame. "
                f"Available columns: {list(df.columns)}"
            )

        out_col = output_column or f"{text_column}_clean"
        logger.info(
            "Preprocessing column '%s' → '%s' (%d rows)",
            text_column,
            out_col,
            len(df),
        )

        df[out_col] = self.transform(df[text_column].fillna(""))
        return df
