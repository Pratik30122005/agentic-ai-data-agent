"""
Analytics service for computing descriptive stats, aggregations,
correlations, and chart specifications using pandas.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

class AnalyticsService:
    def __init__(self):
        pass

    def compute_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        num_df = df.select_dtypes(include=[np.number])
        if num_df.empty:
            return {"numeric_summary": {}, "message": "No numeric columns available."}

        stats = {}
        for col in num_df.columns:
            stats[col] = {
                "mean": round(float(num_df[col].mean()), 4) if not pd.isna(num_df[col].mean()) else None,
                "median": round(float(num_df[col].median()), 4) if not pd.isna(num_df[col].median()) else None,
                "min": round(float(num_df[col].min()), 4) if not pd.isna(num_df[col].min()) else None,
                "max": round(float(num_df[col].max()), 4) if not pd.isna(num_df[col].max()) else None,
                "std": round(float(num_df[col].std()), 4) if not pd.isna(num_df[col].std()) else None,
                "count": int(num_df[col].count())
            }
        return stats

    def compute_correlations(self, df: pd.DataFrame) -> Optional[Dict[str, Dict[str, float]]]:
        num_df = df.select_dtypes(include=[np.number])
        if len(num_df.columns) < 2:
            return None
        corr_matrix = num_df.corr().round(4)
        return corr_matrix.to_dict()

    def compute_groupby_metric(self, df: pd.DataFrame, group_col: str, metric_col: str, agg_func: str = "mean") -> pd.DataFrame:
        if group_col not in df.columns or metric_col not in df.columns:
            raise ValueError(f"Invalid columns for grouping: {group_col}, {metric_col}")
        
        grouped = df.groupby(group_col)[metric_col].agg(["count", "mean", "min", "max"]).reset_index()
        grouped = grouped.rename(columns={
            "count": "record_count",
            "mean": f"avg_{metric_col}",
            "min": f"min_{metric_col}",
            "max": f"max_{metric_col}"
        })
        return grouped.sort_values(by=f"avg_{metric_col}", ascending=False)
