"""Configuration management"""
from pathlib import Path

from pydantic_settings import BaseSettings

# backend/ (parent of app/)
_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_PROJECT_ROOT = _BACKEND_ROOT.parent


class Settings(BaseSettings):
    """Application settings"""

    PROJECT_ROOT: Path = _PROJECT_ROOT
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Cursor Bridge
    CURSOR_BRIDGE_BACKEND: str = "mock"
    CURSOR_BRIDGE_API_KEY: str = "sk-curbr-local-dev"
    CURSOR_BRIDGE_PUBLIC_URL: str = "http://127.0.0.1:8000/api/cursor-bridge"
    CURSOR_BRIDGE_MODELS: str = "cursor-fast,composer-2.5"
    CURSOR_MCP_COMMAND: str = "npx"
    CURSOR_MCP_ARGS: str = "-y,cursor-bridge-mcp"

    # Data paths (see contracts/event_schema.json ingestion flow)
    DATA_DIR: Path = _PROJECT_ROOT / "data"
    EVENTS_DIR: Path = DATA_DIR / "processed" / "events"
    
    # LLM Settings
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4"
    
    # Embeddings Settings
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Database Settings
    DATABASE_URL: str = "postgresql://user:password@localhost/company_brain"
    
    # Vector Store Settings
    VECTOR_STORE_TYPE: str = "pinecone"
    
    # Slack Settings
    SLACK_BOT_TOKEN: str = ""
    SLACK_SIGNING_SECRET: str = ""
    
    @property
    def cursor_mcp_args_list(self) -> list[str]:
        return [arg.strip() for arg in self.CURSOR_MCP_ARGS.split(",") if arg.strip()]

    @property
    def cursor_bridge_models_list(self) -> list[str]:
        return [model.strip() for model in self.CURSOR_BRIDGE_MODELS.split(",") if model.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
