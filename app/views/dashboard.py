import streamlit as st
import pandas as pd
from app.utils.charts import plot_incident_trends, plot_alert_severity, plot_coverage_metrics, plot_compact_metric_card, plot_kpi_progress, plot_threat_heatmap, plot_workflow_velocity

def render_section_header(title: str, icon: str):
    """Clean, light-themed section header with left accent border."""
    st.markdown(f"""
        <div style="background: #FFFFFF; padding: 14px 22px; border-radius: 12px; margin: 20px 0 14px 0; border-left: 4px solid #2563EB; box-shadow: 0 1px 4px rgba(0,0,0,0.04); display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 1.2em; line-height: 1;">{icon}</span>
            <span style="color: #1E293B; font-size: 1rem; font-weight: 700; font-family: 'Outfit', sans-serif; letter-spacing: -0.01em;">{title}</span>
        </div>
    """, unsafe_allow_html=True)

def render_dashboard(kpis: dict, dataset: dict):
    # ── Executive Command Center Banner ──
    st.markdown("""
        <div style="background: #FFFFFF; padding: 14px 24px; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #2563EB; box-shadow: 0 1px 4px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #1E293B; font-size: 1.1rem; font-family: 'Outfit', sans-serif; font-weight: 700;">🛡️ Executive Command Center</h4>
                <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #94A3B8; font-family: 'Outfit', sans-serif;">Unified global security posture & autonomous response</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ── TOP KPI ROW (5 cards) ──
    st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
    c = st.columns(5, gap="medium")
    with c[0]: plot_compact_metric_card("Asset Coverage", f"{round(kpis.get('asset_coverage_pct', 0), 1)}%", "Global Fleet")
    with c[1]: plot_compact_metric_card("Agent Config", f"{round(kpis.get('agent_version_compliance_pct', 0), 1)}%", "Version Ok")
    with c[2]: plot_compact_metric_card("MTTR", f"{round(kpis.get('mean_time_to_respond_hrs', 0), 1)}h", "Time to Respond")
    with c[3]: plot_compact_metric_card("Sec Agent Cov", f"{round(kpis.get('security_agent_coverage_pct', 0), 1)}%", "EDR/XDR")
    with c[4]: plot_compact_metric_card("Major Incidents", f"{kpis.get('major_incident_occurrence', 0)}", "Active Sev 1/2")

    # ── BOTTOM KPI ROW (5 cards) ──
    c = st.columns(5, gap="medium")
    with c[0]: plot_compact_metric_card("Baseline Check", f"{round(kpis.get('security_baseline_compliance_pct', 0), 1)}%", "NIST/CIS")
    with c[1]: plot_compact_metric_card("Patch Levels", f"{round(kpis.get('patch_compliance_pct', 0), 1)}%", "SLA met")
    with c[2]: plot_compact_metric_card("MFA Adoption", f"{round(kpis.get('mfa_adoption_pct', 0), 1)}%", "Enforced")
    with c[3]: plot_compact_metric_card("Prediction Acc", f"{round(kpis.get('prediction_accuracy_pct', 0), 1)}%", "Behavioral")
    with c[4]: plot_compact_metric_card("Leakage Saved", f"${kpis.get('cost_leakage_identified_month', 0):,}", "Cost Savings")

    # ── CHARTS ROW — 3 column layout like reference ──
    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    col_left, col_mid, col_right = st.columns([1.2, 1, 1], gap="medium")
    with col_left:
        plot_incident_trends(dataset.get('historical_incidents', pd.DataFrame()))
    with col_mid:
        plot_alert_severity(dataset.get('alerts', pd.DataFrame()))
    with col_right:
        plot_coverage_metrics(kpis)

    # ── BOTTOM ROW — Heatmap + Workflow ──
    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
    col_heat, col_wf = st.columns([1.5, 1], gap="medium")
    
    wf_data = st.session_state.get('remediation_workflows', {})
    
    with col_heat:
        plot_threat_heatmap(dataset.get('historical_incidents', pd.DataFrame()))

    with col_wf:
        # ── Workflow Console metrics ──
        render_section_header("Remediation Workflow", "⚙️")
        
        ticket_aggregates = {'identified': 0, 'approved': 0, 'implemented': 0, 'verified': 0, 'closed': 0}
        total_tickets = 0
        
        if isinstance(wf_data, dict):
            for category_tickets in wf_data.values():
                if isinstance(category_tickets, list):
                    for t in category_tickets:
                        total_tickets += 1
                        stage = t.get('workflow_stage', 'identified').lower()
                        if stage in ticket_aggregates:
                            ticket_aggregates[stage] += 1
                        elif stage == 'draft':
                            ticket_aggregates['identified'] += 1
        
        # Compact 3-col workflow metrics
        wc = st.columns(3, gap="small")
        with wc[0]: plot_compact_metric_card("Total", str(total_tickets), "Active")
        with wc[1]: 
            approval_count = len(st.session_state.get('approval_queue', []))
            plot_compact_metric_card("Queue", str(approval_count), "Pending")
        with wc[2]: plot_compact_metric_card("Closed", str(ticket_aggregates['closed']), "Resolved")
        
        # Workflow velocity chart
        plot_workflow_velocity(wf_data)
