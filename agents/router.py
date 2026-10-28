"""
Request Router for Agentic AI Data Agent.
Classifies incoming user questions into specialized agent workflows.
"""
import re
from typing import Dict, Any, List
from models.schemas import AgentIntent, RouterResponse

# Heuristic patterns for intent classification
INTENT_PATTERNS = {
    AgentIntent.DATA_QUALITY_ANALYST: [
        r"\bmissing\b", r"\bnull\b", r"\bna\b", r"\bduplicate\b",
        r"\bquality\b", r"\boutlier\b", r"\banomal(y|ies)\b",
        r"\bdata types?\b", r"\binvalid\b", r"\bclean\b"
    ],
    AgentIntent.SQL_ANALYST: [
        r"\bselect\b", r"\btop\b", r"\bfirst\b", r"\blast\b",
        r"\blimit\b", r"\border by\b", r"\bwhere\b", r"\bquery\b",
        r"\bfilter\b", r"\bshow\b.*\brecords?\b", r"\brow\b"
    ],
    AgentIntent.DATA_ANALYST: [
        r"\baverage\b", r"\bmean\b", r"\bmedian\b", r"\bmax\b",
        r"\bmaximum\b", r"\bmin\b", r"\bminimum\b", r"\bsum\b",
        r"\bgroup by\b", r"\bcorrelat(ion|e)\b", r"\bchart\b",
        r"\bplot\b", r"\bhistogram\b", r"\bdistribution\b",
        r"\bstandard deviation\b", r"\bstd\b", r"\bcount\b", r"\bsummary\b"
    ],
    AgentIntent.GENERAL_HELP: [
        r"\bhelp\b", r"\bhow (do|to|can)\b", r"\bexplain\b",
        r"\bwhat (is|can|does)\b", r"\bguide\b", r"\bdocumentation\b",
        r"\bwho are you\b"
    ]
}

class RequestRouter:
    """
    Deterministic Rule-Based Intent Classifier.
    Routes requests to SQL Analyst, Data Analyst, Data Quality Analyst, or General Help.
    """
    def __init__(self):
        pass

    def classify_request(self, user_request: str) -> RouterResponse:
        req_clean = user_request.strip().lower()
        if not req_clean:
            return RouterResponse(
                detected_intent=AgentIntent.GENERAL_HELP,
                selected_agent="General Help Assistant",
                reason="Empty query provided; default to general help.",
                user_request=user_request,
                confidence=1.0
            )

        # 1. Check Data Quality keywords first (high specificity)
        for pattern in INTENT_PATTERNS[AgentIntent.DATA_QUALITY_ANALYST]:
            if re.search(pattern, req_clean):
                return RouterResponse(
                    detected_intent=AgentIntent.DATA_QUALITY_ANALYST,
                    selected_agent="Data Quality Analyst",
                    reason=f"Matched data quality pattern: {pattern}",
                    user_request=user_request,
                    confidence=0.95
                )

        # 2. Check General Help
        for pattern in INTENT_PATTERNS[AgentIntent.GENERAL_HELP]:
            if re.search(pattern, req_clean):
                return RouterResponse(
                    detected_intent=AgentIntent.GENERAL_HELP,
                    selected_agent="General Help Assistant",
                    reason=f"Matched general help inquiry pattern: {pattern}",
                    user_request=user_request,
                    confidence=0.95
                )

        # 3. Check Data Analyst (statistical aggregations, correlations, distributions)
        for pattern in INTENT_PATTERNS[AgentIntent.DATA_ANALYST]:
            if re.search(pattern, req_clean):
                return RouterResponse(
                    detected_intent=AgentIntent.DATA_ANALYST,
                    selected_agent="Data Analyst",
                    reason=f"Matched statistical/analytics pattern: {pattern}",
                    user_request=user_request,
                    confidence=0.90
                )

        # 4. Check SQL Analyst (record queries, slicing, top/bottom rows)
        for pattern in INTENT_PATTERNS[AgentIntent.SQL_ANALYST]:
            if re.search(pattern, req_clean):
                return RouterResponse(
                    detected_intent=AgentIntent.SQL_ANALYST,
                    selected_agent="SQL Analyst",
                    reason=f"Matched SQL record retrieval pattern: {pattern}",
                    user_request=user_request,
                    confidence=0.90
                )

        # Default fallback
        return RouterResponse(
            detected_intent=AgentIntent.DATA_ANALYST,
            selected_agent="Data Analyst",
            reason="No explicit keywords matched; defaulted to general exploratory data analysis.",
            user_request=user_request,
            confidence=0.50
        )
