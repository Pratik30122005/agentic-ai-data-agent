"""
Automated tests for Router, SQL Analyst, Data Analyst, Quality Analyst, and SQL Security.
"""
import pytest
import pandas as pd
from agents.router import RequestRouter
from models.schemas import AgentIntent
from core.database import DatabaseManager
from core.security import SQLSecurityValidator
from services.query_service import QueryService
from services.analytics_service import AnalyticsService
from services.quality_service import QualityService

@pytest.fixture
def test_db(tmp_path):
    db_file = tmp_path / "agent_test.db"
    db_mgr = DatabaseManager(db_path=str(db_file))
    
    # Ingest sample data
    df = pd.DataFrame({
        "track_id": ["t1", "t2", "t3", "t4"],
        "artist_name": ["Luna", "Luna", "Nova", "Nova"],
        "popularity": [80.0, 90.0, 70.0, None],
        "energy": [0.8, 0.9, 0.5, 0.6]
    })
    db_mgr.store_dataset(df, "music.csv")
    return db_mgr

def test_router_classification():
    router = RequestRouter()
    
    r1 = router.classify_request("Show me the top 10 records")
    assert r1.detected_intent == AgentIntent.SQL_ANALYST
    
    r2 = router.classify_request("Find missing values in every column")
    assert r2.detected_intent == AgentIntent.DATA_QUALITY_ANALYST
    
    r3 = router.classify_request("Calculate average popularity by artist")
    assert r3.detected_intent == AgentIntent.DATA_ANALYST
    
    r4 = router.classify_request("How do I use this application?")
    assert r4.detected_intent == AgentIntent.GENERAL_HELP

def test_sql_security_validator():
    validator = SQLSecurityValidator(allowed_tables=["dataset_music_123456"])
    
    # Safe SELECT
    safe, msg = validator.validate_query("SELECT * FROM dataset_music_123456 LIMIT 5")
    assert safe is True
    
    # Block DROP
    safe, msg = validator.validate_query("DROP TABLE dataset_music_123456")
    assert safe is False
    assert "SELECT" in msg or "Forbidden" in msg
    
    # Block INSERT
    safe, msg = validator.validate_query("INSERT INTO dataset_music_123456 VALUES (1, 2)")
    assert safe is False
    
    # Block stacked queries
    safe, msg = validator.validate_query("SELECT * FROM dataset_music_123456; DROP TABLE dataset_music_123456")
    assert safe is False
    assert "Multiple statements" in msg
    
    # Block unauthorized table
    safe, msg = validator.validate_query("SELECT * FROM users_private")
    assert safe is False
    assert "unauthorized table" in msg

def test_analytics_and_quality_services():
    df = pd.DataFrame({
        "artist": ["A", "A", "B", "B"],
        "score": [10.0, 20.0, 30.0, 100.0]
    })
    analytics = AnalyticsService()
    stats = analytics.compute_summary_statistics(df)
    assert stats["score"]["mean"] == 40.0
    assert stats["score"]["max"] == 100.0
    
    # Quality check
    quality = QualityService()
    audit = quality.perform_quality_audit(df)
    assert audit["total_rows"] == 4
    assert audit["duplicate_rows"] == 0
