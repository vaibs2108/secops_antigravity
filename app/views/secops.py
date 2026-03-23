import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_compliance_donut

def render_secops(kpis: dict, dataset: dict):
    st.markdown(f"""
        <div style="background: #FFFFFF; padding: 10px 20px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid #1E40AF; box-shadow: 0 1px 4px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center;">
            <h4 style="margin: 0; color: #1E293B; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">⚙️ Intelligent IT Security Operations</h4>
            <p style="margin: 0; font-size: 0.85rem; color: #64748B;"><b>Objective:</b> Unified tool ecosystem & autonomous optimization.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Threat Intel IOCs", f"{kpis.get('total_threat_intel_iocs', 0):,}")
    with col2:
        plot_compliance_donut(kpis.get('config_management_coverage_pct', 0), "Config Management")
    from app.views.shared import render_domain_kpi_impact
    render_domain_kpi_impact("Intelligent IT Security Operations")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Interactive GenAI Demos", "Remediation Workflow"])
    
    domain = "Intelligent IT Security Operations"
    demos = [
        "Integrated tool ecosystem with AI orchestration",
        "Threat Intel correlation across tools and actionable intel",
        "AI co-pilot for tool administration (rules, updates, config, license, optimisation)",
        "Autonomous tool maintenance & optimisation (health, patch, signature, capacity)"
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

