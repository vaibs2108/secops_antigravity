import pandas as pd
import random
from datetime import datetime, timedelta

class RAGDataGenerator:
    """Generates synthetic SecOps Knowledge Base and Ticketing Data for the RAG Copilot."""
    
    @staticmethod
    def generate_kedb_entries(count: int = 50) -> pd.DataFrame:
        tools = ["CrowdStrike Falcon", "Splunk Enterprise Security", "Palo Alto Panorama", "AWS GuardDuty", "Microsoft Defender", "Okta", "ServiceNow SecOps"]
        categories = ["Sensor Offline", "Log Ingestion Delayed", "Firewall Rule Commit Failure", "API Throttling", "Definition Update Failed", "SSO Integration Broken", "Webhook Timeout"]
        
        data = []
        for i in range(1, count + 1):
            tool = random.choice(tools)
            category = random.choice(categories)
            error_code = f"ERR-{tool[:3].upper()}-{random.randint(1000, 9999)}"
            
            # Simulated resolutions based on category
            if "Offline" in category:
                resolution = f"Restart the {tool} agent service locally. Verify outbound connectivity on port 443 to cloud broker. Clear local cache in /opt/{tool.lower()}/cache."
            elif "Ingestion" in category:
                resolution = f"Check the heavy forwarder queue throughput. Restart the ingestion pipeline. Verify disk space on the {tool} indexer cluster."
            elif "Firewall" in category:
                resolution = f"Unlock the configuration database. Run 'commit force' from the CLI. Ensure no shadow rules are blocking the NAT translation."
            elif "API" in category:
                resolution = f"Rotate the OAuth token for {tool}. Implement exponential backoff in the SIEM pull script. We are currently hitting the 500 req/min limit."
            elif "Update" in category:
                resolution = f"Force a manual signature sync via the central console. Ensure the host has a valid proxy bypass for *.update.{tool.lower().replace(' ', '')}.com."
            elif "SSO" in category:
                resolution = f"Verify the SAML certificate expiration. Synchronize clock drift between the IdP and the SP. Re-import the metadata XML."
            else:
                resolution = f"Increase the timeout parameter in the webhook configuration from 30s to 120s. Verify the receiving endpoint is returning a 200 OK."
                
            entry = {
                "Document_Type": "KEDB",
                "Tool": tool,
                "Error_Code": error_code,
                "Issue_Description": f"Recurring issue where {tool} experiences {category}.",
                "Known_Resolution": resolution,
                "Last_Updated": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            }
            data.append(entry)
            
        return pd.DataFrame(data)
        
    @staticmethod
    def generate_tickets(count: int = 60) -> pd.DataFrame:
        ticket_types = ["Incident", "Change Request", "Service Request"]
        severities = ["S1 - Critical", "S2 - High", "S3 - Medium", "S4 - Low"]
        
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
                severity = "N/A"
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
                severity = "N/A"
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
                "Ticket_ID": ticket_id,
                "Severity": severity,
                "Description": desc,
                "Resolution_Notes": res,
                "Status": status,
                "Created_Date": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d")
            }
            data.append(entry)
            
        return pd.DataFrame(data)
