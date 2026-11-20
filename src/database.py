"""
SQLite Database Module
=======================

Provides :class:`AnalysisDatabase` for storing and retrieving news
analysis history in a local SQLite database.

The database and table are created automatically on first use.
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Default database path: project root / news_analysis.db
_DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "news_analysis.db",
)


class AnalysisDatabase:
    """SQLite-backed storage for news analysis history.

    Parameters
    ----------
    db_path : str or None
        Path to the SQLite database file.  Defaults to
        ``news_analysis.db`` in the project root directory.
        The file and table are created automatically if they
        do not exist.
    """

    TABLE_NAME = "news_history"

    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id                   INTEGER PRIMARY KEY AUTOINCREMENT,
        article_text         TEXT    NOT NULL,
        ml_prediction        TEXT,
        ml_confidence        REAL,
        sentiment            TEXT,
        sentiment_confidence TEXT,
        key_phrases          TEXT,
        created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path or _DEFAULT_DB_PATH
        self._initialize_database()

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def _initialize_database(self) -> None:
        """Create the database file and table if they do not exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(self.CREATE_TABLE_SQL)
                conn.commit()
            logger.info("Database initialized at %s", self.db_path)
        except Exception:
            logger.exception("Failed to initialize database at %s", self.db_path)

    def _get_connection(self) -> sqlite3.Connection:
        """Return a new SQLite connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ------------------------------------------------------------------
    # Insert
    # ------------------------------------------------------------------

    def save_analysis(
        self,
        article_text: str,
        ml_prediction: Optional[str] = None,
        ml_confidence: Optional[float] = None,
        sentiment: Optional[str] = None,
        sentiment_confidence: Optional[Dict[str, float]] = None,
        key_phrases: Optional[List[str]] = None,
    ) -> Optional[int]:
        """Save a complete analysis record.

        Parameters
        ----------
        article_text : str
            The original article text.
        ml_prediction : str or None
            ML model prediction ('FAKE' or 'REAL').
        ml_confidence : float or None
            ML model confidence score (0.0 – 1.0).
        sentiment : str or None
            Azure sentiment result.
        sentiment_confidence : dict or None
            Azure sentiment confidence scores.
        key_phrases : list of str or None
            Extracted key phrases.

        Returns
        -------
        int or None
            The row ID of the inserted record, or None on failure.
        """
        sql = f"""
        INSERT INTO {self.TABLE_NAME}
            (article_text, ml_prediction, ml_confidence,
             sentiment, sentiment_confidence, key_phrases, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            # Serialize complex types to JSON strings
            sent_conf_str = (
                json.dumps(sentiment_confidence) if sentiment_confidence else None
            )
            kp_str = json.dumps(key_phrases) if key_phrases else None
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with self._get_connection() as conn:
                cursor = conn.execute(
                    sql,
                    (
                        article_text,
                        ml_prediction,
                        ml_confidence,
                        sentiment,
                        sent_conf_str,
                        kp_str,
                        now,
                    ),
                )
                conn.commit()
                row_id = cursor.lastrowid
                logger.info("Analysis saved with ID %d.", row_id)
                return row_id
        except Exception:
            logger.exception("Failed to save analysis.")
            return None

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_all_records(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve all analysis records, most recent first.

        Parameters
        ----------
        limit : int, default 100
            Maximum number of records to return.

        Returns
        -------
        list of dict
        """
        sql = f"""
        SELECT * FROM {self.TABLE_NAME}
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """
        try:
            with self._get_connection() as conn:
                rows = conn.execute(sql, (limit,)).fetchall()
                return [self._row_to_dict(row) for row in rows]
        except Exception:
            logger.exception("Failed to retrieve records.")
            return []

    def get_record_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a single analysis record by its ID.

        Parameters
        ----------
        record_id : int
            The row ID.

        Returns
        -------
        dict or None
        """
        sql = f"SELECT * FROM {self.TABLE_NAME} WHERE id = ?"
        try:
            with self._get_connection() as conn:
                row = conn.execute(sql, (record_id,)).fetchone()
                return self._row_to_dict(row) if row else None
        except Exception:
            logger.exception("Failed to retrieve record %d.", record_id)
            return None

    def get_statistics(self) -> Dict[str, Any]:
        """Return aggregate statistics about the analysis history.

        Returns
        -------
        dict
            total_analyses, fake_count, real_count,
            sentiment_distribution, latest_analysis.
        """
        try:
            with self._get_connection() as conn:
                total = conn.execute(
                    f"SELECT COUNT(*) FROM {self.TABLE_NAME}"
                ).fetchone()[0]

                fake = conn.execute(
                    f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE ml_prediction = ?",
                    ("FAKE",),
                ).fetchone()[0]

                real = conn.execute(
                    f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE ml_prediction = ?",
                    ("REAL",),
                ).fetchone()[0]

                # Sentiment distribution
                sentiment_rows = conn.execute(
                    f"SELECT sentiment, COUNT(*) as cnt FROM {self.TABLE_NAME} "
                    f"WHERE sentiment IS NOT NULL GROUP BY sentiment"
                ).fetchall()
                sentiment_dist = {row[0]: row[1] for row in sentiment_rows}

                # Latest analysis timestamp
                latest = conn.execute(
                    f"SELECT MAX(created_at) FROM {self.TABLE_NAME}"
                ).fetchone()[0]

                return {
                    "total": total,
                    "fake": fake,
                    "real": real,
                    "total_analyses": total,
                    "fake_count": fake,
                    "real_count": real,
                    "sentiment_distribution": sentiment_dist,
                    "latest_analysis": latest,
                }
        except Exception:
            logger.exception("Failed to compute statistics.")
            return {
                "total": 0,
                "fake": 0,
                "real": 0,
                "total_analyses": 0,
                "fake_count": 0,
                "real_count": 0,
                "sentiment_distribution": {},
                "latest_analysis": None,
            }

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def clear_history(self) -> bool:
        """Delete all records from the history table.

        Returns
        -------
        bool
            True if successful.
        """
        try:
            with self._get_connection() as conn:
                conn.execute(f"DELETE FROM {self.TABLE_NAME}")
                conn.commit()
            logger.info("Analysis history cleared.")
            return True
        except Exception:
            logger.exception("Failed to clear history.")
            return False

    def delete_record(self, record_id: int) -> bool:
        """Delete a single record by ID.

        Parameters
        ----------
        record_id : int
            The row ID to delete.

        Returns
        -------
        bool
            True if the record was deleted.
        """
        try:
            with self._get_connection() as conn:
                conn.execute(
                    f"DELETE FROM {self.TABLE_NAME} WHERE id = ?", (record_id,)
                )
                conn.commit()
            logger.info("Record %d deleted.", record_id)
            return True
        except Exception:
            logger.exception("Failed to delete record %d.", record_id)
            return False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        """Convert a sqlite3.Row to a plain dict, deserializing JSON fields."""
        d = dict(row)
        # Deserialize JSON-encoded fields
        if d.get("sentiment_confidence"):
            try:
                d["sentiment_confidence"] = json.loads(d["sentiment_confidence"])
            except (json.JSONDecodeError, TypeError):
                pass
        if d.get("key_phrases"):
            try:
                d["key_phrases"] = json.loads(d["key_phrases"])
            except (json.JSONDecodeError, TypeError):
                pass
        return d
