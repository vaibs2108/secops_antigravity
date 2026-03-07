import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_compliance_donut

def render_secops(kpis: dict, dataset: dict):
    st.header("Intelligent IT Security Operations")
    st.info("🎯 **Domain Objective:** Achieve Intelligent Security Operations by orchestrating a unified tool ecosystem where AI agents manage routine maintenance, correlate cross-platform intelligence, and optimize tool configurations autonomously.")
    st.markdown("Ecosystem tool integration, threat intel correlation, and autonomous tool optimization.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Threat Intel IOCs", f"{kpis.get('total_threat_intel_iocs', 0):,}")
    with col2:
        plot_compliance_donut(kpis.get('config_management_coverage_pct', 0), "Config Management Coverage")
        
    st.markdown("---")
    st.subheader("Interactive GenAI Demos")
    
    domain = "Security Operations"
    demos = [
        "Integrated tool ecosystem with AI orchestration",
        "Threat Intel correlation across tools and actionable intel",
        "AI co-pilot for tool administration (Health monitoring, rules management, updates, config, license utilization, rules optimization)",
        "Autonomous tool maintenance & optimization (Health monitoring, upkeep, patch mgmt, signature mgmt, capacity management)"
    ]
    
    for demo in demos:
        render_agent_demo(demo, domain, kpis, dataset)
