"""
Application configuration settings.
"""
import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

class AppConfig(BaseModel):
    app_name: str = "Agentic AI Data Agent"
    max_upload_size_mb: int = 25
    sqlite_db_path: str = str(BASE_DIR / "data" / "agent_data.db")
    default_row_limit: int = 100
    llm_provider: str = os.getenv("LLM_PROVIDER", "none")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

settings = AppConfig()
