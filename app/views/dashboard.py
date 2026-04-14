import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.utils.charts import plot_incident_trends, plot_alert_severity, plot_coverage_metrics, plot_compact_metric_card, plot_kpi_progress, plot_threat_heatmap, plot_workflow_velocity


def _render_gauge(title, value, min_val, max_val, thresholds, suffix="", subtitle="", invert=False):
    """
    Renders a compact Plotly gauge meter with Red/Amber/Green zones.
    
    thresholds: dict with keys 'red_end', 'amber_end' defining boundaries.
    invert: if True, lower values are BETTER (green at bottom, red at top).
    """
    if invert:
        # Lower is better (e.g., False Positive Rate, MTTR)
        bar_color = "#34D399" if value <= thresholds['red_end'] else "#FBBF24" if value <= thresholds['amber_end'] else "#F87171"
        steps = [
            {"range": [min_val, thresholds['red_end']], "color": "rgba(52, 211, 153, 0.15)"},
            {"range": [thresholds['red_end'], thresholds['amber_end']], "color": "rgba(251, 191, 36, 0.15)"},
            {"range": [thresholds['amber_end'], max_val], "color": "rgba(248, 113, 113, 0.15)"},
        ]
    else:
        # Higher is better (e.g., Coverage, Compliance)
        bar_color = "#F87171" if value <= thresholds['red_end'] else "#FBBF24" if value <= thresholds['amber_end'] else "#34D399"
        steps = [
            {"range": [min_val, thresholds['red_end']], "color": "rgba(248, 113, 113, 0.15)"},
            {"range": [thresholds['red_end'], thresholds['amber_end']], "color": "rgba(251, 191, 36, 0.15)"},
            {"range": [thresholds['amber_end'], max_val], "color": "rgba(52, 211, 153, 0.15)"},
        ]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": suffix, "font": {"size": 28, "color": "#F8FAFC", "family": "Inter"}},
        title={"text": f"<b>{title}</b><br><span style='font-size:11px;color:#94A3B8'>{subtitle}</span>", 
               "font": {"size": 13, "color": "#F8FAFC", "family": "Inter"}},
        gauge={
            "axis": {"range": [min_val, max_val], "tickwidth": 1, "tickcolor": "#334155",
                     "tickfont": {"size": 9, "color": "#64748B"}},
            "bar": {"color": bar_color, "thickness": 0.3},
            "bgcolor": "#0F172A",
            "borderwidth": 0,
            "steps": steps,
            "threshold": {
                "line": {"color": "#F8FAFC", "width": 2},
                "thickness": 0.8,
                "value": value
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F8FAFC", "family": "Inter"},
        height=170,
        margin=dict(l=18, r=18, t=50, b=10),
    )
    
    st.plotly_chart(fig, width='stretch', key=f"gauge_{title.replace(' ', '_')}")


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
    # EXECUTIVE KPIs — Strategic Risk & Resilience (Gauge Meters)
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
    posture_index = round((baseline_comp * 0.4 + patch_comp * 0.3 + kpis.get('prediction_accuracy_pct', 50) * 0.3), 1)
    maturity_score = min(5.0, max(1.0, round((asset_cov + mfa + kpis.get('prediction_accuracy_pct', 50) + kpis.get('auto_remediation_rate_pct', 30)) / 4 / 20, 1)))
    
    # ROSI: (savings from automation) / (annual security tooling cost) × 100
    # Annual security tooling cost = total_assets × $150/asset/year (industry benchmark)
    total_assets = kpis.get('total_assets', 10000)
    annual_sec_cost = total_assets * 150  # base cost
    # Savings = analyst time saved + cost leakage identified  
    analyst_saving = kpis.get('ai_analyst_time_saved_hrs_week', 0) * 52 * 75  # $75/hr analyst rate
    leakage_saving = kpis.get('cost_leakage_identified_month', 0) * 12
    rosi_pct = int((analyst_saving + leakage_saving) / max(annual_sec_cost, 1) * 100)
    
    # Restore threat_readiness for Operational KPIs below
    threat_readiness = round(kpis.get('prediction_accuracy_pct', 0), 1)
    
    ec = st.columns(5, gap="small")
    with ec[0]:
        _render_gauge(
            "Risk Score", risk_score, 0, 100,
            {"red_end": 60, "amber_end": 80},
            suffix="", subtitle="Higher = Lower Risk",
        )
    with ec[1]:
        _render_gauge(
            "Resilience Index", resilience_score, 0, 100,
            {"red_end": 60, "amber_end": 80},
            suffix="%", subtitle="Enterprise Hardening",
        )
    with ec[2]:
        _render_gauge(
            "Security Posture", posture_index, 0, 100,
            {"red_end": 60, "amber_end": 80},
            suffix="", subtitle="Baseline + Predictive",
        )
    with ec[3]:
        _render_gauge(
            "Program Maturity", maturity_score, 1.0, 5.0,
            {"red_end": 2.5, "amber_end": 3.5},
            suffix="/5", subtitle="CMMI Aligned",
        )
    with ec[4]:
        _render_gauge(
            "ROSI", rosi_pct, 0, 400,
            {"red_end": 100, "amber_end": 200},
            suffix="%", subtitle="Return on SEC Investment",
        )

    st.markdown("<div style='margin-top: 12px; margin-bottom: 16px; height: 1px; background: #1E293B; width: 100%;'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════
    # OPERATIONAL KPIs — Mapped to All 7 Domains
    # ═══════════════════════════════════════════════════════════════
    st.markdown("""
        <div style="margin-bottom: 6px;">
            <span style="font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px;">⚙️ Operational KPIs — Cross-Domain Coverage</span>
        </div>
    """, unsafe_allow_html=True)

    def _domain_kpi_card(label, value, sub, domain_tag, tag_color):
        """Renders a compact metric card with a colored domain tag."""
        st.markdown(f"""
        <div style="background: #0B1120; padding: 10px 14px; border-radius: 10px; border-left: 3px solid {tag_color}; min-height: 90px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <span style="font-size: 0.72rem; color: #94A3B8; font-weight: 600;">{label}</span>
                <span style="font-size: 0.6rem; background: {tag_color}22; color: {tag_color}; padding: 1px 6px; border-radius: 8px; font-weight: 700; border: 1px solid {tag_color}44;">{domain_tag}</span>
            </div>
            <p style="font-size: 1.3rem; font-weight: 800; color: #F8FAFC; margin: 0; line-height: 1.2;">{value}</p>
            <span style="font-size: 0.65rem; color: #64748B;">{sub}</span>
        </div>
        """, unsafe_allow_html=True)

    # ROW 1 — Zero MI, Zero Touch, Zero Toil, Zero Visibility
    c = st.columns(7, gap="small")
    with c[0]:
        _domain_kpi_card("Major Incidents", f"{kpis.get('major_incident_occurrence', 0)}", "Active Sev 1/2", "Zero MI", "#EF4444")
    with c[1]:
        _domain_kpi_card("MTTR", f"{mttr}h", "Mean Time to Resolve", "Zero MI", "#EF4444")
    with c[2]:
        _domain_kpi_card("Provisioning", f"{kpis.get('provisioning_time_common_tasks_min', 0)}m", "Avg Time to Provision", "Zero Touch", "#8B5CF6")
    with c[3]:
        _domain_kpi_card("Tasks Automated", f"{kpis.get('tasks_automated_per_day', 0):,}", "Per Day", "Zero Toil", "#F59E0B")
    with c[4]:
        _domain_kpi_card("Asset Coverage", f"{asset_cov}%", "EDR/XDR Fleet", "Visibility", "#3B82F6")
    with c[5]:
        _domain_kpi_card("Baseline Compliance", f"{baseline_comp}%", "NIST/CIS", "Compliance", "#10B981")
    with c[6]:
        _domain_kpi_card("False Positive", f"{round(kpis.get('false_positive_rate_pct', 0), 1)}%", "Alert Noise Rate", "Zero FP", "#EC4899")

    # ROW 2 — remaining coverage from each domain
    c2 = st.columns(7, gap="small")
    with c2[0]:
        _domain_kpi_card("MTTD", f"{mttd}h", "Mean Time to Detect", "Zero MI", "#EF4444")
    with c2[1]:
        _domain_kpi_card("MFA Adoption", f"{mfa}%", "Enforced Users", "Zero Touch", "#8B5CF6")
    with c2[2]:
        _domain_kpi_card("Auto-Remediation", f"{round(kpis.get('auto_remediation_rate_pct', 0), 1)}%", "Success Rate", "Zero Toil", "#F59E0B")
    with c2[3]:
        _domain_kpi_card("Shadow IT", f"{kpis.get('shadow_it_discovery_rate_month', 0)}", "Discovered / Month", "Visibility", "#3B82F6")
    with c2[4]:
        _domain_kpi_card("Patch Levels", f"{patch_comp}%", "SLA Compliance", "Compliance", "#10B981")
    with c2[5]:
        _domain_kpi_card("Prediction Acc", f"{threat_readiness}%", "Behavioral ML", "Zero FP", "#EC4899")
    with c2[6]:
        _domain_kpi_card("Tool Coverage", f"{round(kpis.get('orchestration_coverage_pct', 0), 1)}%", "Orchestration", "Intel Ops", "#06B6D4")

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
