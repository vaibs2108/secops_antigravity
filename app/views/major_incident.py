import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_mttx_bar, plot_incident_trends

def render_major_incident_management(kpis: dict, dataset: dict):
    st.markdown(f"""
        <div style="background: #FFFFFF; padding: 10px 20px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid #1E40AF; box-shadow: 0 1px 4px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center;">
            <h4 style="margin: 0; color: #1E293B; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">🚨 Major Incidents (MI)</h4>
            <p style="margin: 0; font-size: 0.85rem; color: #64748B;"><b>Objective:</b> Minimize business disruption via predictive AI & autonomous response.</p>
        </div>
    """, unsafe_allow_html=True)

    
    # Domain specific context
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Major Incidents", f"{kpis.get('major_incident_occurrence', 0)}")
    with col2:
        st.metric("Mean Time to Resolve", f"{kpis.get('mean_time_to_respond_hrs', 0):.1f} hrs")
    
    col_a, col_b = st.columns([1, 1])
    with col_a:
        plot_mttx_bar(kpis.get('mean_time_to_detect_hrs', 0), kpis.get('mean_time_to_respond_hrs', 0))
    with col_b:
        if 'historical_incidents' in dataset and not dataset['historical_incidents'].empty:
            plot_incident_trends(dataset['historical_incidents'])
            
    st.markdown("---")
    from app.views.shared import render_domain_kpi_impact
    render_domain_kpi_impact("Major Incidents (MI)")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Interactive GenAI Demos", "Remediation Workflow"])
    
    domain = "Major Incidents (MI)"
    demos = [
        "AI-driven Anomaly Detection & Predictive Analytics",
        "Self-healing and auto-remediation agentic workflow",
        "GenAI for Scenario Simulation",
        "GenAI-based Smart Knowledge Assist",
        "Root Cause Analysis Assistant & Agent",
        "Continuous Monitoring Agents (Health/Security/Configuration /Anomaly Detection)"
    ]
    
    with tab1:
        st.subheader("Interactive GenAI Demos")
        for demo in demos:
            render_agent_demo(demo, domain, kpis, dataset)
            
    with tab2:
        try:
            from app.utils.workflow_utils import RemediationWorkflow
            RemediationWorkflow.render_remediation_tab(domain)
        except ImportError:
            st.error("Remediation Workflow Engine is currently unavailable.")

