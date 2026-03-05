import streamlit as st
import os
import time
from datetime import datetime
import yaml
import random
import pandas as pd
from app.agents.manager import AgentManager
from app.utils.charts import plot_result_metric_card

def simulate_input_data(demo_name: str) -> dict:
    """Uses heuristics to generate mock 'simulated inputs' to demonstrate the agent receives context."""
    name_lower = demo_name.lower()
    data = {}
    
    if "asset" in name_lower or "inventory" in name_lower:
        data = {"Target Scope": "10.0.0.0/16 Subnet", "Discovery Method": "Active Ping & WMI", "Compliance Req": "NIST CSF ID.AM-1 (Asset Inventory)"}
    elif "incident" in name_lower or "triage" in name_lower or "root cause" in name_lower:
        data = {"Alert ID": f"INC-{random.randint(1000,9999)}", "Suspect IP": f"192.168.1.{random.randint(2,250)}", "Severity": "CRITICAL", "Compliance Req": "GDPR 72hr Breach Notification"}
    elif "compliance" in name_lower or "patch" in name_lower or "baseline" in name_lower:
        data = {"Framework": "CIS Controls v8", "Target Fleet": "Windows Server 2022 Servers", "Compliance Req": "PCI-DSS Req 6 (Patch Management)"}
    elif "provision" in name_lower or "automation" in name_lower:
        data = {"Requester": "System Administrator", "Approval State": "Pre-Approved Auto", "Compliance Req": "SOC 2 CC6.1 (Logical Access)"}
    elif "threat intel" in name_lower or "correlation" in name_lower:
        data = {"Active IOCs": random.randint(5, 50), "Feed Source": "CISA & Custom Feeds", "Compliance Req": "NIST CSF DE.TI-1 (Threat Intel)"}
    else:
        data = {"Context Target": "Enterprise Master Dataset", "Operation Mode": "Autonomous", "Compliance Req": "General ITGC"}
        
    return data

def get_simulated_steps(demo_name: str) -> list[str]:
    """Generates fake capability steps to simulate the agent doing work based on heuristics."""
    name_lower = demo_name.lower()
    
    if "asset" in name_lower:
        return ["Initializing discovery daemon...", "Executing subnet sweeps...", "Correlating with CMDB...", "Normalizing asset taxonomy..."]
    elif "incident" in name_lower or "triage" in name_lower:
        return ["Fetching raw alert logs from SIEM...", "Querying EDR telemetry...", "Validating IOCs against Threat Intel...", "Drafting triage summary..."]
    elif "root cause" in name_lower:
        return ["Reconstructing process tree timeline...", "Identifying patient zero artifact...", "Mapping to MITRE ATT&CK...", "Finalizing Root Cause Analysis..."]
    elif "remediation" in name_lower or "response" in name_lower or "healing" in name_lower:
        return ["Evaluating remediation safety...", "Generating containment script...", "Quarantining compromised host...", "Verifying host isolation..."]
    elif "patch" in name_lower or "compliance" in name_lower:
        if "drift" in name_lower:
            return ["Analyzing baseline configuration states...", "Comparing live telemetry with desired state...", "Calculating drift vectors...", "Identifying non-compliant configuration keys..."]
        elif "policy" in name_lower or "pac" in name_lower:
            return ["Ingesting natural language requirements...", "Mapping to security framework controls...", "Generating Policy-as-Code (PaC) templates...", "Validating syntax and logic..."]
        return ["Scanning fleet for CVEs...", "Cross-referencing patch registries...", "Simulating patch deployment...", "Calculating compliance delta..."]
    else:
        return ["Initializing LangChain Agent...", "Ingesting synthetic KPI context...", "Consulting security knowledge base...", "Orchestrating autonomous pipeline..."]

