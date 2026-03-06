import streamlit as st
import pandas as pd
from app.agents.manager import AgentManager
import os

def render_chatbot(kpis: dict, dataset: dict):
    st.header("SecOps Copilot: A Day in the Life of Security Operations")
    st.info("🎯 **Domain Objective:** Act as an AI-powered SOC Analyst Copilot. This interface seamlessly pulls live contextual data from a FAISS Vector Database containing 110 mathematically generated ITIL Tickets and Known Error Database (KEDB) resolutions.")
    
    # Render the RAG Architecture Flow Diagram
    st.markdown("""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 15px; border-radius: 8px; margin-bottom: 25px;">
        <h4 style="color: #1E293B; margin-top: 0; text-align: center;">Retrieval-Augmented Generation (RAG) Architecture</h4>
    """, unsafe_allow_html=True)
    
    mermaid_code = """
    ```mermaid
    graph LR
        subgraph Synthetic Data Factory
            A[50 KEDB Entries]:::data
            B[60 SecOps Tickets]:::data
        end
        
        C[(FAISS Vector Database)]:::db
        D[RAG Context Retrieval]:::rag
        E((SecOps Copilot)):::ai
        F{SOC Analyst}:::user
        
        A -->|langchain_openai Embeddings| C
        B -->|langchain_openai Embeddings| C
        F <-->|Questions & Answers| E
        E -->|Semantic Search| D
        D -.->|Similarity Matches K=4| C
        C -.->|Retrieved Docs| D
        D -->|Augmented Prompt Context| E
        
        classDef data fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#0f172a;
        classDef db fill:#fef08a,stroke:#ca8a04,stroke-width:2px,color:#0f172a;
        classDef rag fill:#cffafe,stroke:#0891b2,stroke-width:2px,color:#0f172a;
        classDef ai fill:#dcfce7,stroke:#16a34a,stroke-width:3px,color:#0f172a;
        classDef user fill:#f1f5f9,stroke:#475569,stroke-width:2px,color:#0f172a;
    ```
    """
    st.markdown(mermaid_code)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Split the view into two columns: Live Data Feed & AI Copilot Chat
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown("### 📥 Live Ingestion Feed")
        st.caption("A sample of the 110 synthesized documents currently hashed into the FAISS Vector Database.")
        
        kedb_df = st.session_state.get('rag_kedb', pd.DataFrame())
        tickets_df = st.session_state.get('rag_tickets', pd.DataFrame())
        
        with st.expander("📚 KEDB Database Sample (Top 5)", expanded=True):
            if not kedb_df.empty:
                for _, row in kedb_df.head(5).iterrows():
                    st.markdown(f"**{row['Tool']}** ({row['Error_Code']})")
                    st.markdown(f"*{row['Issue_Description']}*")
                    st.markdown("---")
            else:
                st.warning("KEDB Data not initialized.")
                
        with st.expander("🎫 SecOps Tickets Sample (Top 5)", expanded=True):
            if not tickets_df.empty:
                for _, row in tickets_df.head(5).iterrows():
                    st.markdown(f"**{row['Ticket_ID']}** - {row['Severity']} ({row['Document_Type']})")
                    st.markdown(f"*{row['Description']}*")
                    st.markdown("---")
            else:
                st.warning("Ticket Data not initialized.")
                
    with col2:
        st.markdown("### 💬 Copilot Interface")
        
        # Initialize chat history
        if "copilot_messages" not in st.session_state:
            st.session_state.copilot_messages = [
                {
                    "role": "assistant", 
                    "content": "Hello! I am your SecOps Copilot. I have just ingested 50 KEDB resolutions and 60 ITIL tickets into my local FAISS memory buffer. How can I help you resolve a security issue today?"
                }
            ]

        # Display chat messages
        for msg in st.session_state.copilot_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # React to user input
        if prompt := st.chat_input("E.g., A CrowdStrike sensor went offline. How do I fix it based on the KEDB?"):
            
            st.chat_message("user").markdown(prompt)
            st.session_state.copilot_messages.append({"role": "user", "content": prompt})

            if not os.getenv("OPENAI_API_KEY"):
                response = "Error: OPENAI_API_KEY is required to contact the FAISS embeddings and LLM."
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.copilot_messages.append({"role": "assistant", "content": response})
                return

            with st.chat_message("assistant"):
                with st.spinner("Querying FAISS Vector Database & synthesizing response..."):
                    
                    # Retrieve context from RAG Engine
                    rag_engine = st.session_state.get("rag_engine")
                    if rag_engine:
                        retrieved_context = rag_engine.retrieve_context(prompt, top_k=4)
                    else:
                        retrieved_context = "ERROR: Vector Engine Offline."
                    
                    with st.expander("🔍 View Retrieved FAISS Context", expanded=False):
                        st.text(retrieved_context)

                    manager = AgentManager()
                    
                    # Overriding the generic context with strictly the retrieved RAG context
                    system_prompt = f"""
                    You are exactly "SecOps Copilot", an AI assistant handling a "Day in the Life of Security Operations."
                    The user is asking you a direct question.
                    You must answer their question utilizing ONLY the following context retrieved from the ITIL FAISS Vector Database.
                    If the answer isn't firmly in the retrieved context, say you don't know based on the KEDB/Tickets.
                    Be extremely concise, professional, and directly state the Ticket IDs or KEDB Error Codes you reference.
                    
                    {retrieved_context}
                    
                    USER QUERY: {prompt}
                    """
                    
                    # We utilize the standard manager.run_agent to generate the LLM text
                    response = manager.run_agent(
                        role="SecOps Copilot", 
                        kpis={}, # Empty KPIs for RAG
                        custom_instruction=system_prompt
                    )
                    
                    st.markdown(response)
                    
            st.session_state.copilot_messages.append({"role": "assistant", "content": response})
