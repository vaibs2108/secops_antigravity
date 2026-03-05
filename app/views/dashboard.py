import streamlit as st
import pandas as pd
from app.utils.charts import plot_incident_trends, plot_alert_severity, plot_coverage_metrics, plot_compact_metric_card, plot_kpi_progress, plot_threat_heatmap

def render_dashboard(kpis: dict, dataset: dict):
    st.header("Dashboard: Executive Security Posture")
    
    st.info("🎯 **Domain Objective:** Replace text-heavy reports with an intuitive, executive-level command center providing a 360-degree view of enterprise security health, detection velocity, and overall compliance posture.")
    
    st.markdown("Global view of the synthesized enterprise metrics across all major domains.")
    
    st.markdown("### Coverage & Visibility")
    plot_kpi_progress("Asset Coverage", kpis.get('asset_coverage_pct', 0), 100.0)
    plot_kpi_progress("Security Agent Coverage", kpis.get('security_agent_coverage_pct', 0), 100.0)
        
    st.markdown("<br>### Tool Health & Incident Management", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_compact_metric_card("Security Tool Uptime", f"{kpis.get('security_tool_uptime_pct', 0)}%", "24h Rolling Avg")
    with col2:
        plot_compact_metric_card("Agent Version Compliance", f"{kpis.get('agent_version_compliance_pct', 0)}%", "Fleet-wide")
    with col3:
        plot_compact_metric_card("Major Incident Occurrence", f"{kpis.get('major_incident_occurrence', 0)}", "Active Sev 1/2")
        
    st.markdown("<br>### Threat Detection & Response", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_compact_metric_card("ATT&CK Detection Coverage", f"{kpis.get('attack_detection_coverage_pct', 0)}%")
    with col2:
        plot_compact_metric_card("MTTD", f"{kpis.get('mean_time_to_detect_hrs', 0):.1f} hrs", "Mean Time To Detect")
    with col3:
        plot_compact_metric_card("MTTR", f"{kpis.get('mean_time_to_respond_hrs', 0):.1f} hrs", "Mean Time To Respond")
        
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_compact_metric_card("False Positive Rate", f"{kpis.get('false_positive_rate_pct', 0)}%")
    with col2:
        plot_compact_metric_card("Threat Intel Utilization", f"{kpis.get('threat_intelligence_utilization_pct', 0)}%")
    with col3:
        plot_compact_metric_card("Automation Coverage", f"{kpis.get('automation_coverage_pct', 0)}%")

    st.markdown("<br>### Provisioning & Compliance", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        plot_kpi_progress("Security Baseline Compliance", kpis.get('security_baseline_compliance_pct', 0))
    with col2:
        plot_kpi_progress("Patch Compliance", kpis.get('patch_compliance_pct', 0))
        
    st.markdown("<br>### Zero Trust Architecture", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_compact_metric_card("MFA Adoption", f"{kpis.get('mfa_adoption_pct', 0)}%")
    with col2:
        plot_compact_metric_card("Conditional Access Adoption", f"{kpis.get('conditional_access_adoption_pct', 0)}%")
    with col3:
        plot_compact_metric_card("PAM Usage", f"{kpis.get('pam_usage_pct', 0)}%")

    st.markdown("---")
    st.markdown("### Global Metrics Visualized")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        plot_incident_trends(dataset.get('incidents', pd.DataFrame()))
    with col_v2:
        plot_alert_severity(dataset.get('alerts', pd.DataFrame()))
        
    st.markdown("---")
    plot_threat_heatmap(dataset.get('incidents', pd.DataFrame()))
    
    st.markdown("---")
    plot_coverage_metrics(kpis)