def get_structured_output(demo_name: str, simulated_inputs: dict) -> list[str]:
    """Generates mock structured capabilities output to satisfy Step 4."""
    name_lower = demo_name.lower()
    
    if "asset" in name_lower or "inventory" in name_lower:
        return [
            f"✅ Discovered 14 new unmanaged devices in {simulated_inputs.get('Target Scope', 'target scope')}.",
            "✅ Classified 3 shadow-IT server instances running outdated Apache.",
            "✅ Enriched CMDB with owner tags via identity tenant lookup."
        ]
    elif "incident" in name_lower or "triage" in name_lower or "root cause" in name_lower:
        return [
            f"✅ Correlated initial access vector for {simulated_inputs.get('Alert ID', 'Alert')}: Phishing -> Credential Theft.",
            f"✅ Identified lateral movement from Suspect IP {simulated_inputs.get('Suspect IP', 'Unknown')}.",
            "✅ Mitre ATT&CK Mapping: T1566 (Phishing), T1078 (Valid Accounts)."
        ]
    elif "remediation" in name_lower or "healing" in name_lower or "automation" in name_lower:
        return [
            "✅ Generated containment playbook execution script.",
            "✅ Disabled compromised Active Directory user account.",
            "✅ Appended IP blocks to edge firewall ACLs.",
            "✅ Notified SOC channel #incident-response."
        ]
    elif "patch" in name_lower or "compliance" in name_lower or "baseline" in name_lower:
        if "drift" in name_lower:
            return [
                "✅ Detected 12 high-priority drift events in Production S3 buckets.",
                "✅ Identified unauthorized IAM role modifications on 4 instances.",
                "✅ Normalized drift report ready for auto-remediation."
            ]
        elif "policy" in name_lower or "pac" in name_lower:
            return [
                "✅ Generated 4 Terraform/Rego policy files for NIST 800-53 compliance.",
                "✅ Successfully mapped regulatory controls to executable code hooks.",
                "✅ CI/CD pull request generated for policy deployment."
            ]
        return [
            "✅ Identified 42 servers missing critical zero-day patch.",
            f"✅ Flagged 15 deviations from {simulated_inputs.get('Framework', 'Baseline')} configuration standard.",
            "✅ Auto-generated ServiceNow change request CRQ-99382 for patch deployment."
        ]
    else:
        return [
            "✅ Retrieved telemetry from 6 integrated EDR/SIEM tools.",
            "✅ Normalized data into unified OCSF schema.",
            "✅ Successfully applied continuous monitoring constraints."
        ]

def generate_mock_result_metrics(demo_name: str) -> list[dict]:
    name_lower = demo_name.lower()
    if "asset" in name_lower:
        return [
            {"title": "Total Scanned", "val": "14,204", "sub": "IPs Covered", "theme": "neutral"},
            {"title": "Unmanaged", "val": "14", "sub": "Shadow IT", "theme": "critical"},
            {"title": "Outdated OS", "val": "82", "sub": "Needs Patch", "theme": "warning"},
            {"title": "Enriched", "val": "100%", "sub": "CMDB Match", "theme": "success"}
        ]
    elif "incident" in name_lower or "root cause" in name_lower or "triage" in name_lower:
        return [
            {"title": "Signals Analysed", "val": "8,401", "sub": "Raw events", "theme": "neutral"},
            {"title": "Malicious IOCs", "val": "3", "sub": "Confirmed", "theme": "critical"},
            {"title": "Lateral Paths", "val": "2", "sub": "Blocked", "theme": "warning"},
            {"title": "Confidence", "val": "98%", "sub": "AI certainty", "theme": "success"}
        ]
    elif "patch" in name_lower or "compliance" in name_lower or "drift" in name_lower:
        return [
            {"title": "Total Rules", "val": "2,841", "sub": "Analyzed", "theme": "neutral"},
            {"title": "Overly Permissive", "val": "21.2%", "sub": "High risk", "theme": "critical"},
            {"title": "Drift Detected", "val": "12", "sub": "Unapproved auth", "theme": "warning"},
            {"title": "Potential Reduction", "val": "11.8%", "sub": "Rule count", "theme": "success"}
        ]
    else:
        return [
            {"title": "Items Evaluated", "val": "1,024", "sub": "Execution batch", "theme": "neutral"},
            {"title": "Critical Issues", "val": "5", "sub": "Action required", "theme": "critical"},
            {"title": "Anomalies", "val": "17", "sub": "Deviations", "theme": "warning"},
            {"title": "Resolution Rate", "val": "94%", "sub": "Automated", "theme": "success"}
        ]

