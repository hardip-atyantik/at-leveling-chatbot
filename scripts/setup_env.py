#!/usr/bin/env python3
"""Interactive wizard to setup .env file from .env.example"""

import os
import sys
from pathlib import Path

def validate_azure_endpoint(endpoint):
    """Validate Azure OpenAI endpoint format"""
    if not endpoint:
        return False
    return endpoint.startswith("https://") and ".openai.azure.com" in endpoint

def get_user_input(var_name, description, default=None, validator=None):
    """Get input from user with optional validation"""
    prompt = f"\n{description}\n{var_name}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    
    while True:
        value = input(prompt).strip()
        if not value and default:
            value = default
        
        if not value:
            print(f"Error: {var_name} is required.")
            continue
            
        if validator and not validator(value):
            print(f"Error: Invalid format for {var_name}")
            continue
            
        return value

def main():
    """Main wizard function"""
    print("=" * 60)
    print("Environment Configuration Wizard for Atyantik RAG Chatbot")
    print("=" * 60)
    
    # Check if .env already exists
    env_path = Path(".env")
    if env_path.exists():
        response = input("\n.env file already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            sys.exit(0)
    
    print("\nThis wizard will help you set up your environment variables.")
    print("Please have your Azure OpenAI and Qdrant credentials ready.\n")
    
    env_vars = {}
    
    # Azure OpenAI LLM Configuration
    print("\n" + "=" * 40)
    print("AZURE OPENAI LLM CONFIGURATION")
    print("=" * 40)
    
    env_vars['AZURE_OPENAI_ENDPOINT'] = get_user_input(
        "AZURE_OPENAI_ENDPOINT",
        "Enter your Azure OpenAI endpoint URL",
        validator=validate_azure_endpoint
    )
    
    env_vars['AZURE_OPENAI_API_KEY'] = get_user_input(
        "AZURE_OPENAI_API_KEY",
        "Enter your Azure OpenAI API key"
    )
    
    env_vars['AZURE_OPENAI_API_VERSION'] = get_user_input(
        "AZURE_OPENAI_API_VERSION",
        "Enter API version",
        default="2024-08-01-preview"
    )
    
    env_vars['AZURE_OPENAI_DEPLOYMENT_NAME'] = get_user_input(
        "AZURE_OPENAI_DEPLOYMENT_NAME",
        "Enter your GPT deployment name (e.g., gpt-4)"
    )
    
    # Azure OpenAI Embeddings Configuration
    print("\n" + "=" * 40)
    print("AZURE OPENAI EMBEDDINGS CONFIGURATION")
    print("=" * 40)
    
    use_same = input("\nUse same Azure resource for embeddings? (Y/n): ").strip().lower()
    
    if use_same != 'n':
        env_vars['AZURE_OPENAI_EMBEDDINGS_ENDPOINT'] = env_vars['AZURE_OPENAI_ENDPOINT']
        env_vars['AZURE_OPENAI_EMBEDDINGS_API_KEY'] = env_vars['AZURE_OPENAI_API_KEY']
        env_vars['AZURE_OPENAI_EMBEDDINGS_API_VERSION'] = env_vars['AZURE_OPENAI_API_VERSION']
    else:
        env_vars['AZURE_OPENAI_EMBEDDINGS_ENDPOINT'] = get_user_input(
            "AZURE_OPENAI_EMBEDDINGS_ENDPOINT",
            "Enter your Azure OpenAI embeddings endpoint URL",
            validator=validate_azure_endpoint
        )
        
        env_vars['AZURE_OPENAI_EMBEDDINGS_API_KEY'] = get_user_input(
            "AZURE_OPENAI_EMBEDDINGS_API_KEY",
            "Enter your Azure OpenAI embeddings API key"
        )
        
        env_vars['AZURE_OPENAI_EMBEDDINGS_API_VERSION'] = get_user_input(
            "AZURE_OPENAI_EMBEDDINGS_API_VERSION",
            "Enter embeddings API version",
            default="2024-08-01-preview"
        )
    
    env_vars['AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME'] = get_user_input(
        "AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME",
        "Enter your embeddings deployment name (e.g., text-embedding-ada-002)"
    )
    
    # Qdrant Configuration
    print("\n" + "=" * 40)
    print("QDRANT VECTOR DATABASE CONFIGURATION")
    print("=" * 40)
    
    env_vars['QDRANT_URL'] = get_user_input(
        "QDRANT_URL",
        "Enter your Qdrant URL (e.g., https://xyz.qdrant.io or http://localhost:6333)"
    )
    
    env_vars['QDRANT_API_KEY'] = get_user_input(
        "QDRANT_API_KEY",
        "Enter your Qdrant API key (leave empty for local instances)"
    ) or ""
    
    # Opik Configuration (Optional)
    print("\n" + "=" * 40)
    print("OPIK MONITORING CONFIGURATION (Optional)")
    print("=" * 40)
    
    use_opik = input("\nDo you want to configure Opik monitoring? (y/N): ").strip().lower()
    
    if use_opik == 'y':
        env_vars['OPIK_API_KEY'] = get_user_input(
            "OPIK_API_KEY",
            "Enter your Opik API key"
        )
    else:
        env_vars['OPIK_API_KEY'] = ""
    
    # Write to .env file
    print("\n" + "=" * 40)
    print("Writing configuration to .env file...")
    print("=" * 40)
    
    with open(".env", "w") as f:
        f.write("# Azure OpenAI LLM Configuration\n")
        f.write(f"AZURE_OPENAI_API_KEY={env_vars['AZURE_OPENAI_API_KEY']}\n")
        f.write(f"AZURE_OPENAI_ENDPOINT={env_vars['AZURE_OPENAI_ENDPOINT']}\n")
        f.write(f"AZURE_OPENAI_API_VERSION={env_vars['AZURE_OPENAI_API_VERSION']}\n")
        f.write(f"AZURE_OPENAI_DEPLOYMENT_NAME={env_vars['AZURE_OPENAI_DEPLOYMENT_NAME']}\n")
        f.write("\n")
        
        f.write("# Azure OpenAI Embeddings Configuration\n")
        f.write(f"AZURE_OPENAI_EMBEDDINGS_API_KEY={env_vars['AZURE_OPENAI_EMBEDDINGS_API_KEY']}\n")
        f.write(f"AZURE_OPENAI_EMBEDDINGS_ENDPOINT={env_vars['AZURE_OPENAI_EMBEDDINGS_ENDPOINT']}\n")
        f.write(f"AZURE_OPENAI_EMBEDDINGS_API_VERSION={env_vars['AZURE_OPENAI_EMBEDDINGS_API_VERSION']}\n")
        f.write(f"AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME={env_vars['AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME']}\n")
        f.write("\n")
        
        f.write("# Qdrant Vector Database Configuration\n")
        f.write(f"QDRANT_URL={env_vars['QDRANT_URL']}\n")
        f.write(f"QDRANT_API_KEY={env_vars['QDRANT_API_KEY']}\n")
        f.write("\n")
        
        f.write("# Opik Monitoring Configuration (Optional)\n")
        f.write(f"OPIK_API_KEY={env_vars['OPIK_API_KEY']}\n")
    
    print("\n✅ Configuration saved to .env file successfully!")
    print("\nNext steps:")
    print("1. Ensure 'Career Leveling Guide.pdf' is in the project root")
    print("2. Run 'make ingest' to process and upload documents")
    print("3. Run 'make chat' to start the chat interface")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)