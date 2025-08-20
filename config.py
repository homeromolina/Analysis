"""
Configuration file for CrewAI Learning Example
Loads environment variables and provides configuration settings
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the CrewAI Learning Example"""
    
    # Google Cloud Configuration
    USE_GOOGLE_CLI_AUTH = os.getenv("USE_GOOGLE_CLI_AUTH", "false").lower() == "true"
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
    GCP_LOCATION = os.getenv("GCP_LOCATION", "")
    
    # Model Configuration
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash-001")
    
    # Agent Configuration
    AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.2"))
    AGENT_VERBOSE = os.getenv("AGENT_VERBOSE", "true").lower() == "true"
    
    # Web Scraping Configuration
    SCRAPING_TIMEOUT = int(os.getenv("SCRAPING_TIMEOUT", "30"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "10000"))
    
    # Gemini API Key
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        if not cls.USE_GOOGLE_CLI_AUTH and not cls.GEMINI_API_KEY:
            print("Warning: Either USE_GOOGLE_CLI_AUTH must be true or GEMINI_API_KEY must be provided")
            return False
        return True
