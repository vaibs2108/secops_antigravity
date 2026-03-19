import streamlit as st
import pandas as pd
import altair as alt

def plot_incident_trends(incidents_df: pd.DataFrame):
    if incidents_df.empty:
        st.info("No incident data available for trends.")
        return
        
    st.subheader("Incident Trends (Last 30 Days)")
    
    # Extract date from timestamp
    df = incidents_df.copy()
    df['date'] = df['timestamp'].dt.date
    
    # Group by date and severity
    trend_df = df.groupby(['date', 'severity']).size().reset_index(name='count')
    
    chart = alt.Chart(trend_df).mark_line(point=True).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('count:Q', title='Number of Incidents'),
        color=alt.Color('severity:N', 
                        scale=alt.Scale(domain=['Critical', 'High', 'Medium', 'Low'],
                                        range=['#ff4b4b', '#ff7f0e', '#ffbb00', '#1f77b4']),
                        title='Severity'),
        tooltip=['date', 'severity', 'count']
    ).properties(
        height=300
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        labelColor='#475569',
        titleColor='#1e293b',
        gridColor='rgba(0,0,0,0.05)'
    ).configure_legend(
        labelColor='#475569',
        titleColor='#1e293b'
    ).interactive()
    
    st.altair_chart(chart, width='stretch')

def plot_alert_severity(alerts_df: pd.DataFrame):
    if alerts_df.empty:
        st.info("No alert data available.")
        return
        
    st.subheader("Alert Breakdown")
    
    counts = alerts_df['severity'].value_counts().reset_index()
    counts.columns = ['severity', 'count']
    
    chart = alt.Chart(counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="severity", type="nominal",
                        scale=alt.Scale(domain=['Critical', 'High', 'Medium', 'Low'],
                                        range=['#ff4b4b', '#ff7f0e', '#ffbb00', '#1f77b4'])),
        tooltip=['severity', 'count']
    ).properties(
        height=300
    ).configure_view(
        strokeOpacity=0
    ).configure_legend(
        labelColor='#475569',
        titleColor='#1e293b'
    )
    
    st.altair_chart(chart, width='stretch')

def plot_coverage_metrics(kpis: dict):
    st.subheader("Security Coverage")
    
    metrics = {
        "EDR": kpis.get("edr_coverage_pct", 0),
        "Config Mgmt": kpis.get("config_management_coverage_pct", 0),
        "Patch": kpis.get("patch_compliance_pct", 0),
        "Admin MFA": kpis.get("admin_mfa_coverage_pct", 0),
        "PAM JIT": kpis.get("pam_jit_usage_pct", 0)
    }
    
    df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Coverage (%)'])
    
    # Pre-calculate colors based on thresholds
    df['Color'] = '#d62728'  # Default Red (Below 75%)
    df.loc[df['Coverage (%)'] >= 75, 'Color'] = '#ff7f0e'  # Orange (75% to 89%)
    df.loc[df['Coverage (%)'] >= 90, 'Color'] = '#2ca02c'  # Green (90%+)
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Coverage (%):Q', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Metric:N', sort='-x'),
        color=alt.Color('Color:N', scale=None),
        tooltip=['Metric', 'Coverage (%)']
    ).properties(
        height=300
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        labelColor='#475569',
        titleColor='#1e293b',
        gridColor='rgba(0,0,0,0.05)'
    )
    
    st.altair_chart(chart, width='stretch')

def plot_compliance_donut(score: float, title: str):
    """Renders a simple donut chart for a percentage score."""
    st.subheader(title)
    df = pd.DataFrame({
        'Category': ['Compliant', 'Non-Compliant'],
        'Value': [score, 100 - score]
    })
    
    chart = alt.Chart(df).mark_arc(innerRadius=60).encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color(field="Category", type="nominal",
                        scale=alt.Scale(domain=['Compliant', 'Non-Compliant'],
                                        range=['#2ca02c', '#d62728'])),
        tooltip=['Category', 'Value']
    ).properties(
        height=250
    )
    
    # Adding text overlay for the score
    text = alt.Chart(pd.DataFrame({'Text': [f"{score}%"]})).mark_text(size=24, fontWeight='bold', color='#1e293b').encode(
        text='Text:N'
    )
    
    st.altair_chart((chart + text).configure_view(strokeOpacity=0).configure_legend(labelColor='#475569', titleColor='#1e293b'), width='stretch')

def plot_mttx_bar(mttd: float, mttr: float):
    """Renders a horizontal bar chart comparing MTTD and MTTR."""
    st.subheader("Incident Resolution Timings")
    df = pd.DataFrame({
        'Metric': ['Mean Time To Detect', 'Mean Time To Respond'],
        'Hours': [mttd, mttr]
    })
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Hours:Q', title='Hours'),
        y=alt.Y('Metric:N', title=''),
        color=alt.Color('Metric:N', scale=alt.Scale(range=['#1f77b4', '#ff7f0e'])),
        tooltip=['Metric', 'Hours']
    ).properties(
        height=200
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        labelColor='#475569',
        titleColor='#1e293b',
        gridColor='rgba(0,0,0,0.05)'
    )
    
    st.altair_chart(chart, width='stretch')
    
