import streamlit as st
import pandas as pd
from app.agents.manager import AgentManager
import os

def render_chatbot(kpis: dict, dataset: dict):
    st.header("SecOps Copilot: A Day in the Life of Security Operations")
    st.info("🎯 **Domain Objective:** Act as an AI-powered SOC Analyst Copilot. This interface seamlessly pulls live contextual data from a FAISS Vector Database containing mathematically generated ITIL Tickets and Known Error Database (KEDB) resolutions.")
    
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
            )
        else:
            st.warning("KEDB dataset has not been initialized. Please clear cache and rerun.")
            
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
            )
        else:
            st.warning("Tickets dataset has not been initialized. Please clear cache and rerun.")