def generate_mock_result_data(demo_name: str) -> pd.DataFrame:
    name_lower = demo_name.lower()
    if "patch" in name_lower or "compliance" in name_lower or "drift" in name_lower:
        return pd.DataFrame({
            "rule_id": ["FWR-1115", "FWR-1118", "FWR-1262", "FWR-1356", "FWR-1402"],
            "resource_name": ["FW-INTERNAL-19", "FW-DMZ-17", "FW-INTERNAL-11", "FW-CORE-17", "FW-INTERNAL-5"],
            "hit_count": [0, 0, 0, 217, 223],
            "last_used": ["2025-09-14 14:23:18", "2025-09-06 14:23:18", "2025-03-13 14:23:18", "2025-04-14 14:23:18", "2025-03-26 14:23:18"],
            "business_justification": ["Monitoring", "Monitoring", "Backup", "Management Access", "Monitoring"],
            "ai_confidence": ["99.2%", "98.5%", "94.0%", "88.1%", "86.4%"],
            "ai_recommendation": ["Revoke", "Revoke", "Restrict CIDR", "Review", "Review"]
        })
    elif "asset" in name_lower or "inventory" in name_lower:
        return pd.DataFrame({
            "asset_ip": ["10.0.45.22", "10.0.12.9", "10.0.88.104", "10.0.5.55"],
            "detected_os": ["Win Server 2012 R2", "Ubuntu 18.04 LTS", "Unknown IoT", "CentOS 7"],
            "owner": ["Unassigned", "DevOps-Team", "Unassigned", "Finance-IT"],
            "vulnerabilities": ["Critical (CVSS 9.8)", "High (CVSS 7.5)", "None", "Medium (CVSS 5.3)"],
            "ai_confidence": ["99.9%", "95.5%", "100%", "92.1%"],
            "ai_action": ["Isolate & Ticket", "Notify Owner", "Block at NAC", "Schedule Patch"]
        })
    elif "prov" in name_lower or "ident" in name_lower:
         return pd.DataFrame({
            "user_id": ["admin_jdoe", "svc_backup", "contractor_55", "dev_api_key"],
            "risk_score": [92, 85, 78, 65],
            "anomaly_reason": ["Impossible Travel (RU -> US)", "Stale credential usage", "Off-hours access", "Permissive wildcard (*.*)"],
            "ai_confidence": ["98.8%", "97.1%", "89.4%", "85.0%"],
            "ai_action": ["Suspend Account", "Rotate Keys", "Enforce MFA", "Scope Reduction"]
        })
    else:
        return pd.DataFrame({
            "entity_id": [f"ENT-{random.randint(100,999)}" for _ in range(5)],
            "threat_vector": ["Credential Dumping (T1003)", "Ransomware Encrypt (T1486)", "Data Exfiltration (T1048)", "C2 Beacon (T1071)", "Lateral Movement (T1210)"],
            "ai_confidence": ["99.8%", "98.5%", "94.2%", "91.0%", "88.5%"],
            "mitigation_status": ["Quarantined", "Process Killed", "IP Blocked (Edge)", "DNS Sinkholed", "Logged"]
        })

