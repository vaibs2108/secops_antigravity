import streamlit as st
import pandas as pd
import numpy as np
from app.views.shared import render_agent_demo
from app.utils.charts import plot_mttx_bar, plot_incident_trends

def render_recurring_rca(dataset: dict, kpis: dict):
    """Renders the Recurring Incident Root Cause Analysis panel."""
    incidents_df = dataset.get('historical_incidents', pd.DataFrame())
    assets_df = dataset.get('assets', pd.DataFrame())
    
    if incidents_df.empty or 'asset_id' not in incidents_df.columns:
        st.info("Incident data does not contain asset correlation. Regenerate the dataset to enable Recurring RCA.")
        return
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); padding: 14px 20px; border-radius: 10px; margin-bottom: 12px; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; font-size: 1.05rem; color: #FFF;">🔁 Recurring Incident Root Cause Analysis</h4>
                <p style="margin: 4px 0 0; font-size: 0.82rem; color: #DBEAFE;">AI-driven detection of assets with recurring incidents — identify systemic issues before they become major outages.</p>
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
    
    # Only assets with 2+ incidents are "recurring"
    recurring_assets = asset_incident_counts[asset_incident_counts['incident_count'] >= 2].sort_values('incident_count', ascending=False)
    
    # --- Summary Metrics ---
    total_recurring_assets = len(recurring_assets)
    total_recurring_incidents = recurring_assets['incident_count'].sum()
    avg_repeat_count = recurring_assets['incident_count'].mean() if total_recurring_assets > 0 else 0
    top_root_cause = recurring_assets['dominant_root_cause'].value_counts().index[0] if total_recurring_assets > 0 else "N/A"
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div style="background: #FFFFFF; padding: 12px; border-radius: 10px; border-left: 4px solid #DC2626; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <p style="margin: 0; font-size: 0.75rem; color: #64748B; text-transform: uppercase;">Repeat-Offender Assets</p>
            <p style="margin: 4px 0 0; font-size: 1.6rem; font-weight: 800; color: #DC2626;">{total_recurring_assets}</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="background: #FFFFFF; padding: 12px; border-radius: 10px; border-left: 4px solid #F59E0B; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <p style="margin: 0; font-size: 0.75rem; color: #64748B; text-transform: uppercase;">Recurring Incidents</p>
            <p style="margin: 4px 0 0; font-size: 1.6rem; font-weight: 800; color: #F59E0B;">{total_recurring_incidents}</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div style="background: #FFFFFF; padding: 12px; border-radius: 10px; border-left: 4px solid #1E3A8A; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <p style="margin: 0; font-size: 0.75rem; color: #64748B; text-transform: uppercase;">Avg Repeats/Asset</p>
            <p style="margin: 4px 0 0; font-size: 1.6rem; font-weight: 800; color: #1E3A8A;">{avg_repeat_count:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div style="background: #FFFFFF; padding: 12px; border-radius: 10px; border-left: 4px solid #059669; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <p style="margin: 0; font-size: 0.75rem; color: #64748B; text-transform: uppercase;">#1 Root Cause Pattern</p>
            <p style="margin: 4px 0 0; font-size: 1.0rem; font-weight: 800; color: #059669;">{top_root_cause}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # --- Step 2: Top Repeat-Offender Assets Grid ---
    if total_recurring_assets > 0:
        st.markdown("##### 🔴 Top Repeat-Offender Assets")
        
        # Enrich with asset details
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
        
        # Select display columns
        show_cols = ['asset_id', 'incident_count', 'dominant_root_cause', 'avg_mttr', 'crit_high_pct', 'services_str']
        col_names = {'asset_id': 'Asset ID', 'incident_count': '# Incidents', 'dominant_root_cause': 'Primary Root Cause',
                     'avg_mttr': 'Avg MTTR (hrs)', 'crit_high_pct': 'Crit/High %', 'services_str': 'Affected Services'}
        if 'hostname' in display_df.columns:
            show_cols.insert(1, 'hostname')
            col_names['hostname'] = 'Hostname'
        if 'ip_address' in display_df.columns:
            show_cols.insert(2, 'ip_address')
            col_names['ip_address'] = 'IP Address'
        
        st.dataframe(
            display_df[show_cols].rename(columns=col_names),
            width=None, hide_index=True, use_container_width=True
        )
        
        # --- Step 3: Root Cause Distribution ---
        st.markdown("##### 📊 Root Cause Pattern Distribution (Across Recurring Assets)")
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
        
        st.markdown(f"""<div style="background: #FFFFFF; padding: 14px; border-radius: 10px; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">{rc_rows}</div>""", unsafe_allow_html=True)
        
        st.markdown("")
        
        # --- Step 4: Deep Dive per Asset (Expandable) ---
        st.markdown("##### 🔍 Per-Asset Incident Timeline & Analysis")
        
        for _, row in display_df.head(5).iterrows():
            asset_id = row['asset_id']
            hostname = row.get('hostname', asset_id)
            ip = row.get('ip_address', 'N/A')
            count = row['incident_count']
            dom_rc = row['dominant_root_cause']
            
            # Get all incidents for this asset
            asset_incidents = incidents_df[incidents_df['asset_id'] == asset_id].sort_values('timestamp')
            
            with st.expander(f"🖥️ **{hostname}** ({ip}) — {count} incidents | Primary Cause: _{dom_rc}_", expanded=False):
                st.dataframe(
                    asset_incidents[['incident_id', 'timestamp', 'severity', 'root_cause_category', 'affected_service', 'status', 'time_to_resolve_hrs']].rename(columns={
                        'incident_id': 'Incident', 'timestamp': 'When', 'severity': 'Severity',
                        'root_cause_category': 'Root Cause', 'affected_service': 'Service',
                        'status': 'Status', 'time_to_resolve_hrs': 'MTTR (hrs)'
                    }),
                    hide_index=True, use_container_width=True
                )
                
                # Pattern insight
                cause_counts = asset_incidents['root_cause_category'].value_counts()
                top_cause = cause_counts.index[0]
                top_cause_pct = (cause_counts.iloc[0] / count) * 100
                
                if top_cause_pct > 50:
                    st.error(f"⚠️ **Systemic Pattern Detected:** {top_cause_pct:.0f}% of incidents on this asset are caused by **\"{top_cause}\"**. This indicates a persistent, unresolved structural issue requiring permanent remediation.")
                else:
                    st.warning(f"🔶 **Multi-Factor Recurrence:** This asset exhibits diverse root causes ({len(cause_counts)} unique). Top: \"{top_cause}\" ({top_cause_pct:.0f}%). A holistic review is recommended.")
        
        # --- Step 5: LLM-Powered Deep Analysis ---
        st.markdown("---")
        st.markdown("##### 🧠 AI-Powered Recurring RCA Analysis")
        
        import os
        if st.button("🚀 Generate AI Root Cause Correlation Report", key="btn_recurring_rca", type="primary"):
            if not os.getenv("OPENAI_API_KEY"):
                st.error("Error: OPENAI_API_KEY is not set.")
                return
            
            from app.agents.manager import AgentManager
            manager = AgentManager()
            
            # Build a focused context slice
            top5 = display_df.head(5)
            context_data = ""
            for _, r in top5.iterrows():
                asset_incidents_slice = incidents_df[incidents_df['asset_id'] == r['asset_id']].head(10)
                context_data += f"\n--- ASSET: {r.get('hostname', r['asset_id'])} ({r.get('ip_address', 'N/A')}) | {r['incident_count']} incidents ---\n"
                context_data += asset_incidents_slice[['incident_id', 'timestamp', 'severity', 'root_cause_category', 'affected_service', 'time_to_resolve_hrs']].to_csv(index=False)
            
            prompt = f"""RECURRING INCIDENT PATTERN ANALYSIS REQUEST:

Analyze the following assets that have REPEATED incidents and identify the systemic root causes.

TOP 5 REPEAT-OFFENDER ASSETS WITH THEIR INCIDENT HISTORY:
{context_data}

AGGREGATE STATISTICS:
- Total repeat-offender assets: {total_recurring_assets}
- Total recurring incidents: {total_recurring_incidents}
- #1 root cause pattern across all: {top_root_cause}

YOUR OUTPUT MUST INCLUDE:
1. **Executive Summary**: 2-3 sentences on the overall recurring incident health
2. **Per-Asset Root Cause Correlation**: For each of the top 5 assets, explain WHY incidents keep recurring (reference specific root cause categories and their frequency). Identify if it is a single systemic issue or multi-factor
3. **Cross-Asset Pattern Analysis**: Are there common root causes across multiple assets? Does this indicate a broader infrastructure/process weakness?
4. **Recommended Permanent Fixes**: For each top asset, provide a SPECIFIC remediation (not generic advice) - e.g. "Implement certificate auto-renewal via cert-manager to eliminate Certificate Expiration recurrence"
5. **Risk Projection**: If left unaddressed, estimate the impact over the next 30 days based on current recurrence rates

Format your response in markdown with clear headers."""

            with st.status("🧠 **RootCause-v2 Agent analyzing recurring patterns...**", expanded=True) as ai_status:
                st.write("Correlating incident history across hot assets...")
                import time
                time.sleep(1.5)
                st.write("Identifying systemic root cause patterns...")
                time.sleep(1.0)
                
                response = manager.run_agent("Root Cause Analysis", kpis, prompt)
                ai_status.update(label="✅ **Recurring RCA Analysis Complete**", state="complete", expanded=False)
            
            st.markdown(response)
    else:
        st.success("✅ No recurring incident patterns detected. All assets have unique incident profiles.")


def render_major_incident_management(kpis: dict, dataset: dict):
    st.markdown(f"""
        <div style="background: #FFFFFF; padding: 10px 20px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid #1E40AF; box-shadow: 0 1px 4px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center;">
            <h4 style="margin: 0; color: #1E293B; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">🚨 Major Incidents (MI)</h4>
            <p style="margin: 0; font-size: 0.85rem; color: #64748B;"><b>Objective:</b> Minimize business disruption via predictive AI & autonomous response.</p>
        </div>
    """, unsafe_allow_html=True)

    
    # Domain specific context
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Major Incidents", f"{kpis.get('major_incident_occurrence', 0)}")
    with col2:
        st.metric("Mean Time to Resolve", f"{kpis.get('mean_time_to_respond_hrs', 0):.1f} hrs")
    
    col_a, col_b = st.columns([1, 1])
    with col_a:
        plot_mttx_bar(kpis.get('mean_time_to_detect_hrs', 0), kpis.get('mean_time_to_respond_hrs', 0))
    with col_b:
        if 'historical_incidents' in dataset and not dataset['historical_incidents'].empty:
            plot_incident_trends(dataset['historical_incidents'])
            
    st.markdown("---")
    from app.views.shared import render_domain_kpi_impact
    render_domain_kpi_impact("Major Incidents (MI)")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Interactive GenAI Demos", "🔁 Recurring Incident RCA", "Remediation Workflow"])
    
    domain = "Major Incidents (MI)"
    demos = [
        "AI-driven Anomaly Detection & Predictive Analytics",
        "Self-healing and auto-remediation agentic workflow",
        "GenAI for Scenario Simulation",
        "GenAI-based Smart Knowledge Assist",
        "Root Cause Analysis Assistant & Agent",
        "Continuous Monitoring Agents (Health/Security/Configuration /Anomaly Detection)"
    ]
    
    with tab1:
        st.subheader("Interactive GenAI Demos")
        for demo in demos:
            render_agent_demo(demo, domain, kpis, dataset)
            
    with tab2:
        render_recurring_rca(dataset, kpis)
            
    with tab3:
        try:
            from app.utils.workflow_utils import RemediationWorkflow
            RemediationWorkflow.render_remediation_tab(domain)
        except ImportError:
            st.error("Remediation Workflow Engine is currently unavailable.")


