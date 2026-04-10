import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_alert_severity

def render_detection_response(kpis: dict, dataset: dict):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); padding: 16px 24px; border-radius: 12px; margin-bottom: 14px; color: white; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #FFF; font-size: 1.15rem; font-family: 'Inter', sans-serif; font-weight: 800;">🛡️ Efficiency in Detection & Response - March to Zero False Positive</h4>
                <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #94A3B8; font-family: 'Inter', sans-serif;">Reach zero false positives via GenAI triage & intelligent detection.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Total Alerts</p><p class="kpi-value">{kpis.get('total_alerts', 0):,}</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">False Positive Rate</p><p class="kpi-value">{kpis.get('false_positive_rate_pct', 0)}%</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Prediction Accuracy</p><p class="kpi-value">{round(kpis.get('prediction_accuracy_pct', 0), 1)}%</p></div>""", unsafe_allow_html=True)
    
    if 'alerts' in dataset and not dataset['alerts'].empty:
        plot_alert_severity(dataset['alerts'])

    tab1, tab2, tab3 = st.tabs(["🔬 AI Demos", "⚙️ Workflow", "💬 Copilot"])
    
    domain = "Efficiency in Detection & Response"
    demos = [
        "AI-enabled alert triaging and enrichment with context",
        "False positive reduction agent",
        "AI-guided detection and response",
        "AI-powered response playbooks"
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
