"""
Data Analyst Agent.
Handles statistical questions, aggregations, distributions, and generates chart data.
"""
import re
from typing import Optional, Dict, Any, List
import pandas as pd
from core.database import DatabaseManager
from services.analytics_service import AnalyticsService
from models.schemas import AgentExecutionResult

class DataAnalystAgent:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()
        self.analytics = AnalyticsService()

    def process(self, user_request: str, table_name: str) -> AgentExecutionResult:
        df = self.db.read_table(table_name)
        if df.empty:
            return AgentExecutionResult(
                success=False,
                agent_name="Data Analyst",
                message="Dataset is empty."
            )

        q = user_request.lower()

        # Check for correlation request
        if "correlat" in q:
            corrs = self.analytics.compute_correlations(df)
            if not corrs:
                return AgentExecutionResult(
                    success=False,
                    agent_name="Data Analyst",
                    message="Not enough numeric columns found to calculate correlations."
                )
            return AgentExecutionResult(
                success=True,
                agent_name="Data Analyst",
                message="Computed Pearson correlation matrix across numeric features.",
                summary_metrics={"correlations": corrs}
            )

        # Check for group-by request
        group_candidate = None
        for col in df.select_dtypes(include=["object", "category"]).columns:
            if col.lower() in q:
                group_candidate = col
                break

        metric_candidate = None
        for col in df.select_dtypes(include=["number"]).columns:
            if col.lower() in q:
                metric_candidate = col
                break

        if group_candidate and metric_candidate:
            grouped = self.analytics.compute_groupby_metric(df, group_candidate, metric_candidate)
            return AgentExecutionResult(
                success=True,
                agent_name="Data Analyst",
                message=f"Aggregated {metric_candidate} grouped by {group_candidate}.",
                data=grouped.to_dict(orient="records"),
                chart_spec={"type": "bar", "x": group_candidate, "y": f"avg_{metric_candidate}"}
            )

        # Default: Compute summary statistics
        stats = self.analytics.compute_summary_statistics(df)
        return AgentExecutionResult(
            success=True,
            agent_name="Data Analyst",
            message="Calculated comprehensive descriptive statistics for numeric attributes.",
            summary_metrics={"descriptive_statistics": stats}
        )
