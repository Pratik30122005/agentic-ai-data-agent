"""
SQL Analyst Agent.
Translates user questions into safe SQL queries using deterministic templates
or optional LLM prompts (always validated before execution).
"""
import re
from typing import List, Dict, Any, Optional
from core.database import DatabaseManager
from services.query_service import QueryService
from models.schemas import AgentExecutionResult

class SQLAnalystAgent:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()
        self.query_service = QueryService(self.db)

    def process(self, user_request: str, table_name: str) -> AgentExecutionResult:
        meta = self.db.get_dataset_metadata(table_name)
        if not meta:
            return AgentExecutionResult(
                success=False,
                agent_name="SQL Analyst",
                message=f"Table {table_name} does not exist or has not been loaded."
            )

        import json
        columns = json.loads(meta["columns_json"])

        sql_query = self._generate_sql_query(user_request, table_name, columns)
        return self.query_service.execute_safe_query(sql_query, table_name)

    def _generate_sql_query(self, query_text: str, table: str, columns: List[str]) -> str:
        q = query_text.lower()

        # 1. Check for top N / limit requests
        top_match = re.search(r"top\s+(\d+)", q)
        limit = top_match.group(1) if top_match else "10"

        # Check for ordering column
        order_col = None
        for col in columns:
            if col.lower() in q:
                order_col = col
                break

        # Check if requesting highest/top/descending
        is_desc = any(w in q for w in ["highest", "top", "best", "most", "desc"])

        if "artist" in columns and "popularity" in columns and ("artist" in q or "highest" in q):
            return f"SELECT artist_name, AVG(popularity) as avg_popularity, COUNT(*) as track_count FROM {table} GROUP BY artist_name ORDER BY avg_popularity DESC LIMIT {limit}"

        if order_col:
            direction = "DESC" if is_desc else "ASC"
            return f"SELECT * FROM {table} ORDER BY {order_col} {direction} LIMIT {limit}"

        if "top" in q or "records" in q or "rows" in q or "first" in q:
            return f"SELECT * FROM {table} LIMIT {limit}"

        return f"SELECT * FROM {table} LIMIT {limit}"
