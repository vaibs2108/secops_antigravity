import streamlit as st
import pandas as pd
import io
import zipfile

def render_data_explorer(dataset: dict):
    st.header("Synthetic Data Explorer")
    st.info("🎯 **Domain Objective:** Ensure complete data transparency and accessibility by providing tools to inspect, audit, and export the high-fidelity synthetic telemetry used throughout the platform simulations.")
    st.markdown("Explore, preview, and download the synthetic enterprise cybersecurity datasets generated for this session.")
    
    # Overview metrics
    st.subheader("Dataset Overview")
    cols = st.columns(4)
    metric_keys = list(dataset.keys())
    
    label_map = {
        "assets": "Assets (CMDB)",
        "alerts": "Security Alerts",
        "incidents": "Incident Tickets (ITIL)",
        "patch_status": "Vulnerability & Patch Status",
        "compliance": "Compliance Audit Logs",
        "threat_intel": "Threat Intel (CVE Feeds & IOCs)",
        "security_tools": "Admin Access Logs",
        "config_baselines": "Security Policy (Config Baselines)",
        "identity_data": "Identity & IGA (Okta/AD)",
        "observability_events": "Network Observability (Gigamon Flows)",
        "edr_telemetry": "Endpoint Management (EDR Telemetry)",
        "playbooks": "Remediation Playbooks (SOAR)",
        "threat_models": "Threat Models (MITRE ATT&CK)",
        "git_logs": "DevSecOps Git Logs (SAST)",
        "rca_documents": "RCA Documents (KEDB)",
        "financial_data": "Financial Logs (Shadow IT Discovery)"
    }
    
    def get_label(k):
        return label_map.get(k, k.replace('_', ' ').title())
    
    for i, key in enumerate(metric_keys):
        with cols[i % 4]:
            if isinstance(dataset[key], pd.DataFrame):
                st.metric(label=f"{get_label(key)}", value=f"{len(dataset[key]):,}")
            else:
                st.metric(label=f"{get_label(key)}", value="N/A")
                
    st.markdown("---")
    
    # Dataset Selector
    selected_dataset = st.selectbox(
        "Select Dataset to Preview (First 50 Rows)",
        options=metric_keys,
        format_func=get_label
    )
    
    if selected_dataset and isinstance(dataset[selected_dataset], pd.DataFrame):
        df = dataset[selected_dataset]
        
        # Schema info
        st.write(f"**Schema Overview:** `{len(df.columns)} Columns`")
        st.caption(", ".join(df.columns.tolist()))
        
        # Preview 50 rows
        st.dataframe(df.head(50), use_container_width=True, hide_index=True)
        
        # Individual Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"⬇️ Download {selected_dataset}.csv",
            data=csv,
            file_name=f"{selected_dataset}.csv",
            mime='text/csv'
        )
        
    st.markdown("---")
    st.subheader("Option B - Complete Dataset Bundle")
    st.markdown(f"Download all {len(dataset)} synthetic datasets packaged into a single ZIP archive for offline analysis.")
    
    # Generate Zip Bundle
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for key, df in dataset.items():
            if isinstance(df, pd.DataFrame):
                csv_bytes = df.to_csv(index=False).encode('utf-8')
                zip_file.writestr(f"{key}.csv", csv_bytes)
                
    st.download_button(
        label="📦 Download Full Dataset Bundle (.zip)",
        data=zip_buffer.getvalue(),
        file_name="security_dataset_bundle.zip",
        mime="application/zip",
        type="primary"
    )