def render_agent_demo(demo_name: str, domain_name: str, kpis: dict, dataset: dict):
    """
    Standardized UI component for rendering a single sub-demo strictly following 
    the AGENTS_final.md 5-Section Pipeline.
    """
    if 'agent_logs' not in st.session_state:
        st.session_state.agent_logs = []
        
    with st.expander(f"▶️ Demo: {demo_name}", expanded=False):
        st.markdown(f"**Domain:** `{domain_name}` | **Capability:** AI-Driven Execution")
        st.markdown("---")
        
        # --- DEMO OBJECTIVE BRIEF ---
        st.markdown(f"**Objective:** Demonstrate how a GenAI agent can automate **{demo_name.lower()}** tasks using contextual enterprise telemetry while adhering strictly to predefined safety boundaries.")
        st.markdown("---")
        
        # --- SECTION 1: Input Data ---
        st.subheader("SECTION 1 — Input Data & Guardrails")
        
        # Determine demo context to generate appropriate interactive inputs
        name_lower = demo_name.lower()
        interactive_inputs = {}
        
        col1, col2, col3 = st.columns([1.2, 1, 1])
        with col1:
            st.caption("Agent Runtime Context (Interactive)")
            if "incident" in name_lower or "root cause" in name_lower or "triage" in name_lower:
                interactive_inputs['Incident Severity'] = st.selectbox("Incident Severity", ["Critical", "High", "Medium", "Low"], key=f"dd1_{demo_name}")
                interactive_inputs['Attacked Asset Type'] = st.selectbox("Attacked Asset Type", ["Database Server", "Employee Endpoint", "Cloud Workload", "Network Gateway"], key=f"dd2_{demo_name}")
            elif "asset" in name_lower or "inventory" in name_lower or "shadow" in name_lower:
                interactive_inputs['Scan Scope'] = st.multiselect("Scan Scope", ["AWS Production", "Azure Dev", "On-Prem Datacenter", "Remote Endpoints"], default=["AWS Production"], key=f"dd1_{demo_name}")
                interactive_inputs['Discovery Aggressiveness'] = st.selectbox("Discovery Aggressiveness", ["Passive Listen", "Active Port Scan", "Authenticated WMI/SSH"], key=f"dd2_{demo_name}")
            elif "compliance" in name_lower or "baseline" in name_lower or "config" in name_lower:
                if "drift" in name_lower:
                    interactive_inputs['Monitoring Target'] = st.selectbox("Monitoring Target", ["Public Cloud IAM", "S3/Storage Buckets", "Kubernetes RBAC", "Network Security Groups"], key=f"dd1_{demo_name}")
                    interactive_inputs['Detection Sensitivity'] = st.selectbox("Sensitivity", ["Real-time (High)", "Hourly (Medium)", "Daily (Low)"], key=f"dd2_{demo_name}")
                elif "policy" in name_lower or "pac" in name_lower:
                    interactive_inputs['Policy framework'] = st.selectbox("Target Framework", ["NIST 800-53", "CIS v8", "SOC 2", "HIPAA"], key=f"dd1_{demo_name}")
                    interactive_inputs['Output Language'] = st.selectbox("Output Language", ["Terraform (HCL)", "Open Policy Agent (Rego)", "AWS CloudFormation", "Azure Bicep"], key=f"dd2_{demo_name}")
                else:
                    interactive_inputs['Target Framework'] = st.selectbox("Target Framework", ["CIS v8", "NIST 800-53", "PCI-DSS v4.0", "ISO 27001"], key=f"dd1_{demo_name}")
                    interactive_inputs['Enforcement Mode'] = st.selectbox("Enforcement Mode", ["Audit Only", "Auto-Remediate (Safe)", "Strict Block"], key=f"dd2_{demo_name}")
            elif "alert" in name_lower or "false positive" in name_lower:
                interactive_inputs['Alert Category'] = st.selectbox("Alert Category", ["Suspicious Process Execution", "Multiple Failed Logins", "Malware Detected", "Unusual Network Traffic"], key=f"dd1_{demo_name}")
                interactive_inputs['Enrichment Source'] = st.multiselect("Enrichment Sources", ["Threat Intel Feed", "Active Directory", "EDR Logs", "Firewall Logs"], default=["Threat Intel Feed", "EDR Logs"], key=f"dd2_{demo_name}")
            elif "prov" in name_lower or "ident" in name_lower:
                interactive_inputs['Identity Risk Level'] = st.selectbox("Target Risk Level", ["High", "Medium", "Low"], key=f"dd1_{demo_name}")
                interactive_inputs['Provisioning Action'] = st.selectbox("Action", ["JIT Access Grant", "Revoke Privileges", "Force MFA Registration", "Isolate User"], key=f"dd2_{demo_name}")
            else:
                interactive_inputs['Execution Target'] = st.selectbox("Execution Target", ["Global", "Regional (EMEA)", "Regional (US)", "Specific Subnet"], key=f"dd1_{demo_name}")
                interactive_inputs['Priority Level'] = st.selectbox("Priority Level", ["Routine", "Urgent", "Emergency"], key=f"dd2_{demo_name}")
                
        with col2:
            st.caption("Human-in-the-Loop Override & Compliance")
            
            # Load compliance frameworks
            available_frameworks = []
            comp_data = {}
            yaml_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'compliance_frameworks.yaml')
            if os.path.exists(yaml_path):
                try:
                    with open(yaml_path, 'r') as f:
                        comp_data = yaml.safe_load(f)
                        available_frameworks = list(comp_data.keys())
                except Exception as e:
                    pass
            
            selected_fw = st.multiselect("Regulatory Frameworks", available_frameworks, default=[available_frameworks[0]] if available_frameworks else [], key=f"fw_{demo_name}")
            
            custom_instruction = st.text_area(
                "Scenario Parameters", 
                placeholder="e.g., Explain business impact.", 
                key=f"user_input_{demo_name}",
                height=68
            )

        with col3:
            st.caption("Active Guardrails")
            st.markdown("""
            <div style="font-size: 0.85em; background-color: #1e1e2e; padding: 10px; border-radius: 5px; border-left: 3px solid #ff4b4b;">
                <li>🔒 Prevent unauthorized DB access</li>
                <li>🔒 Read-only data operations</li>
                <li>🔒 Human approval for isolation</li>
                <li>🔒 No sensitive PII exfiltration</li>
            </div>
            """, unsafe_allow_html=True)

        # Identify the most relevant dataset for preview
        preview_key = "assets"
        if "incident" in name_lower or "root cause" in name_lower:
            preview_key = "incidents"
        elif "alert" in name_lower or "triage" in name_lower:
            preview_key = "alerts"
        elif "patch" in name_lower:
            preview_key = "patch_status"
        elif "prov" in name_lower or "ident" in name_lower:
            preview_key = "identity_data"
        elif "config" in name_lower or "baseline" in name_lower:
            preview_key = "config_baselines"
        elif "intel" in name_lower:
            preview_key = "threat_intel"
            
        df_preview = dataset.get(preview_key, pd.DataFrame())
        
        if not df_preview.empty:
            st.markdown("---")
            st.caption(f"Contextual Dataset Reference: `{preview_key}.csv` ({len(df_preview):,} total records)")
            st.dataframe(df_preview.head(5), width="stretch", hide_index=True)
            
            csv = df_preview.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"⬇️ Download Contextual Dataset",
                data=csv,
                file_name=f"{preview_key}_sample.csv",
                mime='text/csv',
                key=f"dl_{demo_name}"
            )
            
        if st.button(f"Execute Workflow", key=f"btn_{demo_name}", type="primary", use_container_width=True):
            if not os.getenv("OPENAI_API_KEY"):
                st.error("Error: OPENAI_API_KEY is not set. Please add it to your .env file.")
                return
                
            manager = AgentManager()
            
            # Use the dynamically selected inputs combined with custom instructions for the capability simulation
            steps = get_simulated_steps(demo_name)
            structured_output = get_structured_output(demo_name, interactive_inputs)
            
            # --- SECTION 2: Processing ---
            st.markdown("---")
            st.subheader("SECTION 2 — Processing (AI / Agent Actions)")
            
            with st.status(f"Simulating LangChain Agent Workflow...", expanded=True) as status:
                for step in steps:
                    st.write(f"🔄 {step}")
                    time.sleep(1.0)
                
                # --- SECTION 3: Output ---
                st.markdown("---")
                st.subheader("SECTION 3 — Task Output")
                for output in structured_output:
                    st.success(output)
                    
                st.write("🧠 Handing off execution context to LLM for final analysis...")
                
                simulated_inputs_str = str(interactive_inputs).replace("{", "{{").replace("}", "}}")
                structured_output_str = str(structured_output).replace("{", "{{").replace("}", "}}")
                
                
                role = "Security Copilot"
                
                # Extract specific framework controls if selected
                fw_context = ""
                if selected_fw and comp_data:
                    fw_context = "ACTIVE REGULATORY REQUIREMENTS:\n"
                    for fw in selected_fw:
                        fw_context += f"Framework {fw}:\n"
                        for ctrl, desc in comp_data[fw].items():
                            fw_context += f" - {ctrl}: {desc}\n"
                
                extended_instruction = f"""
SIMULATED SYSTEM CONTEXT: You are explicitly executing Section 4 (AI Analysis) for the '{demo_name}' sub-demo within the '{domain_name}' domain. 

Based on these inputs: {simulated_inputs_str}
And these simulated task outputs: {structured_output_str}
{fw_context}
USER SCENARIO PARAMETERS: {custom_instruction}

IMPORTANT INSTRUCTION: You MUST format your response into exactly THREE distinct sections using Markdown headers:

### 🧠 AI Analysis & Compliance Mapping
(Explain findings, reasoning, and explicitly map the actions to the provided Active Regulatory Requirements controls. Use enterprise terminology.)

### 📋 Recommended Action Plan
(Provide a prioritized, actionable list of next steps. Identify affected areas, ARNs/IPs, and explicit rules.)

### 🎯 AI Confidence Score
(Provide a final line stating **Confidence: XX%** and briefly explain *why* the AI holds this confidence level based on the clarity of the telemetry and alignment with compliance rules.)
"""
                
                result = manager.run_agent(role, kpis, extended_instruction)
                status.update(label="Workflow Complete", state="complete", expanded=False)

            if "⚠️" in result:
                st.error(result)
            else:
                st.session_state.agent_logs.append({
                    "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Agent Task": demo_name,
                    "Domain": domain_name,
                    "Status": "Analysis Complete" if "⚠️" not in result else "Blocked"
                })
                
                # --- NEW SECTION 4: AI Analysis & Data Outcomes ---
                st.markdown("---")
                st.subheader("SECTION 4 — Result Outcomes & Action Plan")
                
                # Visual Metrics
                metrics_data = generate_mock_result_metrics(demo_name)
                m_cols = st.columns(4)
                for i, m in enumerate(metrics_data):
                    with m_cols[i]:
                        plot_result_metric_card(m['title'], m['val'], m['sub'], m['theme'])
                        
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Data Grid
                st.markdown("**🔍 Affected Data Records (Simulated Grid)**")
                df_out = generate_mock_result_data(demo_name)
                
                # Style the dataframe to stand out
                def highlight_critical(val):
                    if isinstance(val, str) and ("Critical" in val or "Revoke" in val or "Suspend" in val or "Quarantined" in val or "Blocked" in val):
                        return 'color: #ff4b4b; font-weight: bold'
                    return ''
                
                # Fix pandas styler deprecation
                styled_df = df_out.style.map(highlight_critical)
                st.dataframe(styled_df, width="stretch", hide_index=True)
                st.markdown("<br>", unsafe_allow_html=True)

                # GenAI Text Analysis
                with st.container(border=True):
                    st.markdown(result)
                    
                # --- SECTION 5: KPI Impact ---
                st.markdown("---")
                st.subheader(f"SECTION 5 — KPI Impact (Simulated)")
                col_a, col_b = st.columns(2)
                
                # Synthetic Before/After metrics based on the demo
                if "incident" in name_lower or "triage" in name_lower:
                    metric_name = "MTTR"
                    before = f"{kpis.get('mean_time_to_respond_hrs', 12.0):.1f} hrs"
                    after = f"{kpis.get('mean_time_to_respond_hrs', 12.0) * 0.3:.1f} hrs"
                elif "alert" in name_lower or "false positive" in name_lower:
                    metric_name = "False Positive Rate"
                    before = f"{kpis.get('false_positive_rate_pct', 60.0)}%"
                    after = "8.2%"
                elif "asset" in name_lower or "discovery" in name_lower:
                    metric_name = "Asset Visibility Coverage"
                    before = f"{kpis.get('asset_coverage_pct', 85.0)}%"
                    after = "99.8%"
                else:
                    metric_name = "Automation Workflow Efficiency"
                    before = "22%"
                    after = "89%"
                    
                with col_a:
                    st.metric(f"Before AI Intervention: {metric_name}", before)
                with col_b:
                    st.metric(f"After AI Intervention: {metric_name}", after, delta="Improved", delta_color="normal")
