import json
import os

records = []

def add_record(category, name, goal, inputs, output, kpis, analysis, tools, agents):
    records.append({
        "Unnamed: 0": None,
        "Unnamed: 1": category,
        "Unnamed: 2": name,
        "Unnamed: 3": goal,
        "Unnamed: 4": inputs,
        "Unnamed: 5": tools,
        "Unnamed: 6": output,
        "Unnamed: 7": kpis,
        "Unnamed: 8": analysis,
        "Unnamed: 9": agents
    })

# Row 1 (Header)
add_record("Category", "Demo Name", "Goal of Demo (aligned to North Star)", "Inputs Required", "Output", "KPIs and Calculations", "Possible AI Analysis", "Relevant Vendor Tools", "Agents Involved")

# Category: Major Incidents (MI)
add_record(
    "Major Incidents (MI)",
    "AI-driven Anomaly Detection & Predictive Analytics",
    "Predict major incidents before they occur (Zero MI)",
    "Observability data (MELT, logs, traces); historical incidents; change data; threat intel; regulations (GDPR, SOX)",
    "Predictive alert with probability and root cause hypothesis",
    "Prediction Accuracy, Early Warning Time",
    "Multivariate pattern recognition; unsupervised ML (clustering, isolation forest)",
    "Netdata MCP, Splunk MCP, CrowdStrike Falcon MCP, Dynatrace MCP Gateway",
    "Monitoring Agent, Anomaly Detection Agent, Predictive Analytics Agent, Health Agent"
)

add_record(
    "Major Incidents (MI)",
    "Self-healing and auto-remediation agentic workflow",
    "Automatically resolve incidents, reduce MTTR (Zero MI)",
    "Correlated incidents + diagnostics; runbooks/SOPs; automation scripts; blast-radius rules; regulations (SOX, HIPAA)",
    "Automated remediation execution; post-validation confirmation",
    "MTTR Reduction, Auto-Remediation Rate",
    "Dynamic playbook generation; risk-based self-heal decision",
    "Palo Alto Networks Cortex AgentiX, Torq AI Agents, Azure SRE Agent, Peta (Agent Vault)",
    "Self Heal Agent, Guardian Agent, IR Agent, Patch Orchestrator Agents"
)

add_record(
    "Major Incidents (MI)",
    "GenAI for Scenario Simulation",
    "Proactively test resilience (Zero MI)",
    "Infrastructure topology; threat models; historical incident patterns; adversarial AI tools; regulations (PCI-DSS)",
    "Simulation report with failed controls and recommendations",
    "Control Effectiveness Score, Remediation Coverage",
    "Adversarial simulation (red team agent)",
    "CyberStrikeAI, SentinelOne (Red Teaming), AttackIQ",
    "No dedicated agent in images - could extend Threat Surface Reduction Agent"
)

add_record(
    "Major Incidents (MI)",
    "GenAI-based Smart Knowledge Assist",
    "Instant troubleshooting guidance, faster MTTR",
    "Internal knowledge base; public forums; real-time incident context; regulations (IP protection)",
    "Conversational step-by-step guide",
    "Knowledge search time, First contact resolution rate",
    "Knowledge gap analysis",
    "knowledge-mcp server, Varonis MCP Server, Microsoft Security Copilot",
    "Policy Enforcement Agent (smart assist), Incident Investigation Agent (knowledge fabric)"
)

add_record(
    "Major Incidents (MI)",
    "Root Cause Analysis Assistant & Agent",
    "Drastically reduce RCA time (Zero MI)",
    "Logs, traces, metrics; change events; CMDB/service map; known error DB; regulations (GDPR)",
    "AI-generated RCA draft with code commit and timeline",
    "RCA time reduction, RCA accuracy score",
    "Causal AI: hypothesis generation; evidence ranking",
    "Azure SRE Agent (Databricks MCP), Splunk MCP, CrowdStrike Falcon MCP",
    "Incident Investigation Agent, Health Agent, Predictive Analytics Agent"
)

