import streamlit as st
import pandas as pd
from app.utils.charts import plot_incident_trends, plot_alert_severity, plot_coverage_metrics, plot_compact_metric_card, plot_kpi_progress, plot_threat_heatmap

def render_section_header(title: str, icon: str):
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); padding: 16px 24px; border-radius: 12px; margin: 30px 0 20px 0; box-shadow: 0 10px 20px -5px rgba(30, 64, 175, 0.3); border: 1px solid rgba(255,255,255,0.2);">
            <div style="margin: 0; font-size: 1.25rem; font-weight: 700; font-family: 'Outfit', sans-serif; display: flex; align-items: center; gap: 14px; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                <span style="background: rgba(255,255,255,0.2); backdrop-filter: blur(8px); padding: 8px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.3); line-height: 1; display: flex; align-items: center; justify-content: center;">{icon}</span>
                <span class="dashboard-section-title">{title}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_dashboard(kpis: dict, dataset: dict):
    # Phase 75: Forced contrast fix for section headers
    st.markdown("""
        <style>
        .dashboard-section-title {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("Dashboard: Executive Security Posture")
    
    st.info("🎯 **Domain Objective:** Replace text-heavy reports with an intuitive, executive-level command center providing a 360-degree view of enterprise security health, detection velocity, and overall compliance posture.")
    
    st.markdown("Global view of the synthesized enterprise metrics across all major domains.")
    
    render_section_header("Coverage & Visibility", "🔭")
    plot_kpi_progress("Asset Coverage", kpis.get('asset_coverage_pct', 0), 100.0)
    plot_kpi_progress("Security Agent Coverage", kpis.get('security_agent_coverage_pct', 0), 100.0)
        
    render_section_header("Tool Health & Incident Management", "🛠️")
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_compact_metric_card("Security Tool Uptime", f"{round(kpis.get('security_tool_uptime_pct', 0), 1)}%", "24h Rolling Avg")
    with col2:
        plot_compact_metric_card("Agent Version Compliance", f"{round(kpis.get('agent_version_compliance_pct', 0), 1)}%", "Fleet-wide")
    with col3:
        plot_compact_metric_card("Major Incident Occurrence", f"{kpis.get('major_incident_occurrence', 0)}", "Active Sev 1/2")
        
    render_section_header("Threat Detection & Response", "⚡")
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_compact_metric_card("ATT&CK Detection Coverage", f"{round(kpis.get('attack_detection_coverage_pct', 0), 1)}%")
    with col2:
        plot_compact_metric_card("MTTD", f"{round(kpis.get('mean_time_to_detect_hrs', 0), 1)} hrs", "Mean Time To Detect")
    with col3:
        plot_compact_metric_card("MTTR", f"{round(kpis.get('mean_time_to_respond_hrs', 0), 1)} hrs", "Mean Time To Respond")
        
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_compact_metric_card("False Positive Rate", f"{round(kpis.get('false_positive_rate_pct', 0), 1)}%")
    with col2:
        plot_compact_metric_card("Threat Intel Utilization", f"{round(kpis.get('threat_intelligence_utilization_pct', 0), 1)}%")
    with col3:
        plot_compact_metric_card("Automation Coverage", f"{round(kpis.get('automation_coverage_pct', 0), 1)}%")

    render_section_header("Provisioning & Compliance", "📋")
    col1, col2 = st.columns(2)
    with col1:
        plot_kpi_progress("Security Baseline Compliance", kpis.get('security_baseline_compliance_pct', 0))
    with col2:
        plot_kpi_progress("Patch Compliance", kpis.get('patch_compliance_pct', 0))
        
    render_section_header("Zero Trust Architecture", "🔐")
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_compact_metric_card("MFA Adoption", f"{round(kpis.get('mfa_adoption_pct', 0), 1)}%")
    with col2:
        plot_compact_metric_card("Conditional Access Adoption", f"{round(kpis.get('conditional_access_adoption_pct', 0), 1)}%")
    with col3:
        plot_compact_metric_card("PAM Usage", f"{round(kpis.get('pam_usage_pct', 0), 1)}%")

    render_section_header("Advanced GenAI Telemetry", "🤖")
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_compact_metric_card("AI Prediction Accuracy", f"{round(kpis.get('prediction_accuracy_pct', 0), 1)}%", "Behavioral Engine")
    with col2:
        plot_compact_metric_card("Auto-Remediation Rate", f"{round(kpis.get('auto_remediation_rate_pct', 0), 1)}%", "Autonomous Agents")
    with col3:
        plot_compact_metric_card("Analyst Time Saved", f"{round(kpis.get('ai_analyst_time_saved_hrs_week', 0), 1)} hrs", "Per Week")
        
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_compact_metric_card("Shadow IT Discovered", f"{kpis.get('shadow_it_discovery_rate_month', 0)} apps", "Monthly Rate")
    with col2:
        plot_compact_metric_card("Cost Leakage Identified", f"${kpis.get('cost_leakage_identified_month', 0):,}", "Est. Savings Opportunity")
    with col3:
        plot_compact_metric_card("Signal-to-Noise Ratio", f"{round(kpis.get('signal_to_noise_ratio_pct', 0), 1)}%", "Alert Fidelity")

    render_section_header("Global Metrics Visualized", "📊")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        plot_incident_trends(dataset.get('incidents', pd.DataFrame()))
    with col_v2:
        plot_alert_severity(dataset.get('alerts', pd.DataFrame()))
        
    st.markdown("---")
    plot_threat_heatmap(dataset.get('incidents', pd.DataFrame()))
    
    st.markdown("---")
    plot_coverage_metrics(kpis)
