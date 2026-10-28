"""
Data Quality Analyst Agent.
Executes automated data quality profiling and summarizes findings.
"""
from typing import Optional
from core.database import DatabaseManager
from services.quality_service import QualityService
from models.schemas import AgentExecutionResult

class DataQualityAnalystAgent:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()
        self.quality = QualityService()

    def process(self, user_request: str, table_name: str) -> AgentExecutionResult:
        df = self.db.read_table(table_name)
        if df.empty:
            return AgentExecutionResult(
                success=False,
                agent_name="Data Quality Analyst",
                message="Dataset is empty; cannot perform quality audit."
            )

        audit = self.quality.perform_quality_audit(df)
        findings = audit["findings"]
        msg = f"Data quality check complete. Found {len(findings)} noteworthy pattern(s)." if findings else "Data quality check complete: Clean dataset with 0 detected issues."

        return AgentExecutionResult(
            success=True,
            agent_name="Data Quality Analyst",
            message=msg,
            quality_issues=findings,
            summary_metrics=audit
        )