add_record(
    "Major Incidents (MI)",
    "Continuous Monitoring Agents (Health/Security/Configuration /Anomaly Detection)",
    "Persistent monitoring for complex threats (Zero MI)",
    "Observability streams; security policies; configuration baselines; regulations (SOX, PCI-DSS)",
    "Contextual alert with specific threat/behaviour description",
    "Dwell time (detection), Analyst triage burden",
    "Behavioural baseline drift detection",
    "Wazuh MCP Server, Netdata MCP, CrowdStrike Falcon MCP, Gigamon",
    "Monitoring Agent, Health Agent, Configuration Agent, Anomaly Detection Agent"
)

# Category: Time to Provision
add_record(
    "Time to Provision",
    "End-to-end Incident Automation (Alert->Triage->Ticket->Action)",
    "Automate incident lifecycle, zero touch",
    "Alert source; ticketing APIs; enrichment sources; regulations (SOX, HIPAA)",
    "Auto-created enriched ticket; automated containment action",
    "Alert-to-ticket time, Manual handling reduction",
    "Criticality scoring based on asset role",
    "TheHive MCP, Cortex MCP Server, Wazuh MCP, Microsoft Sentinel MCP",
    "Alert Triage Agent, Zero Toil (ticket creation), Incident Investigation Agent (enrichment), Self Heal Agent (action)"
)

add_record(
    "Time to Provision",
    "Self-Service AI Co-pilot for Security tools",
    "Empower users to perform tasks securely, zero touch",
    "User identity/permissions; tool APIs; request templates; regulations (SOX)",
    "Self-service action (e.g., temporary firewall open)",
    "Provisioning time, IT ticket volume reduction",
    "Anomalous request detection",
    "Microsoft Security Copilot, Versa Verbo, Valence MCP Server",
    "Orchestrator Agent, Guardian Agent, (various action agents)"
)

add_record(
    "Time to Provision",
    "Device/Application/Identity provisioning agent",
    "Autonomous provisioning triggered by HR event, zero touch",
    "HR system trigger; IGA policies; endpoint management; regulations (GDPR, data residency)",
    "Fully configured user + welcome email",
    "Time-to-productivity, Compliance rate",
    "Role-based access prediction",
    "Microsoft Entra ID, Okta Workflows, ServiceNow",
    "IaC Agent, Zero Touch Provisioning Agent, Configuration Agent, Compliance Agent"
)

# Category: Automation Index
add_record(
    "Automation Index",
    "AI-powered Security tasks automation (log analysis, routine service requests)",
    "Automate repetitive tasks, raise automation index",
    "SOPs; tool APIs; observability data; regulations (SOX)",
    "Automated log summary; fulfilled service requests",
    "Tasks automated per day, Analyst time saved",
    "Workflow optimisation (suggest new automation)",
    "Torq AI Agents, Dropzone AI, Splunk MCP Server",
    "Alert Trigger Agent, Monitoring Agent, Policy Hygiene Agent"
)

add_record(
    "Automation Index",
    "Security Analysts Co-pilot (reporting, rule writing, correlation, script generation)",
    "Augment analysts with AI assistant, raise automation index",
    "Natural language prompts; tool APIs; threat intel; regulations (all)",
    "Executed complex task (e.g. write Sigma rule)",
    "Task success rate, Tool proficiency",
    "Proactive next-step suggestions",
    "Microsoft Security Copilot, CrowdStrike Falcon, Splunk AI Assistant",
    "Policy Enforcement Agent (smart assist), Incident Investigation Agent, IaC Agent"
)

# Category: Asset Visibility & Coverage
add_record(
    "Asset Visibility & Coverage",
    "AI-powered continuous asset discovery",
    "Always-up-to-date inventory, zero visibility gap",
    "Network observability; cloud APIs; endpoint telemetry; regulations (PCI-DSS)",
    "Real-time inventory updates (living CMDB)",
    "Inventory accuracy, Discovery latency",
    "Asset relationship mapping",
    "Gigamon, CrowdStrike Falcon (Enterprise Graph), Netdata MCP",
    "Shadow IT Discovery Agent, Monitoring Agent, Threat Surface Reduction Agent"
)

