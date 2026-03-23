import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_asset_distribution

def render_asset_visibility(kpis: dict, dataset: dict):
    st.markdown(f"""
        <div style="background: #FFFFFF; padding: 10px 20px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid #1E40AF; box-shadow: 0 1px 4px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center;">
            <h4 style="margin: 0; color: #1E293B; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">🔍 Asset Visibility & Coverage</h4>
            <p style="margin: 0; font-size: 0.85rem; color: #64748B;"><b>Objective:</b> Eliminate visibility gaps via autonomous discovery.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Assets Discovered", f"{kpis.get('total_assets', 0):,}")
    with col2:
        st.metric("EDR Coverage", f"{kpis.get('edr_coverage_pct', 0)}%")
    
    if 'assets' in dataset and not dataset['assets'].empty:
        plot_asset_distribution(dataset['assets'])
    from app.views.shared import render_domain_kpi_impact
    render_domain_kpi_impact("Asset Visibility & Coverage")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Interactive GenAI Demos", "Remediation Workflow"])
    
    domain = "Asset Visibility & Coverage"
    demos = [
        "AI-powered continuous asset discovery",
        "Agentic AI to scan address range or cloud accounts non-stop",
        "Context-rich security inventory (ownership, criticality, dependency, config state)",
        "Agentic AI for Shadow IT & Cloud Sprawl"
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

