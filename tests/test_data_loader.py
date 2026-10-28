"""
Automated tests for Phase 2: Data Loader and SQLite Storage.
"""
import pytest
import os
import io
import pandas as pd
from core.database import DatabaseManager, sanitize_table_name, sanitize_column_name
from services.data_loader import DataLoaderService

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_data.db"
    db_mgr = DatabaseManager(db_path=str(db_file))
    return db_mgr

def test_sanitize_table_name():
    name1 = sanitize_table_name("My Dataset (2024)! .csv")
    assert name1.startswith("dataset_my_dataset_2024_")
    assert "!" not in name1
    assert " " not in name1

def test_sanitize_column_name():
    assert sanitize_column_name("Artist Name!") == "artist_name"
    assert sanitize_column_name("123_rank") == "col_123_rank"
    assert sanitize_column_name("   Danceability %  ") == "danceability"

def test_valid_csv_ingestion(temp_db):
    service = DataLoaderService(db_manager=temp_db)
    csv_data = b"id,name,val\n1,Alpha,10.5\n2,Beta,20.0\n"
    table_name, profile = service.ingest_csv(csv_data, "test.csv")
    
    assert profile["row_count"] == 2
    assert profile["column_count"] == 3
    assert table_name.startswith("dataset_test_")
    
    df_read = temp_db.read_table(table_name)
    assert len(df_read) == 2
    assert list(df_read.columns) == ["id", "name", "val"]

def test_empty_file_rejection(temp_db):
    service = DataLoaderService(db_manager=temp_db)
    with pytest.raises(ValueError, match="completely empty"):
        service.ingest_csv(b"", "empty.csv")

def test_malformed_csv_rejection(temp_db):
    service = DataLoaderService(db_manager=temp_db)
    with pytest.raises(ValueError, match="Malformed CSV"):
        service.ingest_csv(b"id,name\n1,Alpha\n2,Beta,ExtraField\n", "bad.csv")

def test_reupload_dataset_replaces_cleanly(temp_db):
    service = DataLoaderService(db_manager=temp_db)
    data1 = b"id,score\n1,100\n"
    data2 = b"id,score\n1,200\n2,300\n"
    
    t1, _ = service.ingest_csv(data1, "grades.csv")
    t2, _ = service.ingest_csv(data2, "grades.csv")
    assert t1 == t2
    
    df_read = temp_db.read_table(t2)
    assert len(df_read) == 2
    assert df_read["score"].tolist() == [200, 300]
