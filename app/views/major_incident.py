import streamlit as st
import pandas as pd
import numpy as np
import time
from app.views.shared import render_agent_demo, render_demo_tile, get_demo_record, render_domain_kpi_impact
from app.utils.charts import plot_mttx_bar, plot_incident_trends

def render_recurring_rca(dataset: dict, kpis: dict):
    """Renders the Recurring Incident Root Cause Analysis panel."""
    incidents_df = dataset.get('historical_incidents', pd.DataFrame())
    assets_df = dataset.get('assets', pd.DataFrame())
    
    if incidents_df.empty or 'asset_id' not in incidents_df.columns:
        st.info("Incident data does not contain asset correlation. Regenerate the dataset to enable Recurring RCA.")
        return
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); padding: 16px 24px; border-radius: 12px; margin-bottom: 14px; color: white; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div>
                <h4 style="margin: 0; color: #FFF; font-size: 1.15rem; font-family: 'Inter', sans-serif; font-weight: 800;">🔁 Recurring Incident Root Cause Analysis</h4>
                <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #94A3B8; font-family: 'Inter', sans-serif;">AI-driven detection of assets with recurring incidents — identify systemic issues before they become major outages.</p>
            </div>
            <div style="background: rgba(255,255,255,0.15); padding: 8px 14px; border-radius: 8px; backdrop-filter: blur(4px);">
                <span style="font-size: 0.75rem; color: #DBEAFE;">Powered by</span><br/>
                <span style="font-weight: 700; font-size: 0.9rem;">RootCause-v2 Agent</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Step 1: Auto-detect recurring assets ---
    asset_incident_counts = incidents_df.groupby('asset_id').agg(
        incident_count=('incident_id', 'count'),
        root_causes=('root_cause_category', lambda x: list(x.unique())),
        dominant_root_cause=('root_cause_category', lambda x: x.value_counts().index[0]),
        severities=('severity', lambda x: list(x)),
        services=('affected_service', lambda x: list(x.unique())),
        avg_mttr=('time_to_resolve_hrs', 'mean'),
        first_incident=('timestamp', 'min'),
        last_incident=('timestamp', 'max')
    ).reset_index()
    
    recurring_assets = asset_incident_counts[asset_incident_counts['incident_count'] >= 2].sort_values('incident_count', ascending=False)
    
    # --- Summary Metrics ---
    total_recurring_assets = len(recurring_assets)
    total_recurring_incidents = recurring_assets['incident_count'].sum()
    avg_repeat_count = recurring_assets['incident_count'].mean() if total_recurring_assets > 0 else 0
    top_root_cause = recurring_assets['dominant_root_cause'].value_counts().index[0] if total_recurring_assets > 0 else "N/A"
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card"><p class="kpi-label">Repeat-Offender Assets</p><p class="kpi-value">{total_recurring_assets}</p></div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card"><p class="kpi-label">Recurring Incidents</p><p class="kpi-value">{total_recurring_incidents}</p></div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card"><p class="kpi-label">Avg Repeats/Asset</p><p class="kpi-value">{avg_repeat_count:.1f}</p></div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card"><p class="kpi-label">#1 Root Cause</p><p class="kpi-value" style="font-size: 1rem;">{top_root_cause}</p></div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    if total_recurring_assets > 0:
        st.markdown("##### 🔴 Top Repeat-Offender Assets")
        display_df = recurring_assets.head(15).copy()
        if not assets_df.empty and 'asset_id' in assets_df.columns:
            display_df = display_df.merge(
                assets_df[['asset_id', 'hostname', 'ip_address', 'os', 'criticality']],
                on='asset_id', how='left'
            )
        
        display_df['root_causes_str'] = display_df['root_causes'].apply(lambda x: ', '.join(x[:3]))
        display_df['services_str'] = display_df['services'].apply(lambda x: ', '.join(x[:2]))
        display_df['avg_mttr'] = display_df['avg_mttr'].round(1)
        display_df['crit_high_pct'] = display_df['severities'].apply(
            lambda x: f"{(sum(1 for s in x if s in ('Critical', 'High')) / len(x) * 100):.0f}%"
        )
        
        show_cols = ['asset_id', 'incident_count', 'dominant_root_cause', 'avg_mttr', 'crit_high_pct', 'services_str']
        col_names = {'asset_id': 'Asset ID', 'incident_count': '# Incidents', 'dominant_root_cause': 'Primary Root Cause',
                     'avg_mttr': 'Avg MTTR (hrs)', 'crit_high_pct': 'Crit/High %', 'services_str': 'Affected Services'}
        if 'hostname' in display_df.columns:
            show_cols.insert(1, 'hostname')
            col_names['hostname'] = 'Hostname'
        if 'ip_address' in display_df.columns:
            show_cols.insert(2, 'ip_address')
            col_names['ip_address'] = 'IP Address'
        
        st.dataframe(display_df[show_cols].rename(columns=col_names), hide_index=True, width='stretch')
        
        # Root Cause Distribution
        st.markdown("##### 📊 Root Cause Pattern Distribution")
        rc_dist = recurring_assets.explode('root_causes')['root_causes'].value_counts().head(10)
        rc_rows = ""
        max_count = rc_dist.max() if len(rc_dist) > 0 else 1
        for cause, count in rc_dist.items():
            bar_width = int((count / max_count) * 100)
            rc_rows += f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                <span style="min-width: 260px; font-size: 0.82rem; color: #1E293B;">{cause}</span>
                <div style="flex: 1; background: #F1F5F9; border-radius: 4px; height: 22px; overflow: hidden;">
                    <div style="width: {bar_width}%; background: linear-gradient(90deg, #1E3A8A, #3B82F6); height: 100%; border-radius: 4px; display: flex; align-items: center; justify-content: flex-end; padding-right: 6px;">
                        <span style="font-size: 0.72rem; color: white; font-weight: 700;">{count}</span>
                    </div>
                </div>
            </div>"""
        st.markdown(f"""<div style="background: #FFFFFF; padding: 14px; border-radius: 10px; border: 1px solid #E2E8F0;">{rc_rows}</div>""", unsafe_allow_html=True)
        
        # Per-Asset timeline
        st.markdown("")
        st.markdown("##### 🔍 Per-Asset Incident Timeline")
        for _, row in display_df.head(5).iterrows():
            asset_id = row['asset_id']
            hostname = row.get('hostname', asset_id)
            ip = row.get('ip_address', 'N/A')
            count = row['incident_count']
            dom_rc = row['dominant_root_cause']
            asset_incidents = incidents_df[incidents_df['asset_id'] == asset_id].sort_values('timestamp')
            
            with st.expander(f"🖥️ **{hostname}** ({ip}) — {count} incidents | Primary Cause: _{dom_rc}_", expanded=False):
                st.dataframe(
                    asset_incidents[['incident_id', 'timestamp', 'severity', 'root_cause_category', 'affected_service', 'status', 'time_to_resolve_hrs']].rename(columns={
                        'incident_id': 'Incident', 'timestamp': 'When', 'severity': 'Severity',
                        'root_cause_category': 'Root Cause', 'affected_service': 'Service',
                        'status': 'Status', 'time_to_resolve_hrs': 'MTTR (hrs)'
                    }),
                    hide_index=True, width='stretch'
                )
                cause_counts = asset_incidents['root_cause_category'].value_counts()
                top_cause = cause_counts.index[0]
                top_cause_pct = (cause_counts.iloc[0] / count) * 100
                if top_cause_pct > 50:
                    st.error(f"⚠️ **Systemic Pattern Detected:** {top_cause_pct:.0f}% of incidents on this asset are caused by **\"{top_cause}\"**.")
                else:
                    st.warning(f"🔶 **Multi-Factor Recurrence:** Diverse root causes ({len(cause_counts)} unique). Top: \"{top_cause}\" ({top_cause_pct:.0f}%).")
        
        # LLM Deep Analysis
        st.markdown("---")
        st.markdown("##### 🧠 AI-Powered Per-Asset ITIL v4 RCA Reports")
        st.caption("Generates an individual Root Cause Analysis report for each repeat-offender asset following the full ITIL v4 Problem Management framework.")
        import os
        
        rca_key = "rca_reports_generated"
        if rca_key not in st.session_state:
            st.session_state[rca_key] = {}
        
        if st.button("🚀 Generate AI Root Cause Reports (Per Asset)", key="btn_recurring_rca", type="primary"):
            if not os.getenv("OPENAI_API_KEY"):
                st.error("Error: OPENAI_API_KEY is not set.")
                return
            from app.agents.manager import AgentManager
            manager = AgentManager()
            top5 = display_df.head(5)
            
            progress_bar = st.progress(0, text="Initializing RCA pipeline...")
            reports = {}
            
            for idx, (_, r) in enumerate(top5.iterrows()):
                asset_id = r['asset_id']
                hostname = r.get('hostname', asset_id)
                ip = r.get('ip_address', 'N/A')
                count = r['incident_count']
                dom_rc = r['dominant_root_cause']
                avg_mttr_val = r['avg_mttr']
                services = r.get('services_str', 'N/A')
                
                asset_incidents_slice = incidents_df[incidents_df['asset_id'] == asset_id].sort_values('timestamp').head(15)
                incident_csv = asset_incidents_slice[['incident_id', 'timestamp', 'severity', 'root_cause_category', 'affected_service', 'status', 'time_to_resolve_hrs']].to_csv(index=False)
                
                progress_bar.progress((idx) / 5, text=f"🧠 Analyzing Asset {idx+1}/5: {hostname} ({ip})...")
                
                prompt = f"""ITIL v4 ROOT CAUSE ANALYSIS — INDIVIDUAL ASSET REPORT

