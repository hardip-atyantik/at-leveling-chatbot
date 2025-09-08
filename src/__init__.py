"""RAG Chatbot - Simplified imports for better DX"""

from .core.config import Config, get_config, handle_errors
from .core.rag import (
    create_embeddings,
    create_qdrant_client,
    create_vector_store,
    create_rag_chain,
    create_or_verify_collection
)
from .ingestion.pipeline import ingest_documents
from .utils.prompts import load_prompt, get_prompts

__all__ = [
    # Config
    'Config',
    'get_config',
    'handle_errors',
    # RAG components
    'create_embeddings',
    'create_qdrant_client', 
    'create_vector_store',
    'create_rag_chain',
    'create_or_verify_collection',
    # Ingestion
    'ingest_documents',
    # Prompts
    'load_prompt',
    'get_prompts'
]

__version__ = '2.0.0'