import streamlit as st
import pandas as pd
from datetime import datetime

def render_agent_console(kpis: dict, dataset: dict):
    st.header("Agents View")
    st.info("🎯 **Domain Objective:** Provide complete transparency into the platform's autonomous workforce by cataloging specialized AI personas and tracking their real-time execution across the enterprise.")
    st.markdown("Monitor the autonomous AI agents currently deployed and executing tasks across the enterprise environment.")
    
    # Initialize logs if they don't exist
    if 'agent_logs' not in st.session_state:
        st.session_state.agent_logs = []
        
    logs = st.session_state.agent_logs
    
    tab1, tab2 = st.tabs(["Agent Directory & Capabilities", "Real-Time Execution Ledger"])
    
    with tab1:
        st.subheader("Configured Autonomous Agents")
        st.markdown("This directory lists all active AI personas operating within the SecOps Demonstration Platform.")
        
        from app.views.shared import load_demo_requirements
        import re
        
        records = load_demo_requirements()
        agent_dict = {}
        
        for r in records:
            domain = str(r.get('Category', str(r.get('Unnamed: 1', 'Unknown Domain'))))
            agents_str = str(r.get('Agents Involved', str(r.get('Unnamed: 9', ''))))
            goal = str(r.get('Goal of Demo', str(r.get('Unnamed: 3', ''))))
            
            # Split agents by comma and clean up
            agent_names = [a.strip() for a in agents_str.split(',') if a.strip()]
            for name in agent_names:
                # Remove markdown asterisks if any
                clean_name = name.replace('*', '').strip()
                if clean_name and clean_name.lower() != "none" and "No dedicated agent" not in clean_name:
                    if clean_name not in agent_dict:
                        agent_dict[clean_name] = {
                            "Agent Name": clean_name,
                            "Agent Role": f"{clean_name.replace(' Agent', '')} Specialist",
                            "Primary Domains": set(),
                            "Key Capabilities": set(),
                            "Under-the-Hood Tasks": set()
                        }
                    agent_dict[clean_name]["Primary Domains"].add(domain)
                    if goal:
                        agent_dict[clean_name]["Key Capabilities"].add(goal)
                        
                    # Inject explicit traceability tasks for directory clarity
                    if "Kill Switch" in clean_name or "Containment" in clean_name:
                        agent_dict[clean_name]["Under-the-Hood Tasks"].add("Generates emergency isolation playbooks; Broadcasts API halt commands to affected subnets.")
                    elif "Triage" in clean_name or "Investigation" in clean_name or "Discovery" in clean_name:
                        agent_dict[clean_name]["Under-the-Hood Tasks"].add("Correlates cross-platform IOCs; Analyzes entity behavior dynamically.")
                    elif "Provision" in clean_name or "IaC" in clean_name or "Config" in clean_name or "Policy" in clean_name:
                        agent_dict[clean_name]["Under-the-Hood Tasks"].add("Synthesizes strict-compliance configurations; Maps runtime drift.")
                    elif "Self Heal" in clean_name or "Heal" in clean_name:
                        agent_dict[clean_name]["Under-the-Hood Tasks"].add("Safely patches baseline deviations; Restores service health autonomously.")
                    elif "Red Team" in clean_name or "Simulator" in clean_name:
                        agent_dict[clean_name]["Under-the-Hood Tasks"].add("Simulates adversarial MITRE techniques against corporate defenses.")
                    else:
                        agent_dict[clean_name]["Under-the-Hood Tasks"].add("Executes specialized domain tasks; Validates constraints.")
        
        # Convert sets back to strings for display
        agents_list = []
        for v in agent_dict.values():
            v["Primary Domains"] = ", ".join(sorted(list(v["Primary Domains"])))
            caps = list(v["Key Capabilities"])
            v["Key Capabilities"] = " • ".join(caps[:3]) + ("..." if len(caps) > 3 else "")
            tasks = list(v["Under-the-Hood Tasks"])
            v["Under-the-Hood Tasks"] = " • ".join(tasks[:2])
            agents_list.append(v)
            
        # Ensure we have a default Copilot
        agents_list.append({
            "Agent Name": "Copilot-Core", 
            "Agent Role": "Security Copilot Agent",
            "Primary Domains": "Global Platform",
            "Key Capabilities": "Conversational interface for querying SecOps data.",
            "Under-the-Hood Tasks": "Generates final confidence scoring and executive reporting."
        })
        
        # Display as an interactive dataframe
        st.dataframe(pd.DataFrame(agents_list), width='stretch', hide_index=True)
    
    with tab2:
        st.subheader("Agent Execution Ledger")
        
        if not logs:
            st.info("No agents have been deployed yet. Navigate to a Security Domain to trigger an AI simulation.")
        else:
            # Create a dataframe from the logs
            df = pd.DataFrame(logs)
            # Sort by latest
            df = df.sort_values(by="Time", ascending=False)
            st.dataframe(df, width='stretch', hide_index=True)

