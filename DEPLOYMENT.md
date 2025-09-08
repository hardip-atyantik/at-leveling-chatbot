# Streamlit Cloud Deployment Guide

## Fixed Issues

### 1. ModuleNotFoundError Resolution
- **Root Cause**: Streamlit Cloud doesn't automatically add the project root to Python path
- **Solution**: Added dynamic path resolution in both `src/ui/app.py` and `src/ingestion/pipeline.py`

```python
# Path resolution code added to all entry points
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
```

### 2. Project Structure Improvements
- Added root `__init__.py` for proper package recognition
- Created `setup.py` for formal package structure
- Added Streamlit configuration files

## Deployment Files Created

### Required Files for Streamlit Cloud:
1. `__init__.py` - Root package marker
2. `setup.py` - Package configuration
3. `.streamlit/config.toml` - Streamlit settings
4. `packages.txt` - System dependencies (if needed)

## Deployment Steps

### 1. Pre-deployment Checklist
- [ ] All environment variables configured in Streamlit Cloud secrets
- [ ] Requirements.txt is up to date
- [ ] PDF file is in the repository root
- [ ] Vector database (Qdrant) is accessible from cloud

### 2. Streamlit Cloud Configuration

#### Environment Variables (Required):
Set these in Streamlit Cloud's "Secrets" section:

```toml
# Vector Database
QDRANT_URL = "your-qdrant-cloud-url"
QDRANT_API_KEY = "your-qdrant-api-key"

# Azure OpenAI LLM
AZURE_OPENAI_API_KEY = "your-llm-api-key"
AZURE_OPENAI_ENDPOINT = "your-llm-endpoint"
AZURE_OPENAI_API_VERSION = "2024-02-01"
AZURE_OPENAI_DEPLOYMENT_NAME = "your-llm-deployment"

# Azure OpenAI Embeddings
AZURE_OPENAI_EMBEDDINGS_API_KEY = "your-embeddings-api-key"
AZURE_OPENAI_EMBEDDINGS_ENDPOINT = "your-embeddings-endpoint"
AZURE_OPENAI_EMBEDDINGS_API_VERSION = "2024-02-01"
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME = "your-embeddings-deployment"

# Optional Monitoring
OPIK_API_KEY = "your-opik-api-key"

# Optional Overrides
COLLECTION_NAME = "atyantik-chatbot-openai"
CHUNK_SIZE = "2048"
CHUNK_OVERLAP = "0"
BATCH_SIZE = "2"
MMR_K = "10"
PDF_PATH = "./Career Leveling Guide.pdf"
MAX_PROCESSES = "8"
OPIK_WORKSPACE = "knightkill"
OPIK_PROJECT = "atyantik-chatbot"
```

### 3. App Configuration
- **Main file path**: `src/ui/app.py`
- **Python version**: 3.11+ recommended
- **Advanced settings**: Use Python 3.11 or later

### 4. Repository Structure
Ensure your repository has this structure:
```
your-repo/
├── src/
│   ├── __init__.py
│   ├── ui/
│   │   └── app.py          # ← Main Streamlit app
│   ├── core/
│   │   ├── config.py
│   │   └── rag.py
│   └── utils/
│       └── prompts.py
├── prompts/
│   ├── system_cto.txt
│   └── user_query.txt
├── __init__.py             # ← Added for deployment
├── setup.py                # ← Added for deployment
├── requirements.txt
├── .streamlit/
│   └── config.toml         # ← Added for deployment
└── Career Leveling Guide.pdf
```

## Common Deployment Issues & Solutions

### 1. Import Errors
- **Issue**: `ModuleNotFoundError: No module named 'src'`
- **Solution**: Fixed with path resolution code in entry points

### 2. Missing Dependencies
- **Issue**: Package not found during deployment
- **Solution**: Ensure all dependencies are in `requirements.txt`

### 3. Environment Variables
- **Issue**: Configuration not loaded
- **Solution**: Use Streamlit Cloud's secrets management, not `.env` files

### 4. File Path Issues
- **Issue**: PDF or prompt files not found
- **Solution**: Use relative paths from repository root

## Testing the Deployment

### Local Testing
```bash
# Test imports
python -c "from src.ui.app import main; print('✅ Imports work')"

# Run locally
streamlit run src/ui/app.py
```

### Cloud Testing
1. Deploy to Streamlit Cloud
2. Check logs for any import errors
3. Verify all environment variables are loaded
4. Test chat functionality

## Performance Optimizations

### 1. Caching
- Uses `@st.cache_resource` for expensive operations
- RAG chain is initialized once and cached

### 2. Memory Management
- Batch processing for large documents
- Garbage collection in ingestion pipeline

### 3. Error Handling
- Graceful fallbacks for API failures
- User-friendly error messages

## Monitoring

### Opik Integration
- LLM call tracing and monitoring
- Performance analytics
- Error tracking

### Logs
- Check Streamlit Cloud logs for debugging
- Monitor API usage and costs

## Support

### Common Commands (Local Development)
```bash
make dev     # Run with hot-reload
make test    # Run tests
make clean   # Clean cache
```

### Debugging Tips
1. Check Streamlit Cloud logs first
2. Verify all secrets are set correctly
3. Test imports locally before deploying
4. Monitor API rate limits

## Version History
- v2.0.0: Fixed Streamlit Cloud deployment issues
- v1.0.0: Initial implementation