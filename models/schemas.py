"""
Pydantic schemas and data models for Agentic AI Data Agent.
"""
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class AgentIntent(str, Enum):
    SQL_ANALYST = "SQL_ANALYST"
    DATA_ANALYST = "DATA_ANALYST"
    DATA_QUALITY_ANALYST = "DATA_QUALITY_ANALYST"
    GENERAL_HELP = "GENERAL_HELP"

class RouterResponse(BaseModel):
    detected_intent: AgentIntent
    selected_agent: str
    reason: str
    user_request: str
    confidence: float = 1.0

class QueryExecutionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    REJECTED = "REJECTED"

class QueryHistoryRecord(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_question: str
    detected_intent: AgentIntent
    selected_workflow: str
    execution_status: QueryExecutionStatus
    details: Optional[str] = None
    execution_time_ms: Optional[float] = None

class DatasetMetadata(BaseModel):
    table_name: str
    original_filename: str
    row_count: int
    column_count: int
    columns: List[str]
    dtypes: Dict[str, str]
    file_size_bytes: int
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class AgentExecutionResult(BaseModel):
    success: bool
    agent_name: str
    message: str
    data: Optional[List[Dict[str, Any]]] = None
    sql_query: Optional[str] = None
    chart_spec: Optional[Dict[str, Any]] = None
    summary_metrics: Optional[Dict[str, Any]] = None
    quality_issues: Optional[List[str]] = None
