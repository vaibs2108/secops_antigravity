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
    
    for i, key in enumerate(metric_keys):
        with cols[i % 4]:
            if isinstance(dataset[key], pd.DataFrame):
                st.metric(label=f"{key.replace('_', ' ').title()}", value=f"{len(dataset[key]):,}")
            else:
                st.metric(label=f"{key}", value="N/A")
                
    st.markdown("---")
    
    # Dataset Selector
    selected_dataset = st.selectbox(
        "Select Dataset to Preview (First 50 Rows)",
        options=metric_keys,
        format_func=lambda x: x.replace('_', ' ').title()
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
    st.markdown("Download all 8 synthetic datasets packaged into a single ZIP archive for offline analysis.")
    
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
