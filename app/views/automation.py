import streamlit as st
from app.views.shared import render_agent_demo

def render_automation(kpis: dict, dataset: dict):
    st.header("Automation Index")
    st.info("🎯 **Domain Objective:** Eliminate Operational Toil by deploying intelligent analyst co-pilots that automate routine summarization, reporting, and low-level configuration tasks, freeing security teams for higher-value threat hunting.")
    st.markdown("Streamline routine security operations via intelligent analyst co-pilots.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("SOC Automation Rate (Sim.)", "78%")
    with col2:
        st.metric("Automated Ticket Closure", "45%")
        
    st.markdown("---")
    st.subheader("Interactive GenAI Demos")
    
    domain = "Automation Index"
    demos = [
        "AI-powered Security tasks automation (log analysis, routine service requests)",
        "Security Analysts Co-pilot (reporting, rule writing, correlation, script generation)"
    ]
    
    for demo in demos:
        render_agent_demo(demo, domain, kpis, dataset)

