.PHONY: help setup env ingest chat clean dev test format lint

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup   - Create virtual environment and install dependencies"
	@echo "  make env     - Interactive wizard to setup .env file"
	@echo "  make ingest  - Run data ingestion pipeline"
	@echo "  make chat    - Start Streamlit chat interface"
	@echo "  make dev     - Run chat in development mode with hot-reload"
	@echo "  make test    - Run tests"
	@echo "  make format  - Format code with black"
	@echo "  make lint    - Check code quality"
	@echo "  make clean   - Clean cache and temporary files"
	@echo "  make help    - Display this help message"

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Activating virtual environment and installing dependencies..."
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "Setup complete! Activate with: source venv/bin/activate"

# Interactive wizard to setup .env file
env:
	@if [ ! -f venv/bin/python ]; then \
		echo "Virtual environment not found. Running setup first..."; \
		make setup; \
	fi
	@echo "Starting environment setup wizard..."
	./venv/bin/python scripts/setup_env.py

# Run data ingestion pipeline
ingest:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Run 'make env' first."; \
		exit 1; \
	fi
	@if [ ! -f "Career Leveling Guide.pdf" ]; then \
		echo "Warning: Career Leveling Guide.pdf not found in project root."; \
		echo "Please add your PDF file before running ingestion."; \
		exit 1; \
	fi
	@echo "Running data ingestion pipeline..."
	PYTHONPATH=. ./venv/bin/python -m src.ingestion.pipeline

# Start Streamlit chat interface
chat:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Run 'make env' first."; \
		exit 1; \
	fi
	@echo "Starting Streamlit chat interface..."
	PYTHONPATH=. ./venv/bin/streamlit run src/ui/app.py

# Development mode with hot-reload
dev:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Run 'make env' first."; \
		exit 1; \
	fi
	@echo "Starting development server with hot-reload..."
	PYTHONPATH=. ./venv/bin/streamlit run src/ui/app.py --server.runOnSave true

# Run tests
test:
	@echo "Running tests..."
	PYTHONPATH=. ./venv/bin/python -m pytest tests/ -v

# Format code
format:
	@echo "Formatting code with black..."
	./venv/bin/black src/ scripts/ --line-length 100

# Lint code
lint:
	@echo "Checking code quality..."
	./venv/bin/pylint src/ --disable=C0114,C0115,C0116

# Clean cache and temporary files
clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	rm -rf .streamlit/cache 2>/dev/null || true
	@echo "Cleanup complete!"