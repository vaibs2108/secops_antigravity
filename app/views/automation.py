import streamlit as st
from app.views.shared import render_agent_demo

def render_automation(kpis: dict, dataset: dict):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); padding: 16px 24px; border-radius: 12px; margin-bottom: 14px; color: white; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #FFF; font-size: 1.15rem; font-family: 'Inter', sans-serif; font-weight: 800;">🤖 Automation Index - March to Zero Toil</h4>
                <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #94A3B8; font-family: 'Inter', sans-serif;">Eliminate operational toil via intelligent analyst co-pilots & hyper-automation.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="kpi-card"><p class="kpi-label">SOC Automation Rate</p><p class="kpi-value">78%</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="kpi-card"><p class="kpi-label">Auto Ticket Closure</p><p class="kpi-value">45%</p></div>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔬 AI Demos", "⚙️ Workflow", "💬 Copilot"])
    
    domain = "Automation Index"
    demos = [
        "AI-powered Security tasks automation (log analysis, routine service requests)",
        "Security Analysts Co-pilot (reporting, rule writing, correlation, script generation)"
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
