"""Setup configuration for RAG Chatbot package"""
from setuptools import setup, find_packages

setup(
    name="atyantik-rag-chatbot",
    version="2.0.0",
    description="RAG Chatbot system for Atyantik Technologies",
    author="Atyantik Technologies",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies will be read from requirements.txt
        "streamlit>=1.49.1",
        "langchain>=0.3.27",
        "qdrant-client>=1.15.1",
        "python-dotenv",
        "pypdfium2>=4.30.0",
        "opik>=1.8.42",
    ],
    package_data={
        "prompts": ["*.txt"],
    },
    include_package_data=True,
)