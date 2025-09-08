"""Centralized configuration using environment variables with sensible defaults"""

import os
from dataclasses import dataclass, field
from typing import Optional
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Central configuration with environment variable support"""
    
    # Collection settings
    collection_name: str = field(default_factory=lambda: os.getenv("COLLECTION_NAME", "atyantik-chatbot-openai"))
    
    # Processing settings
    chunk_size: int = field(default_factory=lambda: int(os.getenv("CHUNK_SIZE", "2048")))
    chunk_overlap: int = field(default_factory=lambda: int(os.getenv("CHUNK_OVERLAP", "0")))
    batch_size: int = field(default_factory=lambda: int(os.getenv("BATCH_SIZE", "2")))
    mmr_k: int = field(default_factory=lambda: int(os.getenv("MMR_K", "3")))
    embedding_batch_size: int = field(default_factory=lambda: int(os.getenv("EMBEDDING_BATCH_SIZE", "1000")))
    
    # File paths
    pdf_path: str = field(default_factory=lambda: os.getenv("PDF_PATH", "./Career Leveling Guide.pdf"))
    
    # Optimization settings
    max_processes: int = field(default_factory=lambda: int(os.getenv("MAX_PROCESSES", "8")))
    
    # Opik settings (hardcoded as per requirements)
    opik_workspace: str = field(default_factory=lambda: os.getenv("OPIK_WORKSPACE", "knightkill"))
    opik_project: str = field(default_factory=lambda: os.getenv("OPIK_PROJECT", "atyantik-chatbot"))
    
    def __post_init__(self):
        """Setup environment after initialization"""
        self.setup_environment()
    
    def setup_environment(self):
        """Setup runtime environment variables"""
        # Opik configuration
        os.environ['OPIK_WORKSPACE'] = self.opik_workspace
        os.environ['OPIK_PROJECT_NAME'] = self.opik_project
        
        # M1 Pro optimization
        os.environ['OMP_NUM_THREADS'] = str(self.max_processes)
        os.environ['MKL_NUM_THREADS'] = str(self.max_processes)
        os.environ['NUMEXPR_NUM_THREADS'] = str(self.max_processes)
    
    @staticmethod
    def validate_environment() -> list[str]:
        """Validate required environment variables"""
        required = [
            # Azure OpenAI
            'AZURE_OPENAI_API_KEY',
            'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_API_VERSION',
            'AZURE_OPENAI_DEPLOYMENT_NAME',
            'AZURE_OPENAI_EMBEDDINGS_API_KEY',
            'AZURE_OPENAI_EMBEDDINGS_ENDPOINT',
            'AZURE_OPENAI_EMBEDDINGS_API_VERSION',
            'AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME',
            # Qdrant
            'QDRANT_URL',
            'QDRANT_API_KEY'
        ]
        return [var for var in required if not os.getenv(var)]


@lru_cache(maxsize=1)
def get_config() -> Config:
    """Get singleton config instance"""
    return Config()


def handle_errors(message: str):
    """Decorator for cleaner error handling"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"❌ {message}: {str(e)}")
                raise
        return wrapper
    return decorator