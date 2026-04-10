import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_asset_distribution

def render_asset_visibility(kpis: dict, dataset: dict):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); padding: 16px 24px; border-radius: 12px; margin-bottom: 14px; color: white; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #FFF; font-size: 1.15rem; font-family: 'Inter', sans-serif; font-weight: 800;">🔍 Asset Visibility & Coverage - March to Zero Visibility Gap</h4>
                <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #94A3B8; font-family: 'Inter', sans-serif;">Eliminate visibility gaps via autonomous discovery & continuous inventory.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Assets Discovered</p><p class="kpi-value">{kpis.get('total_assets', 0):,}</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">EDR Coverage</p><p class="kpi-value">{kpis.get('edr_coverage_pct', 0)}%</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Asset Coverage</p><p class="kpi-value">{round(kpis.get('asset_coverage_pct', 0), 1)}%</p></div>""", unsafe_allow_html=True)
    
    if 'assets' in dataset and not dataset['assets'].empty:
        plot_asset_distribution(dataset['assets'])

    tab1, tab2, tab3 = st.tabs(["🔬 AI Demos", "⚙️ Workflow", "💬 Copilot"])
    
    domain = "Asset Visibility & Coverage"
    demos = [
        "AI-powered continuous asset discovery",
        "Agentic AI to scan address range or cloud accounts non-stop",
        "Context-rich security inventory (ownership, criticality, dependency, config state)",
        "Agentic AI for Shadow IT & Cloud Sprawl"
    ]
    
    with tab1:
        from app.views.shared import render_demo_section
        render_demo_section(demos, domain, kpis, dataset)
    with tab2:
        try:
            from app.utils.workflow_utils import RemediationWorkflow
            RemediationWorkflow.render_remediation_tab(domain)
        except ImportError:
            st.error("Remediation Workflow Engine is currently unavailable.")
    with tab3:
        from app.views.chatbot import render_domain_copilot
        render_domain_copilot(kpis, dataset, domain)
