"""Simplified document ingestion pipeline"""

import os
import gc
import time
from pathlib import Path
from multiprocessing import Pool, cpu_count
from functools import partial
from tqdm import tqdm

from langchain_community.document_loaders import PyPDFium2Loader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.core.config import Config, get_config, handle_errors
from src.core.rag import create_embeddings, create_qdrant_client, create_vector_store, create_or_verify_collection


def load_pdf_pages(pdf_path: str, start_page: int = None, end_page: int = None):
    """Load specific pages from PDF"""
    loader = PyPDFium2Loader(pdf_path)
    documents = loader.load()
    
    if start_page is not None and end_page is not None:
        return documents[start_page:end_page]
    return documents


@handle_errors("Failed to process PDF")
def load_pdf(pdf_path: str, config: Config = None):
    """Load PDF with multiprocessing optimization"""
    config = config or get_config()
    
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    # For small PDFs, load directly
    loader = PyPDFium2Loader(pdf_path)
    temp_docs = loader.load()
    total_pages = len(temp_docs)
    
    if total_pages <= config.max_processes:
        return temp_docs
    
    # For large PDFs, use multiprocessing
    print(f"Processing {total_pages} pages with {config.max_processes} processes...")
    pages_per_process = total_pages // config.max_processes
    page_ranges = [
        (i * pages_per_process, 
         (i + 1) * pages_per_process if i < config.max_processes - 1 else total_pages)
        for i in range(config.max_processes)
    ]
    
    load_func = partial(load_pdf_pages, pdf_path)
    with Pool(config.max_processes) as pool:
        results = pool.starmap(load_func, page_ranges)
    
    # Combine results
    all_documents = []
    for doc_batch in results:
        all_documents.extend(doc_batch)
    return all_documents


def split_documents(documents, config: Config = None):
    """Split documents into chunks"""
    config = config or get_config()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap
    )
    return splitter.split_documents(documents)


def upload_in_batches(vectorstore, documents, batch_size: int = 2):
    """Upload documents to vector store in batches"""
    total_docs = len(documents)
    successful = 0
    failed = 0
    
    print(f"📤 Uploading {total_docs} documents in batches of {batch_size}...")
    
    for i in tqdm(range(0, total_docs, batch_size), desc="Uploading"):
        batch = documents[i:i + batch_size]
        
        try:
            vectorstore.add_documents(batch)
            successful += len(batch)
            gc.collect()  # Memory cleanup
            time.sleep(0.1)  # Rate limiting
        except Exception as e:
            failed += len(batch)
            print(f"\n⚠️ Failed batch {i//batch_size + 1}: {str(e)}")
            
            # Retry once
            try:
                time.sleep(0.5)
                vectorstore.add_documents(batch)
                successful += len(batch)
                failed -= len(batch)
            except:
                pass
    
    print(f"\n✅ Uploaded: {successful}/{total_docs}")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    
    return failed == 0


@handle_errors("Ingestion failed")
def ingest_documents(pdf_path: str = None, config: Config = None):
    """Main ingestion pipeline - simplified entry point"""
    config = config or get_config()
    pdf_path = pdf_path or config.pdf_path
    
    # Validate environment
    missing_vars = Config.validate_environment()
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
    
    print("🔍 Starting document ingestion...")
    
    # Load and process PDF
    print(f"📄 Loading PDF: {pdf_path}")
    documents = load_pdf(pdf_path, config)
    print(f"✅ Loaded {len(documents)} pages")
    
    # Split into chunks
    print("✂️ Splitting documents...")
    chunks = split_documents(documents, config)
    print(f"✅ Created {len(chunks)} chunks")
    
    # Initialize vector store
    print("🔗 Connecting to vector database...")
    embeddings = create_embeddings(config)
    client = create_qdrant_client()
    
    # Test embedding dimension
    test_dim = len(embeddings.embed_query('test'))
    
    # Create/verify collection
    create_or_verify_collection(client, config, test_dim)
    
    # Get vector store
    vectorstore = create_vector_store(client, embeddings, config)
    
    # Upload documents
    start_time = time.time()
    success = upload_in_batches(vectorstore, chunks, config.batch_size)
    
    # Report results
    elapsed = time.time() - start_time
    print(f"\n📈 Processing complete in {elapsed:.1f}s")
    print(f"⚡ Average: {elapsed/len(chunks):.3f}s per chunk")
    
    return success


if __name__ == "__main__":
    # Direct execution
    try:
        success = ingest_documents()
        if success:
            print("🎉 Ingestion completed successfully!")
        else:
            print("⚠️ Ingestion completed with some errors")
            exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
        exit(1)
    except Exception as e:
        print(f"💥 Fatal error: {str(e)}")
        exit(1)