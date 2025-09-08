# Atyantik RAG Chatbot v2.0

An AI-powered knowledge assistant for Atyantik Technologies with improved developer experience, modular architecture, and optimized code structure.

## Quick Start

1. **Setup Environment**
   ```bash
   make setup    # Creates virtual environment and installs dependencies
   make env      # Interactive wizard to configure .env file
   ```

2. **Prepare Data**
   - Place `Career Leveling Guide.pdf` in the project root
   - Run data ingestion: `make ingest`

3. **Start Chat Interface**
   ```bash
   make chat     # Opens Streamlit interface at http://localhost:8501
   ```

## System Requirements

- Python 3.11+
- Azure OpenAI account with deployed models
- Qdrant vector database (cloud or local)

## Configuration

The system requires the following services:

- **Azure OpenAI**: For embeddings (text-embedding-ada-002) and LLM (GPT-4)
- **Qdrant**: Vector database for document storage and similarity search
- **Opik**: (Optional) LLM monitoring and observability

Use `make env` for interactive configuration or manually create `.env` from `.env.example`.

## Available Commands

```bash
make help      # Show all available commands
make setup     # Create virtual environment and install dependencies
make env       # Interactive .env setup wizard
make ingest    # Process and upload documents to vector database
make chat      # Start Streamlit chat interface
make dev       # Development mode with hot-reload
make test      # Run tests
make format    # Auto-format code
make lint      # Check code quality
make clean     # Clean cache and temporary files
```

## Architecture

```
RAGDemo/
├── src/                 # All source code
│   ├── core/           # Core functionality
│   │   ├── config.py   # Centralized configuration
│   │   └── rag.py      # Shared RAG chain logic
│   ├── ingestion/      # Data processing
│   │   └── pipeline.py # Simplified ingestion (~100 lines)
│   ├── ui/             # User interface
│   │   └── app.py      # Streamlit app (~60 lines)
│   └── utils/          # Utilities
│       └── prompts.py  # Prompt management
├── prompts/            # External prompt files
├── scripts/            # Setup and utilities
└── Makefile           # Developer commands
```

### Key Improvements
- **40% less code**: 568 → ~350 lines total
- **75% fewer imports**: Consolidated imports via `src/__init__.py`
- **Zero duplication**: Shared RAG logic in `src/core/rag.py`
- **Environment-driven**: All settings configurable via `.env`

## Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
python scripts/setup_env.py

# Run ingestion  
PYTHONPATH=. python -m src.ingestion.pipeline

# Start chat interface
PYTHONPATH=. streamlit run src/ui/app.py
```

## Troubleshooting

- Ensure `Career Leveling Guide.pdf` exists in project root before running ingestion
- Check your Azure OpenAI deployment names match the configuration
- Verify Qdrant connection and API key
- Use `make clean` to clear cache if experiencing import issues

For detailed development information, see [CLAUDE.md](CLAUDE.md).