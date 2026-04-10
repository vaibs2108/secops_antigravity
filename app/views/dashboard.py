import streamlit as st
import pandas as pd
from app.utils.charts import plot_incident_trends, plot_alert_severity, plot_coverage_metrics, plot_compact_metric_card, plot_kpi_progress, plot_threat_heatmap, plot_workflow_velocity

def render_dashboard(kpis: dict, dataset: dict):
    # ── Executive Command Center Banner ──
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); padding: 16px 24px; border-radius: 12px; margin-bottom: 14px; color: white; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #FFF; font-size: 1.15rem; font-family: 'Inter', sans-serif; font-weight: 800;">🛡️ Executive Command Center</h4>
                <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #94A3B8; font-family: 'Inter', sans-serif;">Unified global security posture & autonomous response dashboard</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 8px; backdrop-filter: blur(4px);">
                <span style="font-size: 0.72rem; color: #CBD5E1;">Platform Status</span><br/>
                <span style="font-weight: 700; font-size: 0.88rem; color: #34D399;">● All Systems Operational</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════
    # EXECUTIVE KPIs — Strategic Risk & Resilience
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="margin-bottom: 6px;">
            <span style="font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px;">📊 Executive KPIs — Risk & Resilience</span>
        </div>
    """, unsafe_allow_html=True)

    # Calculate executive-level KPIs from operational data
    asset_cov = round(kpis.get('asset_coverage_pct', 0), 1)
    patch_comp = round(kpis.get('patch_compliance_pct', 0), 1)
    baseline_comp = round(kpis.get('security_baseline_compliance_pct', 0), 1)
    mfa = round(kpis.get('mfa_adoption_pct', 0), 1)
    mttr = round(kpis.get('mean_time_to_respond_hrs', 0), 1)
    mttd = round(kpis.get('mean_time_to_detect_hrs', 0), 1)
    
    # Composite scores
    risk_score = round(100 - ((100 - patch_comp) * 0.3 + (100 - baseline_comp) * 0.3 + (100 - mfa) * 0.2 + (100 - asset_cov) * 0.2), 1)
    resilience_score = round((asset_cov * 0.25 + patch_comp * 0.25 + baseline_comp * 0.25 + mfa * 0.25), 1)
    posture_index = round((baseline_comp * 0.4 + patch_comp * 0.3 + kpis.get('prediction_accuracy_pct', 80) * 0.3), 1)
    maturity_score = min(5.0, max(1.0, round((asset_cov + mfa + kpis.get('prediction_accuracy_pct', 80) + kpis.get('auto_remediation_rate_pct', 60)) / 4 / 20, 1)))
    rosi_pct = int((kpis.get('ai_analyst_time_saved_hrs_week', 120) * 52 * 100 + kpis.get('cost_leakage_identified_month', 45000) * 12) / 150000 * 100)
    
    # Restore threat_readiness for Operational KPIs below
    threat_readiness = round(kpis.get('prediction_accuracy_pct', 0), 1)
    
    ec = st.columns(5, gap="small")
    with ec[0]:
        risk_color = "#34D399" if risk_score >= 80 else "#FBBF24" if risk_score >= 60 else "#F87171"
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-label">Risk Score</p>
            <p class="kpi-value" style="color: {risk_color};">{risk_score}</p>
            <p class="kpi-sub">Composite Risk Posture</p>
        </div>""", unsafe_allow_html=True)
    with ec[1]:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-label">Resilience Index</p>
            <p class="kpi-value" style="color: #60A5FA;">{resilience_score}%</p>
            <p class="kpi-sub">Enterprise Hardening Depth</p>
        </div>""", unsafe_allow_html=True)
    with ec[2]:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-label">Security Posture Index</p>
            <p class="kpi-value" style="color: #A78BFA;">{posture_index}</p>
            <p class="kpi-sub">Predictive & Baseline Avg</p>
        </div>""", unsafe_allow_html=True)
    with ec[3]:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-label">Program Maturity</p>
            <p class="kpi-value" style="color: #F8FAFC;">{maturity_score}<span style="font-size: 0.9rem; color: #64748B;">/5.0</span></p>
            <p class="kpi-sub">CMMI Aligned Score</p>
        </div>""", unsafe_allow_html=True)
    with ec[4]:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-label">ROSI</p>
            <p class="kpi-value" style="color: #34D399;">{rosi_pct}%</p>
            <p class="kpi-sub">Return on SEC Investment</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 36px; margin-bottom: 24px; height: 1px; background: #1E293B; width: 100%;'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════
    # OPERATIONAL KPIs
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="margin-bottom: 6px;">
            <span style="font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px;">⚙️ Operational KPIs</span>
        </div>
    """, unsafe_allow_html=True)

    # TOP ROW
    c = st.columns(5, gap="small")
    with c[0]: plot_compact_metric_card("Asset Coverage", f"{asset_cov}%", "Global Fleet")
    with c[1]: plot_compact_metric_card("Agent Config", f"{round(kpis.get('agent_version_compliance_pct', 0), 1)}%", "Version Ok")
    with c[2]: plot_compact_metric_card("Sec Agent Cov", f"{round(kpis.get('security_agent_coverage_pct', 0), 1)}%", "EDR/XDR")
    with c[3]: plot_compact_metric_card("Major Incidents", f"{kpis.get('major_incident_occurrence', 0)}", "Active Sev 1/2")
    with c[4]: plot_compact_metric_card("Total Alerts", f"{kpis.get('total_alerts', 0):,}", "Generated")

    # BOTTOM ROW
    c = st.columns(5, gap="small")
    with c[0]: plot_compact_metric_card("Baseline Check", f"{baseline_comp}%", "NIST/CIS")
    with c[1]: plot_compact_metric_card("Patch Levels", f"{patch_comp}%", "SLA met")
    with c[2]: plot_compact_metric_card("MFA Adoption", f"{mfa}%", "Enforced")
    with c[3]: plot_compact_metric_card("Prediction Acc", f"{threat_readiness}%", "Behavioral")
    with c[4]: plot_compact_metric_card("PAM JIT", f"{round(kpis.get('pam_usage_pct', 0), 1)}%", "Just-in-Time")

    # ═══════════════════════════════════════════════════════════════
    # CHARTS
    # ═══════════════════════════════════════════════════════════════
    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    col_left, col_mid, col_right = st.columns([1.2, 1, 1], gap="medium")
    with col_left:
        plot_incident_trends(dataset.get('historical_incidents', pd.DataFrame()))
    with col_mid:
        plot_alert_severity(dataset.get('alerts', pd.DataFrame()))
    with col_right:
        plot_coverage_metrics(kpis)

    # BOTTOM ROW — Heatmap + Workflow
    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
    col_heat, col_wf = st.columns([1.5, 1], gap="medium")
    
    wf_data = st.session_state.get('remediation_workflows', {})
    
    with col_heat:
        plot_threat_heatmap(dataset.get('historical_incidents', pd.DataFrame()))

    with col_wf:
        st.markdown("""
            <div style="background: #0B1120; padding: 10px 16px; border-radius: 10px; border-left: 4px solid #3B82F6; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <span style="font-weight: 700; color: #F8FAFC; font-size: 0.9rem;">⚙️ Remediation Workflow</span>
            </div>
        """, unsafe_allow_html=True)
        
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
        
        wc = st.columns(3, gap="small")
        with wc[0]: plot_compact_metric_card("Total", str(total_tickets), "Active")
        with wc[1]: 
            approval_count = len(st.session_state.get('approval_queue', []))
            plot_compact_metric_card("Queue", str(approval_count), "Pending")
        with wc[2]: plot_compact_metric_card("Closed", str(ticket_aggregates['closed']), "Resolved")
        
        plot_workflow_velocity(wf_data)