You are analyzing a SPECIFIC repeat-offender asset. Generate a COMPLETE, STANDALONE ITIL v4 RCA report for this single asset.

═══════════════════════════════════════════════
ASSET UNDER INVESTIGATION:
  - Hostname: {hostname}
  - IP Address: {ip}
  - Asset ID: {asset_id}
  - Total Recurring Incidents: {count}
  - Dominant Root Cause: {dom_rc}
  - Average MTTR: {avg_mttr_val:.1f} hours
  - Affected Services: {services}
═══════════════════════════════════════════════

FULL INCIDENT HISTORY FOR THIS ASSET:
```csv
{incident_csv}
```

FLEET CONTEXT (for comparison):
- Total repeat-offender assets across enterprise: {total_recurring_assets}
- Total recurring incidents fleet-wide: {total_recurring_incidents}
- Fleet-wide #1 root cause: {top_root_cause}

YOUR OUTPUT MUST EXACTLY FOLLOW THIS ITIL v4 RCA FORMAT:

## 1. Issue Description
- What is happening on this specific asset?
- Frequency and pattern of incidents (cite dates from the CSV)
- Which services are affected and what symptoms are observed?

## 2. Timeline of Events
- Build a chronological timeline from the incident timestamps in the CSV
- Show: First incident → pattern escalation → most recent incident
- Identify any clustering, periodicity, or acceleration in frequency