add_record(
    "Asset Visibility & Coverage",
    "Agentic AI to scan address range or cloud accounts non-stop",
    "Continuous probing for new/misconfigured resources, zero visibility gap",
    "Network ranges; cloud read-only credentials; scanning policies; regulations (PCI-DSS)",
    "Continuous discovery report with findings",
    "Coverage percentage, Rogue asset dwell time",
    "Intelligent scan prioritisation",
    "Wiz, Orca Security, SentinelOne (CSPM)",
    "Shadow IT Discovery Agent, (custom scanning agent needed)"
)

add_record(
    "Asset Visibility & Coverage",
    "Context-rich security inventory (ownership, criticality, dependency, config state)",
    "Enrich assets with business context, zero visibility gap",
    "CMDB; orchestration tools; HR/identity; observability; regulations (GDPR)",
    "Asset record with ownership, criticality, dependencies, compliance state",
    "Context coverage, Incident triage accuracy",
    "Criticality prediction from behaviour",
    "CrowdStrike Falcon, ServiceNow (AI/CMDB)",
    "Threat Surface Reduction Agent, Compliance Agent, Incident Investigation Agent"
)

add_record(
    "Asset Visibility & Coverage",
    "Agentic AI for Shadow IT & Cloud Sprawl",
    "Hunt unauthorised apps/cloud resources, zero visibility gap",
    "Network flows; CASB/SSE; cloud API usage; asset scans; regulations (SOX)",
    "Shadow IT report with risk and cost insights",
    "Shadow IT discovery rate, Cost leakage identified",
    "User behaviour analytics (power users)",
    "Netskope, Zscaler, Valence MCP Server",
    "Shadow IT Discovery Agent, GenAI Shadow IT Agent"
)

# Category: Compliance
add_record(
    "Compliance",
    "AI-powered configuration drift detection / continuous compliance monitoring",
    "Instant drift detection, zero non-compliance, zero config drift",
    "Desired state config (CIS, NIST, internal); actual state; regulations (all)",
    "Drift alert; real-time compliance score",
    "MTTD drift, Compliance coverage",
    "Drift prediction (which systems likely to drift)",
    "SentinelOne (CSPM/AI-SPM), Prisma Cloud, Versa",
    "Configuration Agent, Compliance Agent, Policy Enforcement Agent"
)

add_record(
    "Compliance",
    "Automated configuration drift remediation / self-healing agent",
    "Auto-revert non-compliant configs, zero non-compliance, zero config drift",
    "Remediation actions (IaC); tool write APIs; regulations (SOX, change mgmt)",
    "Auto-healing action with verification",
    "MTTR drift, Auto-remediation success rate",
    "Risk-based remediation (auto vs. approval)",
    "Palo Alto Networks Cortex AgentiX, Torq AI Agents, Azure SRE Agent",
    "Self Heal Agent, Configuration Agent, Guardian Agent"
)

add_record(
    "Compliance",
    "GenAI for Policy Management (Policy as Code)",
    "Translate compliance requirements into executable code, zero non-compliance",
    "Regulatory PDFs; written policies; target IaC language (e.g., Rego)",
    "Generated policy code + plain-English explanation",
    "Policy creation time, Policy accuracy",
    "Policy gap analysis (missing controls)",
    "Exabeam Nova, Checkmarx One Assist",
    "PaaS Agent, Policy Hygiene Agent"
)

# Category: Efficiency in Detection & Response
add_record(
    "Efficiency in Detection & Response",
    "AI-enabled alert triaging and enrichment with context",
    "Enrich alerts automatically, zero false positives",
    "Raw alert; context sources (CMDB, TIP, IGA); observability; regulations (GDPR)",
    "Enriched alert with asset owner, threat intel, user behaviour",
    "Alert enrichment time, Context utilisation",
    "Intelligent enrichment based on alert type",
    "Dropzone AI, Exabeam Nova, Microsoft Security Copilot, Cortex MCP",
    "Alert Triage Agent, Ticket Prioritization Agent, Incident Investigation Agent"
)

add_record(
    "Efficiency in Detection & Response",
    "False positive reduction agent",
    "Suppress noise, zero false positives",
    "Historical alert data (TP/FP); analyst feedback; observability baselines; regulations (data retention)",
    "Suppressed alert with confidence note",
    "Signal to noise ratio, False positive rate",
    "Pattern of life analysis",
    "Arctic Wolf Alpha AI, Dropzone AI, Wazuh MCP",
    "Event Mgmt Agent, Anomaly Detection Agent, Policy Hygiene Agent"
)

