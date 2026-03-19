import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_asset_distribution

def render_asset_visibility(kpis: dict, dataset: dict):
    st.header("Asset Visibility & Coverage")
    st.info("🎯 **Domain Objective:** Eliminate Visibility Gaps by orchestrating autonomous agents to continuously discover, catalog, and risk-score all hardware, cloud, and shadow IT assets across the global enterprise footprint.")
    st.markdown("Continuous discovery, context-rich security inventory, and shadow IT management.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Assets Discovered", f"{kpis.get('total_assets', 0):,}")
    with col2:
        st.metric("EDR Coverage", f"{kpis.get('edr_coverage_pct', 0)}%")
        
    st.markdown("---")
    
    if 'assets' in dataset and not dataset['assets'].empty:
        plot_asset_distribution(dataset['assets'])
        
    st.markdown("---")
    st.subheader("Interactive GenAI Demos")
    
    domain = "Asset Visibility & Coverage"
    demos = [
        "AI-powered continuous asset discovery",
        "Agentic AI to scan address range or cloud accounts non-stop",
        "Context-rich security inventory (ownership, criticality, dependency, config state)",
        "Agentic AI for Shadow IT & Cloud Sprawl"
    ]
    
    for demo in demos:
        render_agent_demo(demo, domain, kpis, dataset)

