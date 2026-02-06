"""
Project Longshot - Global Configuration
========================================
Central configuration management for all modules.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = DATA_DIR / "logs"
PRECEDENTS_DIR = DATA_DIR / "precedents"
ASSETS_DIR = DATA_DIR / "assets"

# Ensure directories exist
for dir_path in [DATA_DIR, LOGS_DIR, PRECEDENTS_DIR, ASSETS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


class APIConfig(BaseModel):
    """API keys and endpoints configuration."""
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")


class DatabaseConfig(BaseModel):
    """Database configuration."""
    url: str = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/longshot.db")
    echo: bool = os.getenv("DB_ECHO", "false").lower() == "true"


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module}:{function}:{line} - {message}"
    rotation: str = "10 MB"
    retention: str = "7 days"


class FeatureFlags(BaseModel):
    """Feature toggle configuration."""
    enable_blockchain_ledger: bool = os.getenv("ENABLE_BLOCKCHAIN_LEDGER", "false").lower() == "true"
    enable_3d_visualization: bool = os.getenv("ENABLE_3D_VISUALIZATION", "true").lower() == "true"
    enable_simulation_mode: bool = os.getenv("ENABLE_SIMULATION_MODE", "true").lower() == "true"
    enable_ai_council: bool = os.getenv("ENABLE_AI_COUNCIL", "true").lower() == "true"


class ModuleConfig(BaseModel):
    """Individual module settings."""
    detective_max_results: int = int(os.getenv("DETECTIVE_MAX_RESULTS", "5"))
    detective_retry_attempts: int = int(os.getenv("DETECTIVE_RETRY_ATTEMPTS", "3"))
    seer_simulation_depth: int = int(os.getenv("SEER_SIMULATION_DEPTH", "5"))
    council_debate_rounds: int = int(os.getenv("COUNCIL_DEBATE_ROUNDS", "3"))
    historian_max_precedents: int = int(os.getenv("HISTORIAN_MAX_PRECEDENTS", "10"))


class Config(BaseModel):
    """Main configuration class combining all sub-configs."""
    api: APIConfig = APIConfig()
    database: DatabaseConfig = DatabaseConfig()
    logging: LoggingConfig = LoggingConfig()
    features: FeatureFlags = FeatureFlags()
    modules: ModuleConfig = ModuleConfig()
    
    # Project metadata
    project_name: str = "Project Longshot"
    version: str = "1.0.0"
    description: str = "AI-Powered Strategic Intelligence & Crisis Management System"


# Global config instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config


if __name__ == "__main__":
    # Print current configuration
    import json
    print("🎯 Project Longshot Configuration")
    print("=" * 50)
    print(json.dumps(config.model_dump(), indent=2, default=str))
