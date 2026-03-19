import streamlit as st
from app.views.shared import render_agent_demo
from app.utils.charts import plot_alert_severity

def render_detection_response(kpis: dict, dataset: dict):
    st.header("Efficiency in Detection & Response")
    st.info("🎯 **Domain Objective:** Reach a state of Zero False Positives by employing GenAI triage agents that correlate alerts with deep environmental context, reducing analyst fatigue and accelerating high-fidelity incident investigations.")
    st.markdown("Efficient alert triaging, contextual enrichment, and false positive reduction.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Generated Alerts", f"{kpis.get('total_alerts', 0):,}")
    with col2:
        st.metric("SOC False Positive Rate", f"{kpis.get('false_positive_rate_pct', 0)}%")
        
    st.markdown("---")
    
    if 'alerts' in dataset and not dataset['alerts'].empty:
        plot_alert_severity(dataset['alerts'])
        
    st.markdown("---")
    st.subheader("Interactive GenAI Demos")
    
    domain = "Efficiency in Detection & Response"
    demos = [
        "AI-enabled alert triaging and enrichment with context",
        "False positive reduction agent",
        "AI-guided detection and response",
        "AI powered response playbooks"
    ]
    
    for demo in demos:
        render_agent_demo(demo, domain, kpis, dataset)

