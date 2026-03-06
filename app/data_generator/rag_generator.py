import pandas as pd
import random
from datetime import datetime, timedelta

class RAGDataGenerator:
    """Generates synthetic SecOps Knowledge Base and Ticketing Data for the RAG Copilot."""
    
    @staticmethod
    def generate_kedb_entries(count: int = 50) -> pd.DataFrame:
        tools = ["EDR (CrowdStrike)", "SIEM (Splunk)", "WAF (Cloudflare)", "Firewall (Palo Alto)", "Cloud Security (AWS GuardDuty)", "IAM (Okta)", "SOAR (ServiceNow)"]
        
        data = []
        for i in range(1, count + 1):
            tool = random.choice(tools)
            ke_id = f"KE-{str(i).zfill(3)}"
            
            # Simulated resolutions based on tool
            if "CrowdStrike" in tool:
                title = "False Positive on Internal App"
                symptoms = "Endpoint isolation triggered for custom payroll.exe binary."
                cause = "Signature update marked custom signed binary as malicious."
                fix = "Add custom hash/path to Global Exclusion List in Console and release isolation."
            elif "Splunk" in tool:
                title = "Missing Logs from Firewall"
                symptoms = "No logs incoming from Palo Alto firewall."
                cause = "Log forwarder service crashed on syslog server."
                fix = "Restart syslog-ng service on receiver node and verify port 514 UDP."
            elif "Cloudflare" in tool:
                title = "Legitimate Traffic Blocked"
                symptoms = "Users in EMEA receiving 403 Forbidden errors."
                cause = "New WAF rule rate-limiting legitimate proxy IPs."
                fix = "Whitelist ISP proxy IP range or adjust rate limit rules."
            elif "Palo Alto" in tool:
                title = "Commit Failure"
                symptoms = "Unable to commit changes to Panorama."
                cause = "Shadow rule conflict in Device Group."
                fix = "Validate rule hierarchy, delete shadowing rule, and force commit."
            elif "GuardDuty" in tool:
                title = "API Throttling Alert"
                symptoms = "High volume of CloudTrail alerts."
                cause = "Internal script polling AWS API too aggressively."
                fix = "Implement exponential backoff in internal scripts."
            else:
                title = "Authentication Timeout"
                symptoms = "Users unable to access SaaS apps."
                cause = "SAML token expiration drift."
                fix = "Resync NTP clocks across Identity Provider and Service Provider."
                
            entry = {
                "Document_Type": "KEDB",
                "KE ID": ke_id,
                "Tool/System": tool,
                "Error Title": title,
                "Symptoms": symptoms,
                "Known Cause": cause,
                "Workaround/Fix": fix,
                "Last_Updated": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            }
            data.append(entry)
            
        return pd.DataFrame(data)
        
    @staticmethod
    def generate_tickets(count: int = 60) -> pd.DataFrame:
        ticket_types = ["Incident", "Change Request", "Service Request"]
        severities = ["P1 - Critical", "P2 - High", "P3 - Medium", "P4 - Low"]
        
        data = []
        for i in range(1, count + 1):
            t_type = random.choices(ticket_types, weights=[0.5, 0.3, 0.2])[0]
            
            if t_type == "Incident":
                ticket_id = f"INC{random.randint(1000000, 9999999)}"
                severity = random.choices(severities, weights=[0.05, 0.15, 0.4, 0.4])[0]
                desc = random.choice([
                    "User reported ransomware screen on laptop.",
                    "Multiple failed login attempts detected for Admin account.",
                    "High volume of outbound traffic to anomalous IP.",
                    "Endpoint EDR sensor went offline unexpectedly.",
                    "Unauthorized access pattern detected on S3 bucket.",
                    "Phishing email reported by multiple executives.",
                    "Web shell activity detected on DMZ server."
                ])
                res = random.choice([
                    "Isolated host from network. Re-imaged from golden baseline.",
                    "Reset user credentials and enforced MFA token rotation.",
                    "Blocked malicious IP at edge firewall. Updated threat intel feed.",
                    "Restarted sensor service. Upgraded to latest agent version.",
                    "Revoked anomalous IAM role. Reconfigured bucket to private.",
                    "Purged email from all inboxes. Blocked sender domain.",
                    "Quarantined server. Initiated forensic disk image capture."
                ])
                status = random.choice(["Closed", "Resolved", "In Progress"])
            elif t_type == "Change Request":
                ticket_id = f"CHG{random.randint(1000000, 9999999)}"
                severity = "Standard"
                desc = random.choice([
                    "Emergency firewall rule update to block zero-day IOCs.",
                    "Upgrade Splunk indexers to version 9.1.x.",
                    "Deploy new CrowdStrike Falcon sensor via SCCM.",
                    "Modify AWS Security Group to allow internal SIEM traffic.",
                    "Migrate VPN authentication from RADIUS to SAML.",
                    "Update WAF ruleset to block excessive scraping."
                ])
                res = "Change successfully implemented and verified during maintenance window."
                status = "Closed"
            else:
                ticket_id = f"REQ{random.randint(1000000, 9999999)}"
                severity = "Routine"
                desc = random.choice([
                    "Requesting access to the AWS Production Security Group.",
                    "Need a new API key generated for the Threat Intel integration.",
                    "Please whitelist a new vendor IP for SFTP access.",
                    "Need temporary local admin rights for troubleshooting.",
                    "Requesting SIEM dashboard creation for VPN metrics."
                ])
                res = "Request approved by manager and automatically fulfilled by IAM provisioning script."
                status = "Closed"
                
            entry = {
                "Document_Type": t_type,
                "Ticket ID": ticket_id,
                "Priority": severity,
                "Description": desc,
                "Resolution Notes": res,
                "Status": status,
                "Created Date": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d")
            }
            data.append(entry)
            
        return pd.DataFrame(data)
