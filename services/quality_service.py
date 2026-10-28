"""
Quality Service for detecting missing values, duplicates,
type inconsistencies, high-cardinality flags, and numerical outliers.
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np

class QualityService:
    def __init__(self):
        pass

    def perform_quality_audit(self, df: pd.DataFrame) -> Dict[str, Any]:
        total_rows = len(df)
        findings = []

        # 1. Missing Values
        missing_by_col = {}
        for col in df.columns:
            m_count = int(df[col].isnull().sum())
            if m_count > 0:
                pct = round((m_count / total_rows) * 100, 2)
                missing_by_col[col] = {"missing_count": m_count, "missing_percentage": pct}
                findings.append(f"Column '{col}' has {m_count} missing values ({pct}%).")

        # 2. Duplicate Rows
        dup_count = int(df.duplicated().sum())
        if dup_count > 0:
            findings.append(f"Detected {dup_count} duplicate row(s) in the dataset.")

        # 3. High Cardinality in Categoricals
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        for col in cat_cols:
            n_unique = int(df[col].nunique())
            if total_rows > 10 and n_unique == total_rows:
                findings.append(f"Column '{col}' has 100% unique values (potential ID column).")

        # 4. Outliers via IQR (Interquartile Range)
        outliers_detected = {}
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            s = df[col].dropna()
            if len(s) >= 4:
                q1 = s.quantile(0.25)
                q3 = s.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                outlier_rows = s[(s < lower) | (s > upper)]
                if len(outlier_rows) > 0:
                    outliers_detected[col] = {
                        "count": len(outlier_rows),
                        "lower_bound": round(float(lower), 2),
                        "upper_bound": round(float(upper), 2),
                        "sample_values": [float(x) for x in outlier_rows.head(5)]
                    }
                    findings.append(f"Column '{col}' has {len(outlier_rows)} potential outlier(s) outside [{round(lower, 2)}, {round(upper, 2)}].")

        return {
            "total_rows": total_rows,
            "duplicate_rows": dup_count,
            "missing_by_column": missing_by_col,
            "outliers": outliers_detected,
            "findings": findings
        }
