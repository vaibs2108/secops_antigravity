import streamlit as st
import pandas as pd
import altair as alt

# ═══════════════════════════════════════════════════════════════
# Premium Chart Theme — Executive Enterprise Palette
# ═══════════════════════════════════════════════════════════════
BRAND_BLUE = '#2563EB'
BRAND_NAVY = '#1E3A8A'
ACCENT_CYAN = '#06B6D4'
ACCENT_EMERALD = '#10B981'
ACCENT_AMBER = '#F59E0B'
ACCENT_ROSE = '#F43F5E'
ACCENT_VIOLET = '#8B5CF6'
CHART_COLORS = [BRAND_BLUE, ACCENT_CYAN, ACCENT_EMERALD, ACCENT_AMBER, ACCENT_ROSE, ACCENT_VIOLET, '#EC4899', '#14B8A6']
SEVERITY_DOMAIN = ['Critical', 'High', 'Medium', 'Low']
SEVERITY_RANGE = ['#EF4444', '#F97316', '#EAB308', '#3B82F6']


def _chart_card_header(title: str, subtitle: str = ""):
    """Renders a clean card header above a chart."""
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; padding: 0 2px;">
        <span style="font-size: 0.88rem; font-weight: 700; color: #1E293B; font-family: 'Outfit', sans-serif;">{title}</span>
        {f'<span style="font-size: 0.7rem; color: #94A3B8; font-weight: 500;">{subtitle}</span>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def _base_theme():
    """Returns a dict of common Altair configure kwargs for all charts."""
    return {
        'strokeOpacity': 0  # view config
    }


# ═══════════════════════════════════════════════════════════════
# 1. INCIDENT TRENDS — Smooth Gradient Area Chart
# ═══════════════════════════════════════════════════════════════
def plot_incident_trends(incidents_df: pd.DataFrame):
    if incidents_df.empty:
        st.info("No incident data available.")
        return

    _chart_card_header("Incident Trends", "Last 30 Days")

    df = incidents_df.copy()
    df['date'] = df['timestamp'].dt.date

    # Stacked area by severity — each color band shows daily volume per severity
    daily_sev = df.groupby(['date', 'severity']).size().reset_index(name='count')

    chart = alt.Chart(daily_sev).mark_area(
        interpolate='monotone',
        opacity=0.8
    ).encode(
        x=alt.X('date:T', title='', axis=alt.Axis(format='%b %d', labelAngle=0,
                 labelColor='#94A3B8', gridColor='#F1F5F9', domainColor='#E2E8F0')),
        y=alt.Y('count:Q', title='',  stack='zero', axis=alt.Axis(
                 labelColor='#94A3B8', gridColor='#F1F5F9', domainColor='#E2E8F0')),
        color=alt.Color('severity:N',
                        scale=alt.Scale(domain=SEVERITY_DOMAIN, range=SEVERITY_RANGE),
                        legend=None),
        order=alt.Order('severity_order:Q'),
        tooltip=[alt.Tooltip('date:T', title='Date', format='%b %d'),
                 alt.Tooltip('severity:N', title='Severity'),
                 alt.Tooltip('count:Q', title='Count')]
    ).transform_calculate(
        severity_order="indexof(['Critical','High','Medium','Low'], datum.severity)"
    ).properties(
        height=220
    ).configure_view(strokeOpacity=0).configure_axis(
        labelFont='Outfit', titleFont='Outfit',
        labelFontSize=11, titleFontSize=12
    )

    st.altair_chart(chart, use_container_width=True)

    # Severity mini-legend below using colored pills
    sev_counts = df['severity'].value_counts()
    pills = ""
    for sev, color in zip(SEVERITY_DOMAIN, SEVERITY_RANGE):
        cnt = sev_counts.get(sev, 0)
        pills += f'<span style="display:inline-flex;align-items:center;gap:4px;margin-right:14px;font-size:0.72rem;color:#64748B;font-family:Outfit,sans-serif;"><span style="width:8px;height:8px;border-radius:50%;background:{color};display:inline-block;"></span>{sev}: <b style="color:#1E293B;">{cnt}</b></span>'
    st.markdown(f'<div style="padding:0 2px;">{pills}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 2. ALERT BREAKDOWN — Clean Donut with Center Stat
# ═══════════════════════════════════════════════════════════════
def plot_alert_severity(alerts_df: pd.DataFrame):
    if alerts_df.empty:
        st.info("No alert data available.")
        return

    _chart_card_header("Alert Distribution", "By Severity")

    counts = alerts_df['severity'].value_counts().reset_index()
    counts.columns = ['severity', 'count']
    total = counts['count'].sum()

    donut = alt.Chart(counts).mark_arc(
        innerRadius=58,
        outerRadius=82,
        cornerRadius=5,
        padAngle=0.02
    ).encode(
        theta=alt.Theta('count:Q', stack=True),
        color=alt.Color('severity:N',
                        scale=alt.Scale(domain=SEVERITY_DOMAIN, range=SEVERITY_RANGE),
                        legend=None),
        tooltip=[alt.Tooltip('severity:N', title='Severity'),
                 alt.Tooltip('count:Q', title='Alerts', format=',')]
    )

    # Center label showing total
    center_text = alt.Chart(pd.DataFrame({'text': [f'{total:,}'], 'sub': ['Total']})).mark_text(
        fontSize=22, fontWeight='bold', color=BRAND_NAVY, font='Outfit', dy=-6
    ).encode(text='text:N')

    center_sub = alt.Chart(pd.DataFrame({'text': ['Alerts']})).mark_text(
        fontSize=11, color='#94A3B8', font='Outfit', dy=12
    ).encode(text='text:N')

    chart = (donut + center_text + center_sub).properties(
        height=200
    ).configure_view(strokeOpacity=0)

    st.altair_chart(chart, use_container_width=True)

    # Color-coded severity pills below
    pills = ""
    for sev, color in zip(SEVERITY_DOMAIN, SEVERITY_RANGE):
        cnt = counts[counts['severity'] == sev]['count'].values
        val = int(cnt[0]) if len(cnt) > 0 else 0
        pills += f'<span style="display:inline-flex;align-items:center;gap:4px;margin-right:12px;font-size:0.72rem;color:#64748B;font-family:Outfit,sans-serif;"><span style="width:8px;height:8px;border-radius:50%;background:{color};display:inline-block;"></span>{sev}: <b style="color:#1E293B;">{val:,}</b></span>'
    st.markdown(f'<div style="padding:2px 2px 0 2px;">{pills}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 3. SECURITY COVERAGE — Horizontal Progress Bars
# ═══════════════════════════════════════════════════════════════
def plot_coverage_metrics(kpis: dict):
    _chart_card_header("Security Coverage", "% Compliance")

    metrics = {
        "Admin MFA": kpis.get("admin_mfa_coverage_pct", 0),
        "Patch": kpis.get("patch_compliance_pct", 0),
        "Config": kpis.get("config_management_coverage_pct", 0),
        "EDR": kpis.get("edr_coverage_pct", 0),
        "PAM JIT": kpis.get("pam_jit_usage_pct", 0)
    }

    # Render as styled HTML progress bars — individual calls to avoid escaping issues
    for name, val in metrics.items():
        val = round(val, 1)
        color = ACCENT_EMERALD if val >= 90 else ACCENT_AMBER if val >= 75 else ACCENT_ROSE
        pct = min(val, 100)
        st.markdown(
            f'<div style="margin-bottom:8px;">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:3px;">'
            f'<span style="font-size:0.78rem;color:#475569;font-family:Outfit,sans-serif;font-weight:600;">{name}</span>'
            f'<span style="font-size:0.78rem;color:#1E293B;font-family:Outfit,sans-serif;font-weight:700;">{val}%</span>'
            f'</div>'
            f'<div style="background:#F1F5F9;border-radius:6px;height:8px;overflow:hidden;">'
            f'<div style="width:{pct}%;height:100%;background:{color};border-radius:6px;"></div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )


# ═══════════════════════════════════════════════════════════════
# 4. COMPLIANCE DONUT — Radial Gauge with % Center
# ═══════════════════════════════════════════════════════════════
def plot_compliance_donut(score: float, title: str):
    """Renders a clean radial gauge for a compliance score."""
    score = round(score, 1)
    color = ACCENT_EMERALD if score >= 90 else ACCENT_AMBER if score >= 75 else ACCENT_ROSE

    _chart_card_header(title)

    # Pure HTML/CSS radial gauge — much cleaner than Altair donut
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:center;padding:12px 0 8px 0;">
        <div style="position:relative;width:130px;height:130px;">
            <svg viewBox="0 0 36 36" style="transform:rotate(-90deg);">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="#F1F5F9" stroke-width="3"/>
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{color}" stroke-width="3"
                      stroke-dasharray="{score}, 100"
                      stroke-linecap="round"/>
            </svg>
            <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;">
                <div style="font-size:1.4rem;font-weight:700;color:{BRAND_NAVY};font-family:Outfit,sans-serif;">{score}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 5. MTTX BAR — Horizontal Bars with Value Labels
# ═══════════════════════════════════════════════════════════════
def plot_mttx_bar(mttd: float, mttr: float):
    """Resolution timings with labeled horizontal bars."""
    _chart_card_header("Resolution Timings", "Hours")

    items = [
        ("MTTD", round(mttd, 1), BRAND_BLUE),
        ("MTTR", round(mttr, 1), ACCENT_AMBER)
    ]
    max_val = max(mttd, mttr, 1)

    for label, val, color in items:
        pct = min((val / max_val) * 100, 100)
        st.markdown(
            f'<div style="margin-bottom:10px;">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
            f'<span style="font-size:0.8rem;color:#475569;font-family:Outfit,sans-serif;font-weight:600;">{label}</span>'
            f'<span style="font-size:0.8rem;color:#1E293B;font-family:Outfit,sans-serif;font-weight:700;">{val}h</span>'
            f'</div>'
            f'<div style="background:#F1F5F9;border-radius:6px;height:10px;overflow:hidden;">'
            f'<div style="width:{pct}%;height:100%;background:{color};border-radius:6px;"></div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )


# ═══════════════════════════════════════════════════════════════
# 6. ASSET DISTRIBUTION — Clean Vertical Bars
# ═══════════════════════════════════════════════════════════════
def plot_asset_distribution(assets_df: pd.DataFrame):
    if assets_df.empty:
        return

    _chart_card_header("Assets by Type")

    counts = assets_df['type'].value_counts().reset_index()
    counts.columns = ['Type', 'Count']

    bars = alt.Chart(counts).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5
    ).encode(
        x=alt.X('Type:N', sort='-y', title='',
                axis=alt.Axis(labelAngle=-25, labelColor='#94A3B8', domainColor='#E2E8F0')),
        y=alt.Y('Count:Q', title='',
                axis=alt.Axis(labelColor='#94A3B8', gridColor='#F1F5F9', domainColor='#E2E8F0')),
        color=alt.Color('Type:N', scale=alt.Scale(range=CHART_COLORS), legend=None),
        tooltip=['Type', 'Count']
    )

    # Value labels on top of bars
    text = bars.mark_text(
        align='center', baseline='bottom', dy=-4,
        fontSize=11, fontWeight='bold', color='#475569', font='Outfit'
    ).encode(text='Count:Q')

    chart = (bars + text).properties(
        height=220
    ).configure_view(strokeOpacity=0).configure_axis(
        labelFont='Outfit', titleFont='Outfit'
    )

    st.altair_chart(chart, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# 7. KPI PROGRESS — Clean inline progress
# ═══════════════════════════════════════════════════════════════
def plot_kpi_progress(label: str, value: float, target: float = 100.0, format_str="%.1f%%"):
    percentage = min(value / target, 1.0)
    st.markdown(f"**{label}**")
    cols = st.columns([3, 1])
    with cols[0]:
        st.progress(percentage)
    with cols[1]:
        st.markdown(f"`{format_str % value}`")


# ═══════════════════════════════════════════════════════════════
# 8. COMPACT METRIC CARD
# ═══════════════════════════════════════════════════════════════
def plot_compact_metric_card(title: str, value: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px 18px; border: 1px solid #E2E8F0; margin-bottom: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.04);">
        <p style="color: #94A3B8; margin: 0; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; font-family: 'Outfit', sans-serif;">{title}</p>
        <h2 style="color: #1E293B; margin: 8px 0 0 0; font-size: 1.6rem; font-weight: 700; font-family: 'Outfit', sans-serif; letter-spacing: -0.03em;">{value}</h2>
        {f'<p style="color: #2563EB; margin: 4px 0 0 0; font-size: 0.7rem; font-weight: 500; font-family: Outfit, sans-serif;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 9. RESULT METRIC CARD (Demo outcomes)
# ═══════════════════════════════════════════════════════════════
def plot_result_metric_card(title: str, value: str, subtitle: str, theme: str = "neutral"):
    themes = {
        "neutral": {"bg": "#F8FAFC", "border": "#E2E8F0", "text": "#1E293B", "sub": "#64748B", "accent": "#2563EB"},
        "warning": {"bg": "#FFFBEB", "border": "#FDE68A", "text": "#92400E", "sub": "#B45309", "accent": "#F59E0B"},
        "critical": {"bg": "#FEF2F2", "border": "#FECACA", "text": "#991B1B", "sub": "#DC2626", "accent": "#EF4444"},
        "success": {"bg": "#F0FDF4", "border": "#BBF7D0", "text": "#166534", "sub": "#16A34A", "accent": "#10B981"}
    }
    t = themes.get(theme, themes["neutral"])
    st.markdown(f"""
    <div style="background: {t['bg']}; border-radius: 12px; padding: 18px; border: 1px solid {t['border']}; box-shadow: 0 1px 4px rgba(0,0,0,0.04);">
        <p style="color: {t['sub']}; margin: 0; font-size: 0.78rem; font-weight: 600; font-family: 'Outfit', sans-serif;">{title}</p>
        <h2 style="color: {t['text']}; margin: 8px 0 4px 0; font-size: 1.8rem; font-weight: 700; font-family: 'Outfit', sans-serif;">{value}</h2>
        <p style="color: {t['accent']}; margin: 0; font-size: 0.78rem; font-weight: 500;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 10. THREAT HEATMAP — Blues scheme, clean grid
# ═══════════════════════════════════════════════════════════════
def plot_threat_heatmap(incidents_df: pd.DataFrame):
    if incidents_df.empty:
        st.info("No incident data available for heatmap.")
        return

    _chart_card_header("Threat Velocity Heatmap", "Last 7 Days")

    df = incidents_df.copy()
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day_name()

    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day_map = {'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed',
               'Thursday': 'Thu', 'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'}
    df['day_short'] = df['day'].map(day_map)

    max_date = df['timestamp'].max()
    df = df[df['timestamp'] > (max_date - pd.Timedelta(days=7))]
    heat_df = df.groupby(['day_short', 'hour']).size().reset_index(name='count')

    chart = alt.Chart(heat_df).mark_rect(
        cornerRadius=3
    ).encode(
        x=alt.X('hour:O', title='',
                axis=alt.Axis(labelAngle=0, labelColor='#94A3B8', domainColor='#E2E8F0')),
        y=alt.Y('day_short:N', sort=day_order, title='',
                axis=alt.Axis(labelColor='#94A3B8', domainColor='#E2E8F0')),
        color=alt.Color('count:Q',
                        scale=alt.Scale(scheme='blues'),
                        title='Incidents',
                        legend=alt.Legend(orient='right', direction='vertical',
                                        gradientLength=120, labelColor='#94A3B8', titleColor='#64748B')),
        tooltip=[alt.Tooltip('day_short:N', title='Day'),
                 alt.Tooltip('hour:O', title='Hour'),
                 alt.Tooltip('count:Q', title='Incidents')]
    ).properties(
        height=200
    ).configure_view(strokeWidth=0).configure_axis(
        grid=False, labelFont='Outfit', titleFont='Outfit'
    )

    st.altair_chart(chart, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# 11. WORKFLOW VELOCITY — Stage pipeline bars
# ═══════════════════════════════════════════════════════════════
def plot_workflow_velocity(workflows_dict: dict):
    stages = ['identified', 'approved', 'implemented', 'verified', 'closed']
    stage_colors = [BRAND_BLUE, ACCENT_CYAN, ACCENT_EMERALD, ACCENT_AMBER, ACCENT_VIOLET]

    counts = {s: 0 for s in stages}

    if isinstance(workflows_dict, dict):
        for category_tickets in workflows_dict.values():
            if isinstance(category_tickets, list):
                for ticket in category_tickets:
                    stage = ticket.get('workflow_stage', 'identified').lower()
                    if stage in counts:
                        counts[stage] += 1
                    elif stage == 'draft':
                        counts['identified'] += 1
                    elif stage == 'pending_approval':
                        counts['identified'] += 1

    df = pd.DataFrame([{'Stage': s.capitalize(), 'Count': counts[s]} for s in stages])

    if df['Count'].sum() == 0:
        st.markdown("""
        <div style="background: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 160px;">
            <div style="font-size: 1.8rem; margin-bottom: 8px; opacity: 0.6;">📋</div>
            <p style="margin: 0; color: #64748B; font-size: 0.85rem; text-align: center; font-family: 'Outfit', sans-serif; font-weight: 600;">No active remediation tickets</p>
            <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.72rem;">Run a demo to generate workflow tickets</p>
        </div>
        """, unsafe_allow_html=True)
        return

    _chart_card_header("Workflow Pipeline")

    # Build pipeline cards as a flex row
    total = df['Count'].sum()
    cards = ""
    for i, (_, row) in enumerate(df.iterrows()):
        cards += (
            f'<div style="flex:1;text-align:center;background:#F8FAFC;border-radius:10px;padding:12px 6px;border:1px solid #E2E8F0;">'
            f'<div style="font-size:1.3rem;font-weight:700;color:{stage_colors[i]};font-family:Outfit,sans-serif;">{row["Count"]}</div>'
            f'<div style="font-size:0.65rem;color:#64748B;font-weight:600;margin-top:2px;text-transform:uppercase;letter-spacing:0.5px;">{row["Stage"]}</div>'
            f'</div>'
        )
    st.markdown(
        f'<div style="display:flex;gap:6px;padding:8px 0;">{cards}</div>',
        unsafe_allow_html=True
    )
