import streamlit as st
import pandas as pd
from app.agents.manager import AgentManager
import os

def render_rag_workflow():
    """Renders a premium, executive-level visual depiction of the RAG data flow."""
    st.markdown("""
        <style>
        .rag-pipeline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #FFFFFF;
            padding: 30px;
            border-radius: 16px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 10px 25px rgba(30, 58, 138, 0.05);
            margin-bottom: 30px;
        }
        .pipeline-node {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            flex: 1;
        }
        .node-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            margin-bottom: 12px;
            border: 1px solid #BFDBFE;
            transition: all 0.3s ease;
        }
        .node-icon.active {
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            color: white;
            box-shadow: 0 8px 15px rgba(30, 58, 138, 0.2);
            border: none;
        }
        .node-label {
            font-size: 0.85rem;
            font-weight: 700;
            color: #1E293B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .node-subtext {
            font-size: 0.75rem;
            color: #64748B;
            margin-top: 4px;
        }
        .pipeline-arrow {
            font-size: 24px;
            color: #CBD5E1;
            padding: 0 10px;
            margin-bottom: 30px;
            animation: pulse-arrow 2s infinite;
        }
        @keyframes pulse-arrow {
            0% { transform: translateX(0); opacity: 0.4; }
            50% { transform: translateX(5px); opacity: 1; }
            100% { transform: translateX(0); opacity: 0.4; }
        }
        </style>
        
        <div class="rag-pipeline">
            <div class="pipeline-node">
                <div class="node-icon">📚</div>
                <div class="node-label">KEDB</div>
                <div class="node-subtext">50 Fixes</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="node-icon">🎫</div>
                <div class="node-label">ITIL Tickets</div>
                <div class="node-subtext">60 CR/SR/INC</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="node-icon active">🧠</div>
                <div class="node-label">FAISS Core</div>
                <div class="node-subtext">Vector Store</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="node-icon">🔍</div>
                <div class="node-label">Semantic</div>
                <div class="node-subtext">Retrieval</div>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="node-icon active" style="background: linear-gradient(135deg, #059669 0%, #10B981 100%);">🤖</div>
                <div class="node-label">SecOps AI</div>
                <div class="node-subtext">Copilot</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_chatbot(kpis: dict, dataset: dict):
    st.header("SecOps Copilot: A Day in the Life of Security Operations")
    
    # Render the premium workflow visualization
    render_rag_workflow()
    
    st.info("🎯 **Domain Objective:** Act as an AI-powered SOC Analyst Copilot. This interface uses **Retrieval-Augmented Generation (RAG)** to pull live contextual data from an in-memory FAISS database.")
    
    # Create Tabs for a cleaner Layout
    tab1, tab2, tab3 = st.tabs(["💬 Copilot Chat", "📚 KEDB Database", "🎫 SecOps Tickets"])
    
    kedb_df = st.session_state.get('rag_kedb', pd.DataFrame())
    tickets_df = st.session_state.get('rag_tickets', pd.DataFrame())
    
    with tab1:
        st.markdown("### 🤖 Security Analyst Copilot")
        st.caption("Ask questions about securing the enterprise. The Copilot will automatically query the FAISS memory banks (KEDB & Tickets) in real-time to augment its answers.")
        
        # Initialize chat history
        if "copilot_messages" not in st.session_state:
            st.session_state.copilot_messages = [
                {
                    "role": "assistant", 
                    "content": "Hello! I am your SecOps Copilot. I have analyzed the active Known Error Database and current Incident Tickets. How can I assist with your investigation today?"
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
                with st.spinner("Searching FAISS Index..."):
                    
                    # Retrieve context from RAG Engine
                    rag_engine = st.session_state.get("rag_engine")
                    if rag_engine:
                        retrieved_context = rag_engine.retrieve_context(prompt, top_k=4)
                    else:
                        retrieved_context = "ERROR: Vector Engine Offline."
                    
                    with st.expander("🔍 View Retrieved Knowledge Base Context", expanded=False):
                        st.text(retrieved_context)

                    manager = AgentManager()
                    
                    system_prompt = f"""
                    You are exactly "SecOps Copilot", an AI assistant handling a "Day in the Life of Security Operations."
                    The user is asking you a direct question.
                    You must answer their question utilizing ONLY the following context retrieved from the ITIL FAISS Vector Database.
                    If the answer isn't firmly in the retrieved context, say you don't know based on the KEDB/Tickets.
                    Be extremely concise, professional, and directly state the Ticket IDs or KEDB Error Codes you reference.
                    
                    {retrieved_context}
                    
                    USER QUERY: {prompt}
                    """
                    
                    response = manager.run_agent(
                        role="SecOps Copilot", 
                        kpis={}, 
                        custom_instruction=system_prompt
                    )
                    
                    st.markdown(response)
                    
            st.session_state.copilot_messages.append({"role": "assistant", "content": response})

    with tab2:
        st.markdown("### 📚 Known Error Database (KEDB)")
        st.markdown("This synthetic view represents established operational fixes mapped by Error ID and Tool.")
        if not kedb_df.empty:
            st.dataframe(kedb_df, use_container_width=True, hide_index=True)
            
            # Download capability
            csv = kedb_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download KEDB as CSV",
                data=csv,
                file_name="synthetic_kedb_database.csv",
                mime="text/csv",
                key="dl_kedb"
            )
        else:
            st.warning("KEDB dataset has not been initialized.")
            
    with tab3:
        st.markdown("### 🎫 SecOps Tickets")
        st.markdown("This synthetic feed represents live/historical Service Requests, Incidents, and Change Orders.")
        if not tickets_df.empty:
            st.dataframe(tickets_df, use_container_width=True, hide_index=True)
            
            # Download capability
            csv = tickets_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Tickets as CSV",
                data=csv,
                file_name="synthetic_secops_tickets.csv",
                mime="text/csv",
                key="dl_tickets"
            )
        else:
            st.warning("Tickets dataset has not been initialized.")
