"""
Smoke tests for Phase 1 of Agentic AI Data Agent.
"""
import os
import pandas as pd
from models.schemas import RouterResponse, AgentIntent, DatasetMetadata, QueryExecutionStatus

def test_environment_and_imports():
    assert AgentIntent.SQL_ANALYST == "SQL_ANALYST"
    assert AgentIntent.DATA_ANALYST == "DATA_ANALYST"
    assert AgentIntent.DATA_QUALITY_ANALYST == "DATA_QUALITY_ANALYST"
    assert AgentIntent.GENERAL_HELP == "GENERAL_HELP"

def test_synthetic_dataset_exists():
    path = "data/sample_spotify.csv"
    assert os.path.exists(path), f"{path} must exist"
    df = pd.read_csv(path)
    assert len(df) == 30, f"Expected 30 rows, got {len(df)}"
    required_cols = [
        "track_id", "track_name", "artist_name", "album_name",
        "popularity", "duration_ms", "danceability", "energy", "release_year"
    ]
    for col in required_cols:
        assert col in df.columns, f"Column {col} missing from synthetic dataset"

def test_pydantic_schema_validation():
    sample_route = RouterResponse(
        detected_intent=AgentIntent.SQL_ANALYST,
        selected_agent="SQL Analyst",
        reason="Keyword match: top records",
        user_request="Show me top 5 tracks"
    )
    assert sample_route.detected_intent == AgentIntent.SQL_ANALYST
    assert sample_route.confidence == 1.0
