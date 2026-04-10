import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_compliance_donut

def render_provisioning(kpis: dict, dataset: dict):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); padding: 16px 24px; border-radius: 12px; margin-bottom: 14px; color: white; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #FFF; font-size: 1.15rem; font-family: 'Inter', sans-serif; font-weight: 800;">⚡ Time to Provision - March to Zero Touch Provisioning</h4>
                <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #94A3B8; font-family: 'Inter', sans-serif;">Autonomous provisioning for identity & infrastructure with zero human intervention.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Enterprise Assets</p><p class="kpi-value">{kpis.get('total_assets', 0):,}</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">PAM JIT Usage</p><p class="kpi-value">{round(kpis.get('pam_usage_pct', 0), 1)}%</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">MFA Adoption</p><p class="kpi-value">{round(kpis.get('mfa_adoption_pct', 0), 1)}%</p></div>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔬 AI Demos", "⚙️ Workflow", "💬 Copilot"])
    
    domain = "Time to Provision"
    demos = [
        "End-to-end Incident Automation (Alert→Triage→Ticket→Action)",
        "Self-Service AI Co-pilot for Security tools",
        "Device/Application/Identity provisioning agent"
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