def plot_asset_distribution(assets_df: pd.DataFrame):
    """Renders a bar chart of asset types."""
    if assets_df.empty:
        return
        
    st.subheader("Enterprise Assets by Type")
    counts = assets_df['type'].value_counts().reset_index()
    counts.columns = ['Asset Type', 'Count']
    
    chart = alt.Chart(counts).mark_bar().encode(
        x=alt.X('Asset Type:N', sort='-y', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('Count:Q'),
        color=alt.Color('Asset Type:N', scale=alt.Scale(scheme='tableau10')),
        tooltip=['Asset Type', 'Count']
    ).properties(
        height=300
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        labelColor='#475569',
        titleColor='#1e293b',
        gridColor='rgba(0,0,0,0.05)'
    ).configure_legend(
        labelColor='#475569',
        titleColor='#1e293b'
    )
    st.altair_chart(chart, width='stretch')

def plot_kpi_progress(label: str, value: float, target: float = 100.0, format_str="%.1f%%"):
    """Renders a visual progress bar for a KPI metric."""
    percentage = min(value / target, 1.0)
    color = "success" if percentage >= 0.8 else "warning" if percentage >= 0.6 else "danger"
    
    st.markdown(f"**{label}**")
    
    # Render using the built-in streamlit progress bar and a styled col/row layout
    cols = st.columns([3, 1])
    with cols[0]:
        # Streamlit progress bar accepts values 0.0 to 1.0
        st.progress(percentage)
    with cols[1]:
        st.markdown(f"`{format_str % value}`")
        
def plot_compact_metric_card(title: str, value: str, subtitle: str = ""):
    """Renders a stylized CSS metric card instead of plain text."""
    st.markdown(f"""
    <div style="background-color: rgba(255, 255, 255, 0.7); border-radius: 12px; padding: 15px; border: 1px solid rgba(226, 232, 240, 0.8); margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.03);">
        <h5 style="color: #475569; margin: 0; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px;">{title}</h5>
        <h2 style="color: #0f172a; margin: 10px 0 0 0; font-size: 1.8em; font-weight: 700;">{value}</h2>
        {f'<p style="color: #1d4ed8; margin: 5px 0 0 0; font-size: 0.8em; font-weight: 600;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)
    
def plot_result_metric_card(title: str, value: str, subtitle: str, theme: str = "neutral"):
    """Renders a light-mode metric card for demo outcomes. Theme: neutral, warning, critical, success"""
    themes = {
        "neutral": {"bg": "#f8fafc", "border": "#e2e8f0", "text": "#0f172a", "sub": "#64748b"},
        "warning": {"bg": "#fefce8", "border": "#fef08a", "text": "#854d0e", "sub": "#a16207"},
        "critical": {"bg": "#fef2f2", "border": "#fecaca", "text": "#991b1b", "sub": "#b91c1c"},
        "success": {"bg": "#f0fdf4", "border": "#bbf7d0", "text": "#166534", "sub": "#15803d"}
    }
    t = themes.get(theme, themes["neutral"])
    
    st.markdown(f"""
    <div style="background-color: {t['bg']}; border-radius: 8px; padding: 15px; border: 1px solid {t['border']}; height: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <h5 style="color: {t['text']}; margin: 0; font-size: 0.85em; font-weight: 600; display: flex; align-items: center; gap: 8px;">{title}</h5>
        <h2 style="color: {t['text']}; margin: 10px 0 5px 0; font-size: 2em; font-weight: 700;">{value}</h2>
        <p style="color: {t['sub']}; margin: 0; font-size: 0.85em;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def plot_threat_heatmap(incidents_df: pd.DataFrame):
    """Renders an eye-catching 2D heatmap of incident frequency."""
    if incidents_df.empty:
        st.info("No incident data available for heatmap.")
        return
        
    st.subheader("Threat Velocity Heatmap")
    
    df = incidents_df.copy()
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day_name()
    
    # Define order for days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Aggregate data
    # Phase 73: Only show last 7 days for more "focused" variance in mock data
    max_date = df['timestamp'].max()
    df = df[df['timestamp'] > (max_date - pd.Timedelta(days=7))]
    heat_df = df.groupby(['day', 'hour']).size().reset_index(name='count')
    
    chart = alt.Chart(heat_df).mark_rect(
        stroke='rgba(0,0,0,0.1)',
        strokeWidth=1
    ).encode(
        x=alt.X('hour:O', title='Hour of Day (0-23)', axis=alt.Axis(labelAngle=0, labelColor='#475569', titleColor='#1e293b')),
        y=alt.Y('day:N', sort=day_order, title='Day of Week', axis=alt.Axis(labelColor='#475569', titleColor='#1e293b')),
        color=alt.Color('count:Q', 
                        scale=alt.Scale(scheme='turbo'), 
                        title='Incident Count',
                        legend=alt.Legend(labelColor='#475569', titleColor='#1e293b')),
        tooltip=['day', 'hour', 'count']
    ).properties(
        height=350
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=False
    )
    
    st.altair_chart(chart, width='stretch')

