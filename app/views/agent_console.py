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
        
        agents_list = [
            {
                "Agent Name": "SecOps Triage-01", 
                "Agent Role": "Incident Triage Agent",
                "Primary Domains": "Detection & Response, Major Incidents",
                "Key Capabilities": "Contextualizes incoming alerts, enriches with Threat Intel, drops False Positives."
            },
            {
                "Agent Name": "RCA-Engine-Alpha", 
                "Agent Role": "Root Cause Agent",
                "Primary Domains": "Major Incidents",
                "Key Capabilities": "Reconstructs process trees, maps to MITRE ATT&CK, identifies patient zero."
            },
            {
                "Agent Name": "AutoProv-v2", 
                "Agent Role": "Provisioning Agent",
                "Primary Domains": "Provisioning",
                "Key Capabilities": "Automates Just-In-Time (JIT) access grants, revokes IAM privileges, provisions assets."
            },
            {
                "Agent Name": "Compliance-Scan-D", 
                "Agent Role": "Compliance Agent",
                "Primary Domains": "Compliance",
                "Key Capabilities": "Scans endpoints against CIS/NIST baselines, calculates drift, issues patch tickets."
            },
            {
                "Agent Name": "Continuous-Nmap", 
                "Agent Role": "Asset Discovery Agent",
                "Primary Domains": "Asset Visibility",
                "Key Capabilities": "Performs active/passive subnet scans, updates CMDB, identifies Shadow IT."
            },
            {
                "Agent Name": "Intel-Correlator", 
                "Agent Role": "Threat Intel Agent",
                "Primary Domains": "Security Operations",
                "Key Capabilities": "Ingests global feeds, correlates local log hits against known threat actor infrastructures."
            },
            {
                "Agent Name": "SOAR-Automation", 
                "Agent Role": "Automation Agent",
                "Primary Domains": "Automation",
                "Key Capabilities": "Executes containment playbooks, isolates compromised hosts, updates edge firewalls."
            },
            {
                "Agent Name": "Copilot-Core", 
                "Agent Role": "Security Copilot Agent",
                "Primary Domains": "Global Platform",
                "Key Capabilities": "Conversational interface for querying SecOps data, summarizing KPIs, generating reports."
            }
        ]
        
        # Display as an interactive dataframe
        st.dataframe(pd.DataFrame(agents_list), width="stretch", hide_index=True)
    
    with tab2:
        st.subheader("Agent Execution Ledger")
        
        if not logs:
            st.info("No agents have been deployed yet. Navigate to a Security Domain to trigger an AI simulation.")
        else:
            # Create a dataframe from the logs
            df = pd.DataFrame(logs)
            # Sort by latest
            df = df.sort_values(by="Time", ascending=False)
            st.dataframe(df, width="stretch", hide_index=True)
