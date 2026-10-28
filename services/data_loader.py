"""
Data loader and validation service.
Handles CSV ingestion, file size limits, error handling, and column profiling.
"""
import io
from typing import Tuple, Dict, Any, Optional
import pandas as pd
from core.config import settings
from core.database import DatabaseManager

class DataLoaderService:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()
        self.max_bytes = settings.max_upload_size_mb * 1024 * 1024

    def validate_and_load_csv(self, file_bytes: bytes, filename: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Validates the file, parses CSV data safely, and extracts profile metadata.
        """
        # 1. File size check
        if len(file_bytes) > self.max_bytes:
            raise ValueError(
                f"File size ({len(file_bytes) / (1024*1024):.2f} MB) exceeds maximum allowed limit of {settings.max_upload_size_mb} MB."
            )
        
        # 2. Empty file check
        if len(file_bytes.strip()) == 0:
            raise ValueError("The uploaded file is completely empty. Please upload a valid CSV dataset.")

        # 3. Parse CSV safely
        try:
            # Handle utf-8 and fallback to latin-1 if needed
            try:
                buffer = io.StringIO(file_bytes.decode('utf-8'))
                df = pd.read_csv(buffer, on_bad_lines='error')
            except UnicodeDecodeError:
                buffer = io.StringIO(file_bytes.decode('latin-1'))
                df = pd.read_csv(buffer, on_bad_lines='error')
        except pd.errors.EmptyDataError:
            raise ValueError("The uploaded CSV has no columns or data records.")
        except Exception as e:
            raise ValueError(f"Malformed CSV file: {str(e)}")

        # 4. Check for rows and columns
        if df.empty or len(df.columns) == 0:
            raise ValueError("The parsed dataset contains 0 rows or 0 columns.")

        # 5. Extract profile metadata
        profile = self.profile_dataframe(df, filename)

        return df, profile

    def profile_dataframe(self, df: pd.DataFrame, filename: str) -> Dict[str, Any]:
        """Calculates column types, missing values, and memory metrics."""
        total_rows = len(df)
        total_cols = len(df.columns)
        
        col_summary = []
        for col in df.columns:
            null_count = int(df[col].isnull().sum())
            null_pct = round((null_count / total_rows) * 100, 2) if total_rows > 0 else 0
            unique_count = int(df[col].nunique(dropna=True))
            col_summary.append({
                "column_name": str(col),
                "dtype": str(df[col].dtype),
                "null_count": null_count,
                "null_percentage": null_pct,
                "unique_count": unique_count
            })

        return {
            "filename": filename,
            "row_count": total_rows,
            "column_count": total_cols,
            "columns": list(df.columns),
            "columns_summary": col_summary,
            "total_missing_cells": int(df.isnull().sum().sum())
        }

    def ingest_csv(self, file_bytes: bytes, filename: str) -> Tuple[str, Dict[str, Any]]:
        """
        Full ingestion pipeline: validates, profiles, stores in SQLite, and returns table name and metadata.
        """
        df, profile = self.validate_and_load_csv(file_bytes, filename)
        table_name = self.db.store_dataset(df, filename)
        profile["table_name"] = table_name
        return table_name, profile