## 3. Impact Assessment
- **Business Impact**: SLA breach risk, customer-facing disruption potential
- **Operational Impact**: Analyst hours consumed by this single asset, MTTR of {avg_mttr_val:.1f}h vs target
- **System Impact**: Service availability degradation for {services}

## 4. RCA Methodology — 5 Whys Analysis
Perform a detailed 5 Whys analysis specifically for this asset:
- **Why 1**: Why did the incidents occur? (cite the dominant root cause: {dom_rc})
- **Why 2**: Why did {dom_rc} happen on this asset?
- **Why 3**: Why was that underlying condition present?
- **Why 4**: Why wasn't it detected or prevented earlier?
- **Why 5**: What systemic gap allowed this to persist through {count} incidents?

## 5. Problem Investigation & Root Cause
- The definitive root cause for THIS asset (not generic)
- Contributing factors: People / Process / Technology
- Cite specific incident IDs and timestamps from the CSV as evidence
- How does this asset's pattern compare to the fleet-wide #{top_root_cause} trend?

## 6. Action Items & Remediation Plan
Provide a table with columns: Action | Owner Role | Priority (P1-P4) | Target Timeline | Change Ref
- Include both immediate workaround AND permanent fix
- Each action must be specific to this asset's root cause
- Link each permanent fix to the ITIL Change Enablement process

