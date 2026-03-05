import streamlit as st
from app.agents.manager import AgentManager
import os

def render_chatbot(kpis: dict, dataset: dict):
    st.header("Platform Copilot")
    st.info("🎯 **Domain Objective:** Empower users with a conversational AI interface to query the live dataset, interpret complex security KPIs, and receive guided explanations of the platform's simulated findings.")
    st.markdown("💬 Ask questions about the SecOps platform, the simulated KPIs, or the generated dataset.")
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add a greeting message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! I am the platform copilot. I have full context of the current KPIs and the synthetic dataset. How can I help you understand this demonstration platform today?"
        })

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("E.g., How is the False Positive Rate calculated in this demo?"):
        
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        if not os.getenv("OPENAI_API_KEY"):
            response = "Error: OPENAI_API_KEY is not set. Please add it to your environment."
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            return

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                manager = AgentManager()
                
                # We inject the full app state (KPIs and Dataset summaries) into the system prompt for the QA bot
                dataset_summaries = {}
                for key, df in dataset.items():
                    dataset_summaries[key] = f"{len(df)} records covering columns: {list(df.columns)}"
                    
                kpis_str = str(kpis).replace("{", "{{").replace("}", "}}")
                dataset_summaries_str = str(dataset_summaries).replace("{", "{{").replace("}", "}}")
                prompt_str = str(prompt).replace("{", "{{").replace("}", "}}")
                    
                context = f"""
                You are a helpful Copilot for a GenAI Security Operations Demonstration Platform.
                Your job is to answer the user's questions specifically about this platform, the KPIs it is showing, or the synthetic datasets it generates.
                
                CURRENT PLATFORM STATE:
                KPIs: {kpis_str}
                
                SYNTHETIC DATASETS AVAILABLE:
                {dataset_summaries_str}
                
                USER QUERY: {prompt_str}
                
                Answer clearly, concisely, and act as an expert guide to this specific platform's capabilities.
                """
                
                response = manager.run_agent(
                    role="Documentation Expert", 
                    kpis=kpis, 
                    custom_instruction=context
                )
                
                st.markdown(response)
                
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
