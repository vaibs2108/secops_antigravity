import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_mttx_bar, plot_incident_trends

def render_major_incident_management(kpis: dict, dataset: dict):
    st.header("Major Incidents (MI)")
    st.info("🎯 **Domain Objective:** Minimize business disruption by leveraging autonomous agents to predict anomalies before they escalate, automate root cause analysis, and orchestrate self-healing remediation workflows.")
    st.markdown("AI-powered capabilities for triage, predictive analytics, and self-healing response.")
    
    # Domain specific context
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Major Incidents", f"{kpis.get('major_incident_occurrence', 0)}")
    with col2:
        st.metric("Mean Time to Resolve", f"{kpis.get('mean_time_to_respond_hrs', 0):.1f} hrs")
        
    st.markdown("---")
    
    col_a, col_b = st.columns([1, 1])
    with col_a:
        plot_mttx_bar(kpis.get('mean_time_to_detect_hrs', 0), kpis.get('mean_time_to_respond_hrs', 0))
    with col_b:
        if 'incidents' in dataset and not dataset['incidents'].empty:
            plot_incident_trends(dataset['incidents'])
            
    st.markdown("---")
    st.subheader("Interactive GenAI Demos")
    
    domain = "Major Incidents (MI)"
    demos = [
        "AI-driven Anomaly Detection & Predictive Analytics",
        "Self-healing and auto-remediation agentic workflow",
        "GenAI for Scenario Simulation",
        "GenAI-based Smart Knowledge Assist",
        "Root Cause Analysis Assistant & Agent",
        "Continuous Monitoring Agents (Health/Security/Configuration /Anomaly Detection)"
    ]
    
    for demo in demos:
        render_agent_demo(demo, domain, kpis, dataset)