## 7. Known Error Database (KEDB) Entry
Generate a formal KEDB record:
| Field | Value |
|-------|-------|
| Error ID | KE-2026-{1001 + idx:04d} |
| Asset | {hostname} ({ip}) |
| Error Summary | (one-line description of the recurring issue) |
| Root Cause | (reference to Section 5) |
| Workaround | (interim fix) |
| Permanent Fix | (reference to Section 6) |
| Status | Open |

## 8. Lessons Learned & Preventive Measures
- What monitoring or process gap allowed {count} incidents before detection?
- What preventive control should be implemented?
- Continual Service Improvement (CSI) recommendation for this asset class

Format your entire response in professional, well-structured markdown."""

                with st.status(f"🧠 **Analyzing {hostname} ({ip})...**", expanded=True) as ai_status:
                    st.write(f"📊 Loading {count} incident records...")
                    time.sleep(0.5)
                    st.write(f"🔍 Applying 5 Whys analysis for root cause: {dom_rc}...")
                    time.sleep(0.5)
                    response = manager.run_agent("Root Cause Analysis", kpis, prompt)
                    ai_status.update(label=f"✅ **RCA Complete — {hostname}**", state="complete", expanded=False)
                
                reports[f"{hostname} ({ip})"] = response
                progress_bar.progress((idx + 1) / 5, text=f"✅ Completed {idx+1}/5 asset reports")
            
            st.session_state[rca_key] = reports
            progress_bar.progress(1.0, text="✅ All 5 per-asset ITIL RCA reports generated!")
        
        # Display reports in expandable sections
        if st.session_state[rca_key]:
            st.markdown("---")
            st.markdown("##### 📋 Individual Asset RCA Reports")
            for asset_label, report_content in st.session_state[rca_key].items():
                with st.expander(f"📄 **ITIL RCA Report — {asset_label}**", expanded=False):
                    st.markdown(report_content)
    else:
        st.success("✅ No recurring incident patterns detected.")


def render_major_incident_management(kpis: dict, dataset: dict):
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); padding: 16px 24px; border-radius: 12px; margin-bottom: 14px; color: white; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #FFF; font-size: 1.15rem; font-family: 'Inter', sans-serif; font-weight: 800;">🎯 Major Incidents (MI) - March to Zero MI</h4>
                <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #94A3B8; font-family: 'Inter', sans-serif;">Minimize business disruption via predictive AI & autonomous response.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Current Major Incidents</p><p class="kpi-value">{kpis.get('major_incident_occurrence', 0)}</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Mean Time to Resolve</p><p class="kpi-value">{kpis.get('mean_time_to_respond_hrs', 0):.1f}h</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">MTTD</p><p class="kpi-value">{kpis.get('mean_time_to_detect_hrs', 0):.1f}h</p></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card"><p class="kpi-label">Total Incidents</p><p class="kpi-value">{len(dataset.get('historical_incidents', []))}</p></div>""", unsafe_allow_html=True)
    
    # Charts row
    col_a, col_b = st.columns(2)
    with col_a:
        plot_mttx_bar(kpis.get('mean_time_to_detect_hrs', 0), kpis.get('mean_time_to_respond_hrs', 0))
    with col_b:
        if 'historical_incidents' in dataset and not dataset['historical_incidents'].empty:
            plot_incident_trends(dataset['historical_incidents'])

    # Sub-tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔬 AI Demos", "🔁 Recurring RCA", "⚙️ Workflow", "💬 Copilot"])
    
    domain = "Major Incidents (MI)"
    demos = [
        "AI-driven Anomaly Detection & Predictive Analytics",
        "Self-healing and auto-remediation agentic workflow",
        "GenAI for Scenario Simulation",
        "GenAI-based Smart Knowledge Assist",
        "Root Cause Analysis Assistant & Agent",
        "Continuous Monitoring Agents (Health/Security/Configuration/Anomaly detection)"
    ]
    
    with tab1:
        from app.views.shared import render_demo_section
        render_demo_section(demos, domain, kpis, dataset)
            
    with tab2:
        render_recurring_rca(dataset, kpis)
            
    with tab3:
        try:
            from app.utils.workflow_utils import RemediationWorkflow
            RemediationWorkflow.render_remediation_tab(domain)
        except ImportError:
            st.error("Remediation Workflow Engine is currently unavailable.")
    
    with tab4:
        from app.views.chatbot import render_domain_copilot
        render_domain_copilot(kpis, dataset, domain)
