# Demo Validation Audit — SecOps Platform

> Full cross-reference of `demo_requirements.json` (master Excel) vs. each domain view file.

## Master Data Summary (demo_requirements.json — 24 demos total)

| # | Category (JSON) | Demo Name | North Star Tab |
|---|-----------------|-----------|----------------|
| 1 | Major Incidents (MI) | AI-driven Anomaly Detection & Predictive Analytics | 🎯 Zero MI |
| 2 | Major Incidents (MI) | Self-healing and auto-remediation agentic workflow | 🎯 Zero MI |
| 3 | Major Incidents (MI) | GenAI for Scenario Simulation | 🎯 Zero MI |
| 4 | Major Incidents (MI) | GenAI-based Smart Knowledge Assist | 🎯 Zero MI |
| 5 | Major Incidents (MI) | Root Cause Analysis Assistant & Agent | 🎯 Zero MI |
| 6 | Major Incidents (MI) | Continuous Monitoring Agents (Health/Security/Configuration/Anomaly detection) | 🎯 Zero MI |
| 7 | Time to Provision | End-to-end Incident Automation (Alert→Triage→Ticket→Action) | ⚡ Zero Touch |
| 8 | Time to Provision | Self-Service AI Co-pilot for Security tools | ⚡ Zero Touch |
| 9 | Time to Provision | Device/Application/Identity provisioning agent | ⚡ Zero Touch |
| 10 | Automation Index | AI-powered Security tasks automation (log analysis, routine service requests) | 🤖 Zero Toil |
| 11 | Automation Index | Security Analysts Co-pilot (reporting, rule writing, correlation, script generation) | 🤖 Zero Toil |
| 12 | Asset Visibility & Coverage | AI-powered continuous asset discovery | 🔍 Zero Visibility Gap |
| 13 | Asset Visibility & Coverage | Agentic AI to scan address range or cloud accounts non-stop | 🔍 Zero Visibility Gap |
| 14 | Asset Visibility & Coverage | Context-rich security inventory (ownership, criticality, dependency, config state) | 🔍 Zero Visibility Gap |
| 15 | Asset Visibility & Coverage | Agentic AI for Shadow IT & Cloud Sprawl | 🔍 Zero Visibility Gap |
| 16 | Compliance | AI-powered configuration drift detection / continuous compliance monitoring | ⚖️ Zero Non-Compliance |
| 17 | Compliance | Automated configuration drift remediation / self-healing agent | ⚖️ Zero Non-Compliance |
| 18 | Compliance | GenAI for Policy Management (Policy as Code) | ⚖️ Zero Non-Compliance |
| 19 | Efficiency in Detection & Response | AI-enabled alert triaging and enrichment with context | 🛡️ Zero False Positive |
| 20 | Efficiency in Detection & Response | False positive reduction agent | 🛡️ Zero False Positive |
| 21 | Efficiency in Detection & Response | AI-guided detection and response | 🛡️ Zero False Positive |
| 22 | Efficiency in Detection & Response | AI-powered response playbooks | 🛡️ Zero False Positive |
| 23 | Intelligent IT Security Operations | Integrated tool ecosystem with AI orchestration | ⚙️ Intelligent Ops |
| 24 | Intelligent IT Security Operations | Threat Intel correlation across tools and actionable intel | ⚙️ Intelligent Ops |
| 25 | Intelligent IT Security Operations | AI co-pilot for tool administration (rules, updates, config, license, optimisation) | ⚙️ Intelligent Ops |
| 26 | Intelligent IT Security Operations | Autonomous tool maintenance & optimisation (health, patch, signature, capacity) | ⚙️ Intelligent Ops |

---

## Domain-by-Domain Comparison

### 🎯 Zero MI — `major_incident.py`

