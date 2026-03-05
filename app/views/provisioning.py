import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_compliance_donut

def render_provisioning(kpis: dict, dataset: dict):
    st.header("Provisioning (Time to Provision)")
    st.info("🎯 **Domain Objective:** Enable Zero-Touch Provisioning by automating the entire lifecycle of security tools, identities, and infrastructure assets from request through deployment and continuous verification.")
    st.markdown("Automating end-to-end security deployment and identity management.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Enterprise Assets", f"{kpis.get('total_assets', 0):,}")
    with col2:
        plot_compliance_donut(kpis.get('pam_usage_pct', 0), "PAM JIT Usage")
        
    st.markdown("---")
    st.subheader("Interactive GenAI Demos")
    
    domain = "Provisioning (Time to Provision)"
    demos = [
        "End to end Incident Automation (Alert -> Triage -> Ticket)",
        "Self-Service AI Co-pilot for Security tools",
        "Device/Application/Identity provisioning agent"
    ]
    
    for demo in demos:
        render_agent_demo(demo, domain, kpis, dataset)