add_record(
    "Efficiency in Detection & Response",
    "AI-guided detection and response",
    "Guide analysis step-by-step, reduce response time",
    "Playbooks; real-time alert data; tool state; observability; regulations (legal hold)",
    "Next-recommended step (e.g., memory dump)",
    "Investigation completion rate, Analyst proficiency gain",
    "Adaptive guidance based on evidence",
    "CrowdStrike Falcon, SentinelOne Singularity, Exabeam Timeline",
    "Incident Investigation Agent, Orchestrator Agent, IR Agent"
)

add_record(
    "Efficiency in Detection & Response",
    "AI powered response playbooks",
    "Dynamically generate & execute tailored playbooks",
    "Incident context (IOCs, assets); tool APIs; threat intel; observability; regulations (legal, privacy)",
    "Dynamic playbook execution (isolate, block, search, notify)",
    "Playbook efficacy, Response time improvement",
    "Post incident playbook refinement",
    "Palo Alto Cortex AgentiX, Torq AI Agents, Malware Containment Agents, Dropzone AI",
    "IR Agent, Self Heal Agent, MIM Agent, Malware Containment Agent, Ransomware Kill Switch Agent"
)

# Category: Intelligent IT Security Operations
add_record(
    "Intelligent IT Security Operations",
    "Integrated tool ecosystem with AI orchestration",
    "Unify tools via AI conductor, intelligent ops",
    "APIs for all security tools; unified observability fabric; regulations (data integrity)",
    "Cross-tool investigation presented in single timeline",
    "Orchestration coverage, Investigation time reduction",
    "Topology aware orchestration",
    "Useful Infinity Platform, Splunk ES (with SOAR/UEBA), CrowdStrike Falcon",
    "Orchestrator Agent, Smart AI Bridge MCP"
)

add_record(
    "Intelligent IT Security Operations",
    "Threat Intel correlation across tools and actionable intel",
    "Transform raw intel into actionable rules, intelligent ops",
    "Threat intel feeds; tool capabilities; observability; regulations (data classification)",
    "Auto-generated signatures across SIEM, firewall, EDR",
    "Intel-to-detection time, Threat coverage",
    "Intel prioritisation based on asset inventory",
    "SentinelOne (Threat Intel), Cortex XSOAR, MISP MCP",
    "Threat Surface Reduction Agent, Malicious Domain Blocking Agent, Policy Hygiene Agent"
)

add_record(
    "Intelligent IT Security Operations",
    "AI co-pilot for tool administration (rules, updates, config, license, optimisation)",
    "Simplify tool maintenance, intelligent ops",
    "Tool configs; license data; best practices; regulations (change compliance)",
    "Optimisation suggestion (e.g. stale rules)",
    "Tool admin time reduction, Rule efficiency",
    "Anomaly detection in tool health",
    "Versa Verbo, Microsoft Security Copilot, Splunk AI Assistant",
    "Policy Hygiene Agent"
)

add_record(
    "Intelligent IT Security Operations",
    "Autonomous tool maintenance & optimisation (health, patch, signature, capacity)",
    "Self-maintaining tools, intelligent ops",
    "Vendor APIs; infrastructure health metrics; capacity thresholds; observability; regulations (update compliance)",
    "Auto-update; auto-scale alert",
    "Tool uptime, Patch/signature lag",
    "Predictive capacity planning",
    "VersaONE, CrowdStrike Falcon (platform health)",
    "Policy Hygiene Agent, Patch Orchestrator Agents, Health Agent"
)


final_data = {
    "columns": [
        "Unnamed: 0",
        "Unnamed: 1",
        "Unnamed: 2",
        "Unnamed: 3",
        "Unnamed: 4",
        "Unnamed: 5",
        "Unnamed: 6",
        "Unnamed: 7",
        "Unnamed: 8",
        "Unnamed: 9"
    ],
    "records": records
}

out_path = os.path.join(os.path.dirname(__file__), "app", "data", "demo_requirements.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=2)

print(f"Successfully wrote {len(records)} records to {out_path}")