| Status | Code Demo Name | JSON Demo Name |
|--------|---------------|---------------|
| ✅ | AI-driven Anomaly Detection & Predictive Analytics | AI-driven Anomaly Detection & Predictive Analytics |
| ✅ | Self-healing and auto-remediation agentic workflow | Self-healing and auto-remediation agentic workflow |
| ✅ | GenAI for Scenario Simulation | GenAI for Scenario Simulation |
| ✅ | GenAI-based Smart Knowledge Assist | GenAI-based Smart Knowledge Assist |
| ✅ | Root Cause Analysis Assistant & Agent | Root Cause Analysis Assistant & Agent |
| ⚠️ MISMATCH | Continuous Monitoring Agents (Health/Security/Configuration **/Anomaly Detection**) | Continuous Monitoring Agents (Health/Security/Configuration/**Anomaly detection**) |

**Issue**: Code has extra space before `/Anomaly` and capitalizes "Detection" vs JSON's lowercase "detection". 
The `get_demo_record` strips all non-alphanumeric chars before matching, so this **still matches** at runtime. ✅ Functional match.

---

### ⚡ Zero Touch — `provisioning.py`

| Status | Code Demo Name | JSON Demo Name |
|--------|---------------|---------------|
| ✅ | End-to-end Incident Automation (Alert→Triage→Ticket→Action) | End-to-end Incident Automation (Alert→Triage→Ticket→Action) |
| ✅ | Self-Service AI Co-pilot for Security tools | Self-Service AI Co-pilot for Security tools |
| ✅ | Device/Application/Identity provisioning agent | Device/Application/Identity provisioning agent |

**Result**: ✅ All 3 demos exactly match.

---

### 🤖 Zero Toil — `automation.py`

| Status | Code Demo Name | JSON Demo Name |
|--------|---------------|---------------|
| ✅ | AI-powered Security tasks automation (log analysis, routine service requests) | AI-powered Security tasks automation (log analysis, routine service requests) |
| ✅ | Security Analysts Co-pilot (reporting, rule writing, correlation, script generation) | Security Analysts Co-pilot (reporting, rule writing, correlation, script generation) |

**Result**: ✅ All 2 demos exactly match.

---

### 🔍 Zero Visibility Gap — `asset_visibility.py`

| Status | Code Demo Name | JSON Demo Name |
|--------|---------------|---------------|
| ✅ | AI-powered continuous asset discovery | AI-powered continuous asset discovery |
| ✅ | Agentic AI to scan address range or cloud accounts non-stop | Agentic AI to scan address range or cloud accounts non-stop |
| ✅ | Context-rich security inventory (ownership, criticality, dependency, config state) | Context-rich security inventory (ownership, criticality, dependency, config state) |
| ✅ | Agentic AI for Shadow IT & Cloud Sprawl | Agentic AI for Shadow IT & Cloud Sprawl |

**Result**: ✅ All 4 demos exactly match.

---

### ⚖️ Zero Non-Compliance — `compliance.py`

| Status | Code Demo Name | JSON Demo Name |
|--------|---------------|---------------|
| ✅ | AI-powered configuration drift detection / continuous compliance monitoring | AI-powered configuration drift detection / continuous compliance monitoring |
| ✅ | Automated configuration drift remediation / self-healing agent | Automated configuration drift remediation / self-healing agent |
| ✅ | GenAI for Policy Management (Policy as Code) | GenAI for Policy Management (Policy as Code) |

**Result**: ✅ All 3 demos exactly match.

---

### 🛡️ Zero False Positive — `detection_response.py`

| Status | Code Demo Name | JSON Demo Name |
|--------|---------------|---------------|
| ✅ | AI-enabled alert triaging and enrichment with context | AI-enabled alert triaging and enrichment with context |
| ✅ | False positive reduction agent | False positive reduction agent |
| ✅ | AI-guided detection and response | AI-guided detection and response |
| ❌ MISMATCH | **AI powered response playbooks** | **AI-powered response playbooks** |

**Issue**: Code is missing the HYPHEN in "AI-powered". The `get_demo_record` fuzzy matcher strips special chars, so it **does match at runtime**. But the display name on the card is technically wrong vs the Excel. **Fix recommended** for exactness.

---

### ⚙️ Intelligent Ops — `secops.py`

| Status | Code Demo Name | JSON Demo Name |
|--------|---------------|---------------|
| ✅ | Integrated tool ecosystem with AI orchestration | Integrated tool ecosystem with AI orchestration |
| ✅ | Threat Intel correlation across tools and actionable intel | Threat Intel correlation across tools and actionable intel |
| ✅ | AI co-pilot for tool administration (rules, updates, config, license, optimisation) | AI co-pilot for tool administration (rules, updates, config, license, optimisation) |
| ✅ | Autonomous tool maintenance & optimisation (health, patch, signature, capacity) | Autonomous tool maintenance & optimisation (health, patch, signature, capacity) |

**Result**: ✅ All 4 demos exactly match.

---

## Summary

| Domain | Tab | Demos in JSON | Demos in Code | Match? |
|--------|-----|--------------|---------------|--------|
| Major Incidents (MI) | 🎯 Zero MI | 6 | 6 | ✅ (minor spacing diff) |
| Time to Provision | ⚡ Zero Touch | 3 | 3 | ✅ |
| Automation Index | 🤖 Zero Toil | 2 | 2 | ✅ |
| Asset Visibility & Coverage | 🔍 Zero Visibility Gap | 4 | 4 | ✅ |
| Compliance | ⚖️ Zero Non-Compliance | 3 | 3 | ✅ |
| Efficiency in Detection & Response | 🛡️ Zero False Positive | 4 | 4 | ⚠️ "AI powered" missing hyphen |
| Intelligent IT Security Operations | ⚙️ Intelligent Ops | 4 | 4 | ✅ |
| **TOTAL** | | **26** | **26** | |

## Issues Found (To Fix)

1. **`detection_response.py` line 33**: `"AI powered response playbooks"` → should be `"AI-powered response playbooks"` (missing hyphen)
2. **`major_incident.py` line 236**: Extra space in `"Configuration /Anomaly Detection"` — functionally OK but cosmetically wrong vs Excel which has `"Configuration/Anomaly detection"`. Low priority.
