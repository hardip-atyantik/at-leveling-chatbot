"""Streamlit chat interface - simplified and optimized"""

import streamlit as st
from functools import lru_cache
import sys
from pathlib import Path

# Add project root to Python path for Streamlit Cloud compatibility
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.config import Config, get_config
from src.core.rag import create_rag_chain
from src.utils.prompts import get_prompts


@st.cache_resource
def initialize():
    """Initialize RAG chain with caching"""
    config = get_config()
    
    # Validate environment
    missing = Config.validate_environment()
    if missing:
        st.error(f"Missing environment variables: {', '.join(missing)}")
        st.stop()
    
    # Get prompts
    system_prompt, user_prompt = get_prompts()
    
    # Create RAG chain
    try:
        chain, _, _, _, opik_tracer = create_rag_chain(system_prompt, user_prompt, config)
        return chain, opik_tracer
    except Exception as e:
        st.error(f"Failed to initialize: {str(e)}")
        st.stop()


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Atyantik Leveling Guide",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Atyantik Leveling Guide")
    st.markdown("Ask me anything about Atyantik Leveling Guide!")
    
    # Initialize chain
    chain, opik_tracer = initialize()
    
    # Session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Atyantik..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display response
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base..."):
                try:
                    response_stream = chain.stream(prompt, config={"callbacks": [opik_tracer]})
                    response = st.write_stream(response_stream)
                except Exception as e:
                    response = f"Error: {str(e)}"
                
                #st.markdown(response)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info("AI assistant trained on Atyantik's knowledge base.")
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()