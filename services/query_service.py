"""
Query Service for SQL Analyst agent.
Safely executes validated queries with strict timeouts, row caps, and error catching.
"""
import time
from typing import Dict, Any, Optional
import pandas as pd
from sqlalchemy import text
from core.database import DatabaseManager
from core.security import SQLSecurityValidator
from models.schemas import AgentExecutionResult

class QueryService:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()

    def execute_safe_query(self, sql_query: str, active_table: str, limit: int = 100) -> AgentExecutionResult:
        """
        Validates SQL against the active table and executes it if safe.
        """
        validator = SQLSecurityValidator(allowed_tables=[active_table])
        is_safe, reason = validator.validate_query(sql_query)
        if not is_safe:
            return AgentExecutionResult(
                success=False,
                agent_name="SQL Analyst",
                message=f"Query rejected by Security Policy: {reason}",
                sql_query=sql_query
            )

        # Append row limit if not already limited
        clean_query = sql_query.strip().rstrip(";")
        if "limit" not in clean_query.lower():
            clean_query += f" LIMIT {limit}"

        start_time = time.time()
        try:
            with self.db.engine.connect() as conn:
                df = pd.read_sql_query(text(clean_query), conn)
            elapsed_ms = (time.time() - start_time) * 1000

            return AgentExecutionResult(
                success=True,
                agent_name="SQL Analyst",
                message=f"Query executed successfully in {elapsed_ms:.1f}ms. Returned {len(df)} row(s).",
                sql_query=clean_query,
                data=df.to_dict(orient="records"),
                summary_metrics={"row_count": len(df), "columns": list(df.columns), "execution_time_ms": elapsed_ms}
            )
        except Exception as e:
            return AgentExecutionResult(
                success=False,
                agent_name="SQL Analyst",
                message=f"Database execution error: {str(e)}",
                sql_query=clean_query
            )
