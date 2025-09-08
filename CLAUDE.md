# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview (v2.0 - Refactored)

This is a RAG (Retrieval Augmented Generation) chatbot system for Atyantik Technologies with improved developer experience. The system features modular architecture, shared components, and environment-driven configuration for better maintainability and reduced code duplication.

## Project Structure

```
RAGDemo/
├── src/                    # All source code (modular architecture)
│   ├── __init__.py        # Package exports for simple imports
│   ├── core/              # Core functionality
│   │   ├── config.py      # Environment-driven configuration
│   │   └── rag.py         # Shared RAG chain components
│   ├── ingestion/         # Data processing
│   │   └── pipeline.py    # Simplified ingestion (100 lines)
│   ├── ui/                # User interface  
│   │   └── app.py         # Streamlit app (60 lines)
│   └── utils/             # Utilities
│       └── prompts.py     # Prompt loader
├── prompts/               # External prompt templates
│   ├── system_cto.txt    # CTO persona prompt
│   └── user_query.txt    # User query template
├── scripts/               # Setup and utility scripts
│   └── setup_env.py      # Interactive .env wizard
├── Makefile              # Enhanced developer commands
├── README.md             # Installation guide
├── requirements.txt      # Python dependencies
└── CLAUDE.md            # This documentation
```

## Core Architecture

### Simplified Architecture (v2.0)

#### Core Module (`src/core/`)
- **config.py**: Dataclass-based configuration with environment variable support
- **rag.py**: Shared RAG chain factory functions used by both ingestion and chat

#### Ingestion Module (`src/ingestion/pipeline.py`)
- Reduced from 269 lines to ~100 lines
- Single entry point: `ingest_documents()`
- Reuses RAG components from `core/rag.py`

#### UI Module (`src/ui/app.py`)
- Reduced from 119 lines to ~60 lines  
- Simplified initialization using shared components
- Cleaner error handling with decorators

### Key Improvements

#### Code Reduction (40% less code)
- **Before**: 568 lines across 3 files
- **After**: ~350 lines with better organization
- **Imports**: 75% reduction through consolidated imports

#### Developer Experience
- **Single import**: `from src import *` gets all needed components
- **Environment-driven**: All settings in `.env` with sensible defaults
- **Error handling**: Clean decorator-based error handling
- **Hot reload**: `make dev` for development with auto-reload

#### Better Commands
```bash
make dev     # Development mode with hot-reload
make test    # Run tests
make format  # Auto-format code  
make lint    # Check code quality
```

## Environment Configuration

Required environment variables (from `.env`):
- `QDRANT_URL`: Qdrant vector database URL
- `QDRANT_API_KEY`: Qdrant API authentication
- `AZURE_OPENAI_API_KEY`: Azure OpenAI LLM API key
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI LLM endpoint
- `AZURE_OPENAI_API_VERSION`: Azure OpenAI LLM API version
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Azure OpenAI LLM deployment name
- `AZURE_OPENAI_EMBEDDINGS_API_KEY`: Azure OpenAI embeddings API key
- `AZURE_OPENAI_EMBEDDINGS_ENDPOINT`: Azure OpenAI embeddings endpoint
- `AZURE_OPENAI_EMBEDDINGS_API_VERSION`: Azure OpenAI embeddings API version
- `AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME`: Azure OpenAI embeddings deployment name
- `OPIK_API_KEY`: Opik monitoring API key (optional for monitoring)

All configuration via environment variables with defaults:
```env
COLLECTION_NAME=atyantik-chatbot-openai
CHUNK_SIZE=2048
CHUNK_OVERLAP=0
BATCH_SIZE=2
MMR_K=10
PDF_PATH=./Career Leveling Guide.pdf
MAX_PROCESSES=8
OPIK_WORKSPACE=knightkill
OPIK_PROJECT=atyantik-chatbot
```

## Common Commands

### Quick Start
```bash
make setup     # Create venv and install dependencies
make env       # Setup .env file interactively
make ingest    # Process and upload documents
make chat      # Start chat interface
```

### Development
```bash
make dev       # Run with hot-reload
make test      # Run tests
make format    # Format code with black
make lint      # Check code quality
make clean     # Clean cache files
```

### Direct Python Usage
```python
# Simple import - gets everything needed
from src import *

# Run ingestion
config = get_config()
success = ingest_documents(config=config)

# Create RAG chain
system_prompt, user_prompt = get_prompts()
chain, *_ = create_rag_chain(system_prompt, user_prompt)
```


## Key Dependencies

- **LangChain** (0.3.27): Document processing, text splitting, LLM integration
- **Qdrant** (1.15.1): Vector database for semantic search
- **Azure OpenAI**: Embedding generation (text-embedding-ada-002) and LLM services
- **Streamlit** (1.49.1): Web-based chat interface
- **Opik** (1.8.42): LLM observability and tracing
- **PyPDFium2** (4.30.0): PDF document processing

## Vector Database Schema

- **Collection**: "atyantik-chatbot-openai"
- **Embedding Model**: Azure OpenAI text-embedding-ada-002 (1536 dimensions)
- **Distance Metric**: Cosine similarity
- **Optimization**: Binary quantization enabled for memory efficiency
- **Storage**: On-disk payload storage for large datasets

## Important Implementation Notes

- **Shared Configuration**: All common constants centralized in `config.py` to reduce human error
- **PDF processing**: Uses multiprocessing optimized for M1 Pro (configurable max processes)
- **Batch processing**: Configurable batch sizes for vector uploads to prevent memory issues
- **Environment validation**: Centralized validation with clear error messages
- **Chat interface**: Includes sidebar with clear chat history functionality
- **External prompts**: Text files for easy editing without code changes
- **Development workflow**: Use `make` commands for streamlined operations
- **Setup wizard**: Interactive `.env` configuration via `setup_env.py`
- **Factory patterns**: Shared config provides pre-configured instances to eliminate duplication