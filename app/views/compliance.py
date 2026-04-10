import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_compliance_donut

def render_compliance(kpis: dict, dataset: dict):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); padding: 16px 24px; border-radius: 12px; margin-bottom: 14px; color: white; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #FFF; font-size: 1.15rem; font-family: 'Inter', sans-serif; font-weight: 800;">⚖️ Compliance - March to Zero Non-Compliance · Zero Config · Zero Drift</h4>
                <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #94A3B8; font-family: 'Inter', sans-serif;">Maintain zero drift via autonomous compliance monitoring & self-healing.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Baseline Compliance</p><p class="kpi-value">{round(kpis.get('cis_baseline_compliance_pct', kpis.get('security_baseline_compliance_pct', 78.4)), 1)}%</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Patch Compliance</p><p class="kpi-value">{round(kpis.get('patch_compliance_pct', 0), 1)}%</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Config Mgmt Coverage</p><p class="kpi-value">{round(kpis.get('config_management_coverage_pct', 0), 1)}%</p></div>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔬 AI Demos", "⚙️ Workflow", "💬 Copilot"])
    
    domain = "Continuous Compliance & Governance"
    demos = [
        "AI-powered configuration drift detection / continuous compliance monitoring",
        "Automated configuration drift remediation / self-healing agent",
        "GenAI for Policy Management (Policy as Code)"
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
