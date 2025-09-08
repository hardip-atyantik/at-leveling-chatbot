"""Core RAG chain logic shared across the application"""

import os
from typing import Tuple, Optional
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance
from opik.integrations.langchain import OpikTracer

from .config import Config, get_config, handle_errors


@handle_errors("Failed to initialize embeddings")
def create_embeddings(config: Config = None) -> AzureOpenAIEmbeddings:
    """Create Azure OpenAI embeddings instance"""
    config = config or get_config()
    return AzureOpenAIEmbeddings(
        api_key=os.getenv('AZURE_OPENAI_EMBEDDINGS_API_KEY'),
        azure_endpoint=os.getenv('AZURE_OPENAI_EMBEDDINGS_ENDPOINT'),
        api_version=os.getenv('AZURE_OPENAI_EMBEDDINGS_API_VERSION'),
        azure_deployment=os.getenv('AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME'),
        chunk_size=config.embedding_batch_size
    )


@handle_errors("Failed to connect to Qdrant")
def create_qdrant_client() -> QdrantClient:
    """Create Qdrant client instance"""
    return QdrantClient(
        url=os.getenv('QDRANT_URL'),
        api_key=os.getenv('QDRANT_API_KEY')
    )


@handle_errors("Failed to initialize vector store")
def create_vector_store(
    client: Optional[QdrantClient] = None,
    embeddings: Optional[AzureOpenAIEmbeddings] = None,
    config: Config = None
) -> QdrantVectorStore:
    """Create or get vector store instance"""
    config = config or get_config()
    client = client or create_qdrant_client()
    embeddings = embeddings or create_embeddings(config)
    
    return QdrantVectorStore(
        client=client,
        collection_name=config.collection_name,
        embedding=embeddings
    )


def create_or_verify_collection(
    client: QdrantClient,
    config: Config,
    embedding_dim: int = 1536
) -> bool:
    """Create or verify Qdrant collection exists"""
    try:
        client.create_collection(
            on_disk_payload=True,
            collection_name=config.collection_name,
            vectors_config=models.VectorParams(
                size=embedding_dim,
                distance=Distance.COSINE
            ),
            quantization_config=models.BinaryQuantization(
                binary=models.BinaryQuantizationConfig(always_ram=False)
            )
        )
        return True
    except Exception as e:
        if "already exists" in str(e).lower():
            return True
        raise


@handle_errors("Failed to create RAG chain")
def create_rag_chain(
    system_prompt: str,
    user_prompt: str,
    config: Config = None
) -> Tuple:
    """Create complete RAG chain with all components"""
    config = config or get_config()
    
    # Initialize components
    embeddings = create_embeddings(config)
    client = create_qdrant_client()
    vectorstore = create_vector_store(client, embeddings, config)
    
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": config.mmr_k}
    )
    
    # Create prompt template
    prompt_template = ChatPromptTemplate(
        messages=[
            ("system", system_prompt),
            ("user", user_prompt)
        ]
    )
    
    # Initialize LLM and tracer
    opik_tracer = OpikTracer()
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
        max_tokens=None,
        streaming=True,
        callbacks=[opik_tracer]
    )
    
    # Build chain
    chain = (
        {"context": retriever, "query": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )
    
    return chain, vectorstore, client, embeddings, opik_tracer