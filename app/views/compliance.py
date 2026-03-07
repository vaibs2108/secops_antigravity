import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_compliance_donut

def render_compliance(kpis: dict, dataset: dict):
    st.header("Compliance")
    st.info("🎯 **Domain Objective:** Maintain a state of Zero Non-Compliance and Zero Configuration Drift by deploying autonomous monitors that detect baseline deviations in real-time and orchestrate self-healing remediation agents.")
    st.markdown("Security baselines, drift detection, and patch management driven by AI.")
    
    col1, col2 = st.columns(2)
    with col1:
        plot_compliance_donut(kpis.get('cis_baseline_compliance_pct', kpis.get('security_baseline_compliance_pct', 78.4)), "Baseline Compliance")
    with col2:
        plot_compliance_donut(kpis.get('patch_compliance_pct', 0), "Patch Compliance")
        
    st.markdown("---")
    st.subheader("Interactive GenAI Demos")
    
    domain = "Compliance"
    demos = [
        "AI powered configuration drift detection/continuous compliance monitoring",
        "Automated configuration drift remediation agent/self-Healing agent",
        "GenAI for Policy Management (e.g. Crafting security policies in a code i.e., PaC)"
    ]
    
    for demo in demos:
        render_agent_demo(demo, domain, kpis, dataset)
