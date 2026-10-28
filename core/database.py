"""
Database engine and table management using SQLAlchemy.
Provides safe table operations, cataloging, and isolated dataset tables.
"""
import re
import hashlib
from typing import Optional, List, Dict, Any
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from core.config import settings

def get_engine(db_path: Optional[str] = None):
    path = db_path or settings.sqlite_db_path
    return create_engine(f"sqlite:///{path}", echo=False)

def sanitize_table_name(filename: str) -> str:
    """
    Generate a safe, predictable, injection-resistant internal table name.
    Only allows lowercase alphanumeric characters and underscores, prefixed with dataset_.
    """
    # Remove file extension
    base = re.sub(r'\.[^.]+$', '', filename).lower()
    # Replace non-alphanumeric with underscores
    clean = re.sub(r'[^a-z0-9_]', '_', base)
    clean = re.sub(r'_+', '_', clean).strip('_')
    if not clean:
        clean = "uploaded"
    # Add a short deterministic hash based on filename to prevent collisions
    hash_suffix = hashlib.md5(filename.encode('utf-8')).hexdigest()[:6]
    return f"dataset_{clean}_{hash_suffix}"

def sanitize_column_name(col: str) -> str:
    """
    Sanitize column names to prevent SQL identifier issues.
    """
    clean = str(col).strip()
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', clean)
    clean = re.sub(r'_+', '_', clean).strip('_')
    if not clean or clean[0].isdigit():
        clean = f"col_{clean}"
    return clean.lower()

class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        self.engine = get_engine(db_path)
        self._init_catalog()

    def _init_catalog(self):
        """Create catalog table to keep metadata separate from dataset tables."""
        with self.engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS _dataset_catalog (
                    table_name TEXT PRIMARY KEY,
                    original_filename TEXT NOT NULL,
                    row_count INTEGER NOT NULL,
                    column_count INTEGER NOT NULL,
                    columns_json TEXT NOT NULL,
                    dtypes_json TEXT NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))

    def store_dataset(self, df: pd.DataFrame, original_filename: str) -> str:
        """
        Stores the dataframe in a sanitized SQLite table and records metadata.
        Supports re-uploading datasets safely by replacing existing table.
        """
        table_name = sanitize_table_name(original_filename)
        
        # Clean and sanitize column names
        cleaned_df = df.copy()
        cleaned_df.columns = [sanitize_column_name(c) for c in cleaned_df.columns]

        # Write to SQLite
        with self.engine.begin() as conn:
            cleaned_df.to_sql(table_name, conn, if_exists="replace", index=False)
            
            # Record metadata in catalog
            import json
            conn.execute(
                text("""
                    INSERT INTO _dataset_catalog (table_name, original_filename, row_count, column_count, columns_json, dtypes_json)
                    VALUES (:table_name, :original_filename, :row_count, :column_count, :columns_json, :dtypes_json)
                    ON CONFLICT(table_name) DO UPDATE SET
                        original_filename=excluded.original_filename,
                        row_count=excluded.row_count,
                        column_count=excluded.column_count,
                        columns_json=excluded.columns_json,
                        dtypes_json=excluded.dtypes_json,
                        uploaded_at=CURRENT_TIMESTAMP
                """),
                {
                    "table_name": table_name,
                    "original_filename": original_filename,
                    "row_count": len(cleaned_df),
                    "column_count": len(cleaned_df.columns),
                    "columns_json": json.dumps(list(cleaned_df.columns)),
                    "dtypes_json": json.dumps({c: str(t) for c, t in cleaned_df.dtypes.items()})
                }
            )
        return table_name

    def list_datasets(self) -> List[Dict[str, Any]]:
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM _dataset_catalog ORDER BY uploaded_at DESC"))
            return [dict(row._mapping) for row in result]

    def get_dataset_metadata(self, table_name: str) -> Optional[Dict[str, Any]]:
        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM _dataset_catalog WHERE table_name = :table_name"),
                {"table_name": table_name}
            ).first()
            return dict(result._mapping) if result else None

    def read_table(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """Safely read records from a verified dataset table."""
        # Validate that table exists in catalog to prevent arbitrary table reading
        meta = self.get_dataset_metadata(table_name)
        if not meta:
            raise ValueError(f"Unauthorized or non-existent table: {table_name}")
        
        query = f"SELECT * FROM {table_name}"
        if limit and limit > 0:
            query += f" LIMIT {int(limit)}"
            
        with self.engine.connect() as conn:
            return pd.read_sql_query(text(query), conn)
