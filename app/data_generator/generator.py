import pandas as pd
import numpy as np
import uuid
import random
from datetime import datetime, timedelta

class SecurityDataGenerator:
    """
    Generates synthetic realistic security data representing an enterprise environment.
    All data is generated in memory as pandas DataFrames.
    """
    
    def __init__(self):
        self.num_assets = 10000
        self.num_alerts = 20000
        self.num_incidents = 500
        self.num_threat_intel = 1000
        self.start_date = datetime.now() - timedelta(days=30)
        
        # Consistent random seed for reproducible demo if desired, 
        # but requirements imply generating new data on start, so we use current time.
        np.random.seed()
        
    def generate_all(self):
        """
        Orchestrates generation of all datasets and returns them as a dictionary.
        """
        print("Generating synthetic enterprise dataset...")
        assets_df = self.generate_assets()
        alerts_df = self.generate_alerts(assets_df)
        incidents_df = self.generate_incidents(alerts_df)
        patch_df = self.generate_patch_status(assets_df)
        compliance_df = self.generate_compliance()
        intel_df = self.generate_threat_intel()
        admin_df = self.generate_admin_access()
        
        # New datasets requested by AGENTS_final.md
        config_df = self.generate_config_baselines(assets_df)
        identity_df = self.generate_identity_data()
        observability_df = self.generate_observability_data()
        
        # Advanced Datasets for Phase 66
        edr_df = self.generate_edr_telemetry(assets_df)
        playbooks_df = self.generate_playbooks()
        mitre_df = self.generate_threat_models()
        git_df = self.generate_git_logs()
        rca_df = self.generate_rca_documents()
        financial_df = self.generate_financial_data()
        
        # Phase 85: Advanced Compliance Generators
        drift_df = self.generate_config_drift_logs(assets_df)
        policy_df = self.generate_policy_documents()
        iac_df = self.generate_iac_scripts()
        
        # Phase 96: Production-Realistic Vendor Datasets
        cis_fw_baseline_df = self.generate_cis_firewall_baseline()
        firewall_logs_df = self.generate_firewall_logs(assets_df)
        firewall_drift_df = self.generate_firewall_drift()
        access_logs_df = self.generate_access_logs(assets_df)
        dlp_logs_df = self.generate_dlp_logs()
        dlp_policies_df = self.generate_dlp_policies()
        
        return {
            "assets": assets_df,
            "alerts": alerts_df,
            "historical_incidents": incidents_df,
            "patch_status": patch_df,
            "compliance": compliance_df,
            "threat_intel": intel_df,
            "admin_access": admin_df,
            "config_baselines": config_df,
            "identity_data": identity_df,
            "observability_events": observability_df,
            "edr_telemetry": edr_df,
            "playbooks": playbooks_df,
            "threat_models": mitre_df,
            "git_logs": git_df,
            "rca_documents": rca_df,
            "financial_data": financial_df,
            "config_drift_logs": drift_df,
            "policy_documents": policy_df,
            "iac_scripts": iac_df,
            "cis_firewall_baseline": cis_fw_baseline_df,
            "firewall_logs": firewall_logs_df,
            "firewall_drift": firewall_drift_df,
            "access_logs": access_logs_df,
            "dlp_logs": dlp_logs_df,
            "dlp_policies": dlp_policies_df
        }

    def generate_edr_telemetry(self, assets_df):
        """Generates CrowdStrike Falcon-realistic EDR telemetry with SIEM-parsed fields."""
        n = 5000
        ips = assets_df['ip_address'].tolist()
        hostnames = assets_df['hostname'].tolist()
        asset_ids = assets_df['asset_id'].tolist()
        
        event_names = ["ProcessRollup2", "DnsRequest", "NetworkConnect", "FileWrite", 
                       "RegistryWrite", "QueueApcEtw", "SuspiciousCredAccess", "ModuleLoad",
                       "RansomwareActivity", "CreateRemoteThread"]
        platforms = ["Win", "Lin", "Mac"]
        file_paths = [
            "\\\\Device\\\\HarddiskVolume1\\\\Windows\\\\System32\\\\ntdll.dll",
            "\\\\Device\\\\HarddiskVolume1\\\\Windows\\\\System32\\\\vdsldr.exe",
            "\\\\Device\\\\HarddiskVolume1\\\\Windows\\\\System32\\\\cmd.exe",
            "/usr/bin/python3", "/usr/sbin/sshd", "/bin/bash",
            "\\\\Device\\\\HarddiskVolume1\\\\Program Files\\\\CrowdStrike\\\\CSFalconService.exe",
            "\\\\Device\\\\HarddiskVolume1\\\\Windows\\\\System32\\\\powershell.exe",
            "/usr/lib/openssh/sftp-server", "/opt/CrowdStrike/falconctl"
        ]
        config_builds = ["1007.3.0013806.1", "1009.1.0015204.1", "1008.2.0014503.2", "1010.0.0016101.1"]

        data = {
            "event_id": [f"EDR-{str(uuid.uuid4())[:8].upper()}" for _ in range(n)],
            "timestamp": [(self.start_date + timedelta(days=np.random.randint(0, 31), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z" for _ in range(n)],
            "aid": [str(uuid.uuid4())[:12].replace("-", "") for _ in range(n)],
            "cid": [str(uuid.uuid4())[:12].replace("-", "") for _ in range(n)],
            "aip": np.random.choice(ips, size=n),
            "asset_id": np.random.choice(asset_ids, size=n),
            "event_simpleName": np.random.choice(event_names, size=n, p=[0.25, 0.15, 0.15, 0.12, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03]),
            "event_platform": np.random.choice(platforms, size=n, p=[0.7, 0.2, 0.1]),
            "ConfigBuild": np.random.choice(config_builds, size=n),
            "ContextProcessId": [str(uuid.uuid4())[:8] for _ in range(n)],
            "TargetProcessId": [str(np.random.randint(100, 65535)) for _ in range(n)],
            "RawProcessId": [str(np.random.randint(4, 65535)) for _ in range(n)],
            "ConfigStateHash": [str(uuid.uuid4())[:16] for _ in range(n)],
            "Entitlements": np.random.choice(["15", "7", "31", "3"], size=n),
            "ApcContextFileName": np.random.choice(file_paths, size=n),
            "EffectiveTransmissionClass": np.random.choice(["2", "3", "4"], size=n),
            # SIEM-parsed fields (normalized)
            "metadata_vendor_name": ["CrowdStrike"] * n,
            "metadata_product_name": ["Falcon"] * n,
            "principal_hostname": np.random.choice(hostnames, size=n),
            "principal_nat_ip": np.random.choice(ips, size=n),
            "target_process_file_sha256": [uuid.uuid4().hex[:64] for _ in range(n)],
            "target_process_file_full_path": np.random.choice(file_paths, size=n),
            "severity": np.random.choice(["Critical", "High", "Medium", "Low", "Informational"], size=n, p=[0.03, 0.07, 0.20, 0.35, 0.35]),
            "is_malicious": np.random.choice([True, False], size=n, p=[0.04, 0.96])
        }
        return pd.DataFrame(data)

    def generate_playbooks(self):
        data = {
            "playbook_id": [f"PBK-{str(uuid.uuid4())[:6].upper()}" for _ in range(50)],
            "name": ["Isolate Endpoint", "Reset User Password", "Block IP on Firewall", "Revoke AWS Token", "Quarantine File", "Suspend Okta Account"] * 8 + ["Disable VPN Profile", "Reimage Workstation"],
            "automation_engine": np.random.choice(["Cortex XSOAR", "Torq", "Dropzone AI", "ServiceNow SecOps"], size=50),
            "success_rate_pct": np.random.randint(35, 72, size=50),
            "last_updated": [self.start_date - timedelta(days=np.random.randint(10, 100)) for _ in range(50)]
        }
        return pd.DataFrame(data)
        
    def generate_threat_models(self):
        data = {
            "mitre_id": [f"T{np.random.randint(1000, 1600)}" for _ in range(100)],
            "tactic": np.random.choice(["Initial Access", "Execution", "Persistence", "Privilege Escalation", "Defense Evasion", "Credential Access", "Discovery", "Lateral Movement"], size=100),
            "technique_name": np.random.choice(["Phishing", "Valid Accounts", "OS Credential Dumping", "PowerShell", "Scheduled Task", "Remote Desktop Protocol", "Pass the Hash"], size=100),
            "platform": np.random.choice(["Windows", "Linux", "macOS", "AWS", "Azure"], size=100),
            "detection_coverage": np.random.choice(["High", "Medium", "Low"], size=100, p=[0.4, 0.4, 0.2])
        }
        return pd.DataFrame(data)
        
    def generate_git_logs(self):
        data = {
            "commit_id": [str(uuid.uuid4())[:8] for _ in range(500)],
            "timestamp": [self.start_date + timedelta(days=np.random.randint(0, 31), hours=np.random.randint(0, 24)) for _ in range(500)],
            "repository": np.random.choice(["auth-service", "payment-api", "frontend-react", "infra-terraform", "customer-portal"], size=500),
            "developer": [f"dev_{i}@company.com" for i in np.random.randint(1, 50, size=500)],
            "changes": np.random.choice(["Modified 3 files", "Added 1 file, deleted 2", "Modified 15 files", "Changed 1 line"], size=500),
            "passed_sast_scan": np.random.choice([True, False], size=500, p=[0.95, 0.05])
        }
        return pd.DataFrame(data)
        
    def generate_rca_documents(self):
        data = {
            "doc_id": [f"RCA-{np.random.randint(100, 999)}" for _ in range(200)],
            "related_incident": [f"INC-{np.random.randint(1000, 9999)}" for _ in range(200)],
            "root_cause_category": np.random.choice(["Code Defect", "Configuration Error", "Hardware Failure", "Third-Party Outage", "Malicious Attack", "Human Error"], size=200),
            "author": np.random.choice(["L3 Engineering", "SecOps Lead", "SRE Team", "Network Admin"], size=200),
            "mttr_hrs": np.random.uniform(0.5, 48.0, size=200).round(1),
            "status": np.random.choice(["Draft", "Under Review", "Approved", "Published to KEDB"], size=200, p=[0.1, 0.2, 0.3, 0.4])
        }
        return pd.DataFrame(data)

    def generate_cis_firewall_baseline(self):
        """Generates CIS Benchmark firewall baseline rules (200 rules)."""
        benchmarks = [
            ("CIS Oracle Linux 8", "3.0.0"), ("CIS AlmaLinux 8", "3.0.0"),
            ("CIS Windows Server 2022", "2.0.0"), ("CIS Ubuntu 22.04", "1.0.0"),
            ("CIS Palo Alto Firewall 10", "1.1.0"), ("CIS Cisco ASA 9", "4.1.0")
        ]
        rules = [
            ("cis-ssh-5.2.1", "Ensure SSH Protocol is set to 2", "2"),
            ("cis-audit-4.1", "Ensure auditing for processes that start prior to auditd", "1"),
            ("cis-fw-3.5.1", "Ensure default deny firewall policy", "deny"),
            ("cis-pass-5.4.1", "Ensure password expiration is 365 days or less", "365"),
            ("cis-log-4.2.1", "Ensure rsyslog or syslog-ng is configured", "enabled"),
            ("cis-net-3.1.1", "Ensure IP forwarding is disabled", "0"),
            ("cis-net-3.2.2", "Ensure ICMP redirects are not accepted", "0"),
            ("cis-ssh-5.2.11", "Ensure SSH MaxAuthTries is set to 4 or less", "4"),
            ("cis-ssh-5.2.13", "Ensure only strong ciphers are used", "aes256-ctr,aes192-ctr"),
            ("cis-fw-3.5.2", "Ensure loopback traffic is configured", "accept"),
            ("cis-auth-5.3.1", "Ensure password hashing algorithm is SHA-512", "sha512"),
            ("cis-kern-1.5.1", "Ensure core dumps are restricted", "0"),
            ("cis-time-2.2.1", "Ensure NTP is configured with authorized server", "pool.ntp.org"),
            ("cis-perm-6.1.2", "Ensure permissions on /etc/shadow are 640", "640"),
            ("cis-fw-3.5.3", "Ensure outbound established connections configured", "accept"),
            ("cis-net-3.2.1", "Ensure source routed packets are not accepted", "0"),
            ("cis-ssh-5.2.5", "Ensure SSH LogLevel is set to INFO", "INFO"),
            ("cis-mnt-1.1.3", "Ensure nodev option set on /tmp partition", "nodev"),
            ("cis-acc-5.4.4", "Ensure default user umask is 027", "027"),
            ("cis-srv-2.1.1", "Ensure xinetd is not installed", "not_installed"),
        ]
        data = []
        for _ in range(200):
            bm_name, bm_ver = benchmarks[np.random.randint(0, len(benchmarks))]
            rule_id, rule_name, expected_val = rules[np.random.randint(0, len(rules))]
            section = rule_id.split("-")[1]
            data.append({
                "rule_id": rule_id,
                "benchmark_name": bm_name,
                "benchmark_version": bm_ver,
                "section": section,
                "rule_name": rule_name,
                "expected_value": expected_val,
                "severity": np.random.choice(["Critical", "High", "Medium"], p=[0.2, 0.5, 0.3]),
                "cis_control_id": f"CIS-{np.random.randint(1, 18)}.{np.random.randint(1, 12)}"
            })
        return pd.DataFrame(data)

    def generate_firewall_logs(self, assets_df):
        """Generates 10K firewall log entries in structured Syslog/CEF format."""
        n = 10000
        ips = assets_df['ip_address'].tolist()
        fw_hostnames = [f"fw-{loc}-{i:02d}.acme.local" for loc in ["prod", "dmz", "edge", "dc"] for i in range(1, 6)]
        vendors = ["ACME_FW", "PAN_FW", "CISCO_ASA", "FORTI_FW"]
        zones = ["internal", "dmz", "external", "guest", "management", "trust", "untrust"]
        protocols = ["TCP", "UDP", "ICMP", "HTTPS", "DNS", "SSH", "RDP"]
        data = {
            "log_id": [f"FW-{str(uuid.uuid4())[:8].upper()}" for _ in range(n)],
            "timestamp": [(self.start_date + timedelta(days=np.random.randint(0, 31), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60), seconds=np.random.randint(0, 60))).strftime('%Y-%m-%dT%H:%M:%SZ') for _ in range(n)],
            "firewall_hostname": np.random.choice(fw_hostnames, size=n),
            "firewall_vendor": np.random.choice(vendors, size=n, p=[0.3, 0.3, 0.2, 0.2]),
            "action": np.random.choice(["allow", "deny", "drop", "reject"], size=n, p=[0.65, 0.20, 0.10, 0.05]),
            "src_ip": np.random.choice(ips, size=n),
            "dst_ip": [f"10.{np.random.randint(0, 255)}.{np.random.randint(0, 255)}.{np.random.randint(1, 254)}" for _ in range(n)],
            "src_port": np.random.randint(1024, 65535, size=n),
            "dst_port": np.random.choice([22, 80, 443, 3389, 8080, 53, 25, 445, 3306, 5432, 8443], size=n),
            "protocol": np.random.choice(protocols, size=n, p=[0.35, 0.15, 0.05, 0.20, 0.10, 0.08, 0.07]),
            "rule_id": [f"rule_{np.random.randint(1000, 9999)}" for _ in range(n)],
            "zone_in": np.random.choice(zones, size=n),
            "zone_out": np.random.choice(zones, size=n),
            "session_id": [f"0x{uuid.uuid4().hex[:8]}" for _ in range(n)],
            "bytes_sent": np.random.randint(64, 1500000, size=n),
            "bytes_received": np.random.randint(64, 500000, size=n),
        }
        return pd.DataFrame(data)

    def generate_firewall_drift(self):
        """Generates 500 firewall configuration drift records (baseline vs running)."""
        config_items = [
            ("SSH Access Rule (Port 22)", "deny from 0.0.0.0/0", ["allow from 172.16.10.0/24", "allow from 0.0.0.0/0", "allow from 10.0.0.0/8"], "Security Policy Change"),
            ("Logging Profile", "Log at Session End", ["Log at Session Start", "Disabled", "Log at Session Start and End"], "Audit Policy Change"),
            ("Admin Access", "HTTPS from 192.168.1.10/32", ["HTTPS from 10.0.0.0/8", "HTTPS from 0.0.0.0/0", "HTTP from 10.0.0.0/8"], "Access Control Change"),
            ("Dormant Rule Status", "disabled", ["enabled", "enabled (shadow)", "enabled (orphaned)"], "Shadow Rule"),
            ("TLS Minimum Version", "TLS 1.2", ["TLS 1.0", "TLS 1.1", "SSL 3.0"], "Encryption Policy Change"),
            ("Outbound DNS Rule", "allow to 10.1.1.53 only", ["allow to any", "allow to 8.8.8.8", "allow to 1.1.1.1"], "DNS Policy Change"),
            ("ICMP Policy", "deny all ICMP", ["allow ICMP echo", "allow all ICMP", "allow ICMP from internal"], "Network Policy Change"),
            ("Password Complexity", "min 14 chars + special", ["min 8 chars", "min 12 chars", "no requirement"], "Authentication Change"),
            ("Session Timeout", "300 seconds", ["600 seconds", "900 seconds", "0 (disabled)"], "Session Policy Change"),
            ("IPS Profile", "strict (block all high/critical)", ["moderate (alert only)", "disabled", "default"], "Threat Prevention Change"),
        ]
        justifications = [
            "Developer network was temporarily permitted SSH access to debug an issue.",
            "Changed for more verbose troubleshooting but not reverted to baseline.",
            "Management interface was inadvertently opened to the entire corporate network.",
            "Rule is disabled in baseline but was found enabled in production.",
            "Legacy application requires older TLS version for compatibility.",
            "DNS resolution changed to external provider during ISP outage, never reverted.",
            "Network team enabled ICMP for monitoring but forgot to disable.",
            "Relaxed during onboarding sprint, not reverted per change management.",
            "Extended timeout for long-running API calls, not approved by security.",
            "IPS profile downgraded after false positive complaints, never restored.",
        ]
        fw_hostnames = [f"fw-{loc}-{i:02d}.acme.local" for loc in ["prod", "dmz", "edge", "dc"] for i in range(1, 4)]
        data = []
        for _ in range(500):
            idx = np.random.randint(0, len(config_items))
            item, baseline, running_opts, drift_type = config_items[idx]
            running_val = np.random.choice(running_opts)
            risk = "Critical" if drift_type in ("Access Control Change", "Encryption Policy Change", "Threat Prevention Change") else np.random.choice(["High", "Medium", "Low"], p=[0.5, 0.35, 0.15])
            data.append({
                "drift_id": f"FWD-{str(uuid.uuid4())[:8].upper()}",
                "firewall_hostname": np.random.choice(fw_hostnames),
                "configuration_item": item,
                "baseline_value": baseline,
                "current_running_value": running_val,
                "drift_type": drift_type,
                "risk_level": risk,
                "justification": justifications[idx],
                "cis_rule_ref": f"cis-{config_items[idx][0][:3].lower()}-{np.random.randint(1,9)}.{np.random.randint(1,15)}",
                "detected_timestamp": (self.start_date + timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d %H:%M')
            })
        return pd.DataFrame(data)

    def generate_access_logs(self, assets_df):
        """Generates 8K access log entries in Apache Combined Log Format (CLF) structure."""
        n = 8000
        ips = assets_df['ip_address'].tolist()
        users = [f"user_{i}" for i in range(1, 100)] + ["jdoe", "admin", "svc_account_1", "svc_account_2", "api_health_check", "backup_agent", "-"]
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
        endpoints = [
            "/api/v1/customers/{id}", "/api/v1/payments/{id}", "/api/v1/users/{id}",
            "/admin/config", "/admin/users", "/admin/logs", "/admin/backup",
            "/auth/login", "/auth/logout", "/auth/token/refresh",
            "/api/v1/reports/financial", "/api/v1/inventory/{id}",
            "/health", "/metrics", "/api/v1/orders/{id}",
            "/api/v1/employees/{id}", "/api/internal/debug", "/api/v1/exports/csv"
        ]
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1",
            "python-requests/2.31.0", "curl/8.4.0",
            "PostmanRuntime/7.35.0", "Apache-HttpClient/4.5.14",
        ]
        data = {
            "log_id": [f"ACC-{str(uuid.uuid4())[:8].upper()}" for _ in range(n)],
            "timestamp": [(self.start_date + timedelta(days=np.random.randint(0, 31), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60), seconds=np.random.randint(0, 60))).strftime('%d/%b/%Y:%H:%M:%S +0000') for _ in range(n)],
            "client_ip": np.random.choice(ips, size=n),
            "user": np.random.choice(users, size=n),
            "method": np.random.choice(methods, size=n, p=[0.50, 0.25, 0.10, 0.05, 0.05, 0.05]),
            "endpoint": [ep.replace("{id}", str(np.random.randint(10000, 99999))) for ep in np.random.choice(endpoints, size=n)],
            "http_version": np.random.choice(["HTTP/1.1", "HTTP/2.0"], size=n, p=[0.7, 0.3]),
            "status_code": np.random.choice([200, 201, 301, 400, 401, 403, 404, 500, 502, 503], size=n, p=[0.55, 0.08, 0.04, 0.05, 0.08, 0.05, 0.06, 0.04, 0.03, 0.02]),
            "response_bytes": np.random.randint(100, 50000, size=n),
            "user_agent": np.random.choice(user_agents, size=n),
        }
        return pd.DataFrame(data)

    def generate_dlp_logs(self):
        """Generates 2K DLP incident logs in Zscaler Endpoint DLP export format."""
        n = 2000
        policies = ["ZDP", "PCI-DSS-Monitor", "HIPAA-PHI-Watch", "IP-Protection", "GDPR-PII", "Internal-Code-Leak"]
        users = [f"user_{i}@acme.com" for i in range(1, 80)]
        file_types = ["txt", "csv", "xlsx", "pdf", "doc", "pptx", "zip", "json", "py", "sql"]
        channels = ["Email", "USB Transfer", "Cloud Upload", "Network Drive Transfer", "Browser Upload", "Clipboard", "Print"]
        data_patterns = [
            "Credit Card Numbers (5 or more)", "Social Security Numbers",
            "Medical Record IDs", "API Keys / Secrets", "Source Code (proprietary)",
            "Employee PII (names + SSN)", "Financial Statements", "Customer Email Addresses",
            "Passport Numbers", "Bank Account Numbers"
        ]
        dlp_rules = [
            "Credit Cards: Detect leakage of credit card information",
            "SSN: Detect Social Security Number exposure",
            "PHI: Protected Health Information detection",
            "Secrets: API key and credential leak detection",
            "Code: Proprietary source code exfiltration",
            "PII: Personally Identifiable Information bundle",
        ]
        data = {
            "event_id": [f"DLP-{str(uuid.uuid4())[:8].upper()}" for _ in range(n)],
            "timestamp": [(self.start_date + timedelta(days=np.random.randint(0, 31), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))).strftime('%Y-%m-%d %H:%M:%S') for _ in range(n)],
            "policy_name": np.random.choice(policies, size=n),
            "user": np.random.choice(users, size=n),
            "file_type": np.random.choice(file_types, size=n),
            "file_hash": [uuid.uuid4().hex[:32] for _ in range(n)],
            "dlp_rule": np.random.choice(dlp_rules, size=n),
            "match_count": np.random.choice([1, 2, 3, 5, 10, 15, 25, 50], size=n),
            "data_pattern": np.random.choice(data_patterns, size=n),
            "channel": np.random.choice(channels, size=n),
            "action": np.random.choice(["Block", "Confirm Allow", "Log Only", "Quarantine", "Encrypt"], size=n, p=[0.35, 0.20, 0.25, 0.10, 0.10]),
            "severity": np.random.choice(["Critical", "High", "Medium", "Low"], size=n, p=[0.10, 0.30, 0.40, 0.20]),
        }
        return pd.DataFrame(data)

    def generate_dlp_policies(self):
        """Generates 50 DLP policy/sensor configuration entries in Fortinet FortiOS style."""
        sensors = [
            ("PCI-DSS-Sensor", "Block credit card uploads"),
            ("HIPAA-PHI-Sensor", "Block protected health information"),
            ("GDPR-PII-Sensor", "Block EU personal data transfers"),
            ("IP-Code-Sensor", "Block proprietary code exfiltration"),
            ("Financial-Sensor", "Monitor financial statement leaks"),
            ("API-Key-Sensor", "Block API credentials in uploads"),
            ("Customer-Data-Sensor", "Block customer PII exports"),
        ]
        filter_names = ["blockCC", "blockPHI", "blockPII", "blockCode", "monitorFinancial", "blockSecrets", "blockExports"]
        protocols = ["https", "http", "smtp", "ftp", "smb", "any"]
        filter_types = ["file-type", "file-size", "fingerprint", "watermark", "archive"]
        file_type_sets = ["txt, doc, pdf", "xlsx, csv, json", "py, java, cpp, go", "zip, tar, gz", "pptx, pdf, doc", "any"]
        sensitivity_names = ["credit_card", "ssn", "medical_id", "api_key", "source_code", "financial_statement", "pii_bundle"]
        data = []
        for _ in range(50):
            s_name, s_comment = sensors[np.random.randint(0, len(sensors))]
            data.append({
                "sensor_id": f"DLP-CFG-{str(uuid.uuid4())[:6].upper()}",
                "sensor_name": s_name,
                "comment": s_comment,
                "filter_name": np.random.choice(filter_names),
                "filter_action": np.random.choice(["block", "log-only", "quarantine", "encrypt"], p=[0.50, 0.25, 0.15, 0.10]),
                "protocol": np.random.choice(protocols),
                "filter_type": np.random.choice(filter_types),
                "file_types": np.random.choice(file_type_sets),
                "sensitivity_name": np.random.choice(sensitivity_names),
                "match_criteria": np.random.choice(["or", "and"]),
                "status": np.random.choice(["enabled", "disabled", "test_mode"], p=[0.75, 0.10, 0.15]),
            })
        return pd.DataFrame(data)

    def generate_assets(self):
        """
        Generate 10k+ asset records with varying types and agent coverage.
        """
        
        # Helper to generate realistic internal IPs
        ips = [f"10.{np.random.randint(0, 255)}.{np.random.randint(0, 255)}.{np.random.randint(1, 254)}" for _ in range(self.num_assets)]
        oses = np.random.choice(["Windows", "Linux", "macOS"], size=self.num_assets, p=[0.7, 0.2, 0.1])
        
        # Helper to generate hostnames
        hostnames = []
        for os_type in oses:
            prefix = "WIN" if os_type == "Windows" else "SRV" if os_type == "Linux" else "MAC"
            hostnames.append(f"{prefix}-{str(uuid.uuid4())[:6].upper()}")
            
        data = {
            "asset_id": [f"AST-{str(uuid.uuid4())[:8].upper()}" for _ in range(self.num_assets)],
            "hostname": hostnames,
            "ip_address": ips,
            "type": np.random.choice(["endpoint", "server", "cloud_workload", "mobile", "network_device"], 
                                     size=self.num_assets, p=[0.6, 0.2, 0.15, 0.03, 0.02]),
            "os": oses,
            "criticality": np.random.choice(["High", "Medium", "Low"], size=self.num_assets, p=[0.1, 0.3, 0.6]),
            "cmdb_source": np.random.choice(["ServiceNow CMDB", "Device42", "Manual", "Lansweeper"], size=self.num_assets, p=[0.6, 0.2, 0.1, 0.1]),
            "telemetry_source": np.random.choice(["Gigamon NetFlow", "CrowdStrike Falcon", "AWS VPC Flow", "Palo Alto Logs"], size=self.num_assets, p=[0.3, 0.4, 0.2, 0.1]),
            # Enterprise under stress — significant visibility and coverage gaps
            "has_edr": np.random.choice([True, False], size=self.num_assets, p=[0.52, 0.48]),
            "has_config_management": np.random.choice([True, False], size=self.num_assets, p=[0.45, 0.55]),
            "last_seen": [self.start_date + timedelta(days=np.random.randint(20, 31), hours=np.random.randint(0, 24)) for _ in range(self.num_assets)]
        }
        return pd.DataFrame(data)

    def generate_alerts(self, assets_df):
        """
        Generate 20k+ alert records associated to assets.
        """
        asset_ids = assets_df['asset_id'].tolist()
        
        data = {
            "alert_id": [f"ALT-{str(uuid.uuid4())[:8].upper()}" for _ in range(self.num_alerts)],
            "timestamp": [self.start_date + timedelta(days=np.random.randint(0, 31), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60)) for _ in range(self.num_alerts)],
            "asset_id": np.random.choice(asset_ids, size=self.num_alerts),
            "severity": np.random.choice(["Critical", "High", "Medium", "Low"], size=self.num_alerts, p=[0.05, 0.15, 0.3, 0.5]),
            "rule_name": np.random.choice([
                "Suspicious Process Execution", "Multiple Failed Logins", "Malware Detected", 
                "Unusual Network Traffic", "Lateral Movement Suspected", "Privilege Escalation",
                "Phishing Link Clicked", "Ransomware Behavior"
            ], size=self.num_alerts),
            "status": np.random.choice(["New", "In Progress", "Closed"], size=self.num_alerts, p=[0.7, 0.1, 0.2]),
            # ~60% false positive rate overall, weighted towards lower severities practically, but random here
            "is_false_positive": np.random.choice([True, False], size=self.num_alerts, p=[0.72, 0.28])
        }
        return pd.DataFrame(data).sort_values("timestamp").reset_index(drop=True)

    def generate_incidents(self, alerts_df):
        """
        Generate 500+ incidents linked to assets with deliberate recurring patterns.
        ~15% of incidents are concentrated on 20 'hot assets' to simulate real-world repeat offenders.
        """
        asset_ids_from_alerts = alerts_df['asset_id'].unique().tolist()
        
        # Create a pool of 20 "problematic" assets that will have recurring incidents
        hot_assets = np.random.choice(asset_ids_from_alerts, size=min(20, len(asset_ids_from_alerts)), replace=False).tolist()
        
        root_causes = [
            "Misconfigured Firewall Rule", "Unpatched CVE Vulnerability", "Stale Service Account Credentials",
            "Memory Leak in Application", "DNS Misconfiguration", "Certificate Expiration",
            "Disk Space Exhaustion", "Third-Party API Timeout", "Malware Persistence Mechanism",
            "Unauthorized Configuration Change", "Load Balancer Health Check Failure", "Database Connection Pool Exhaustion",
            "SSH Key Rotation Failure", "Ransomware Lateral Movement", "Privilege Escalation Exploit"
        ]
        
        services = [
            "auth-service", "payment-api", "customer-portal", "inventory-service", "email-gateway",
            "vpn-concentrator", "dns-resolver", "ad-controller", "backup-service", "monitoring-agent"
        ]
        
        # Generate asset assignments — 15% on hot assets (recurring), rest random
        incident_assets = []
        for _ in range(self.num_incidents):
            if np.random.random() < 0.15:
                incident_assets.append(np.random.choice(hot_assets))
            else:
                incident_assets.append(np.random.choice(asset_ids_from_alerts))
        
        data = {
            "incident_id": [f"INC-{str(uuid.uuid4())[:8].upper()}" for _ in range(self.num_incidents)],
            "timestamp": [self.start_date + timedelta(days=np.random.randint(0, 31), hours=np.random.randint(0, 24)) for _ in range(self.num_incidents)],
            "asset_id": incident_assets,
            "severity": np.random.choice(["Critical", "High", "Medium", "Low"], size=self.num_incidents, p=[0.02, 0.08, 0.4, 0.5]),
            "status": np.random.choice(["New", "In Progress", "Resolved", "Closed"], size=self.num_incidents, p=[0.1, 0.3, 0.2, 0.4]),
            "is_major_incident": np.random.choice([True, False], size=self.num_incidents, p=[0.12, 0.88]),
            "root_cause_category": np.random.choice(root_causes, size=self.num_incidents),
            "affected_service": np.random.choice(services, size=self.num_incidents),
            "time_to_detect_hrs": np.random.exponential(scale=6, size=self.num_incidents),
            "time_to_resolve_hrs": np.random.exponential(scale=28, size=self.num_incidents)
        }
        
        # Generate some linked alerts
        alert_ids = alerts_df['alert_id'].tolist()
        linked_alerts = []
        for _ in range(self.num_incidents):
            num_links = np.random.randint(1, 15)
            linked_alerts.append(", ".join(np.random.choice(alert_ids, size=num_links)))
        
        data["linked_alerts"] = linked_alerts
        return pd.DataFrame(data).sort_values("timestamp").reset_index(drop=True)

    def generate_patch_status(self, assets_df):
        """
        Generate patch status details for assets.
        ~85% compliant, ~15% missing patches.
        """
        asset_ids = assets_df['asset_id'].tolist()
        
        data = {
            "asset_id": asset_ids,
            "is_compliant": np.random.choice([True, False], size=self.num_assets, p=[0.48, 0.52]),
            "critical_missing_patches": np.zeros(self.num_assets, dtype=int)
        }
        
        df = pd.DataFrame(data)
        
        # Inject missing patch counts into non-compliant systems
        mask = df['is_compliant'] == False
        non_compliant_count = df[mask].shape[0]
        df.loc[mask, 'critical_missing_patches'] = np.random.randint(1, 10, size=non_compliant_count)
        
        return df

    def generate_compliance(self):
        """
        Organization-wide baseline compliance data. Note: We use synthetic metric distributions here directly.
        """
        return pd.DataFrame({
            "metric": ["MFA Registration", "Conditional Access Coverage", "CIS Baseline Compliance"],
            "value_percentage": [61.3, 44.8, 42.1]
        })

    def generate_threat_intel(self):
        """
        Generate threat intel indicators.
        """
        data = {
            "indicator_id": [f"IOC-{str(uuid.uuid4())[:8].upper()}" for _ in range(self.num_threat_intel)],
            "type": np.random.choice(["IP", "Domain", "File Hash", "URL"], size=self.num_threat_intel, p=[0.4, 0.3, 0.2, 0.1]),
            "value": [f"indicator-val-{i}" for i in range(self.num_threat_intel)],
            "severity": np.random.choice(["High", "Medium"], size=self.num_threat_intel, p=[0.4, 0.6]),
            "mitre_technique": np.random.choice([
                "T1059", "T1078", "T1053", "T1110", "T1003", "T1566", "T1105", "T1055"
            ], size=self.num_threat_intel),
            "intelligence_source": np.random.choice(["Recorded Future", "CrowdStrike Falcon", "MISP", "Internal ISAC"], size=self.num_threat_intel, p=[0.4, 0.4, 0.1, 0.1]),
            "confidence": np.random.randint(50, 100, size=self.num_threat_intel)
        }
        return pd.DataFrame(data)

    def generate_admin_access(self):
        """
        Admin access logs representing PAM usage.
        """
        num_sessions = 5000
        data = {
            "session_id": [f"PAM-{str(uuid.uuid4())[:8].upper()}" for _ in range(num_sessions)],
            "user_id": [f"admin_{np.random.randint(1, 50)}" for _ in range(num_sessions)],
            "timestamp": [self.start_date + timedelta(days=np.random.randint(0, 31), hours=np.random.randint(0, 24)) for _ in range(num_sessions)],
            "target_system": [f"server_core_{np.random.randint(1, 100)}" for _ in range(num_sessions)],
            "requires_mfa": np.random.choice([True, False], size=num_sessions, p=[0.61, 0.39]),
            "is_just_in_time": np.random.choice([True, False], size=num_sessions, p=[0.32, 0.68])
        }
        return pd.DataFrame(data).sort_values("timestamp").reset_index(drop=True)

    def generate_config_baselines(self, assets_df):
        """
        Generate 10k+ configuration baseline records.
        """
        asset_ids = assets_df['asset_id'].tolist()
        data = {
            "config_id": [f"CFG-{str(uuid.uuid4())[:8].upper()}" for _ in range(self.num_assets)],
            "asset_id": asset_ids,
            "baseline_framework": np.random.choice(["CIS v8", "NIST 800-53", "PCI-DSS"], size=self.num_assets, p=[0.6, 0.3, 0.1]),
            "last_scan_date": [self.start_date + timedelta(days=np.random.randint(15, 31)) for _ in range(self.num_assets)],
            "is_compliant": np.random.choice([True, False], size=self.num_assets, p=[0.42, 0.58]) # ~42% target
        }
        
        df = pd.DataFrame(data)
        
        # Add drift metrics for non-compliant
        mask = df['is_compliant'] == False
        non_compliant_count = df[mask].shape[0]
        df.loc[mask, 'drift_items_count'] = np.random.randint(1, 8, size=non_compliant_count)
        df['drift_items_count'] = df['drift_items_count'].fillna(0).astype(int)
        
        return df

    def generate_identity_data(self):
        """
        Generate 10k+ Identity user accounts and MFA/Conditional Access states.
        """
        num_identities = 12000
        data = {
            "user_id": [f"USR-{str(uuid.uuid4())[:8].upper()}" for _ in range(num_identities)],
            "department": np.random.choice(["Engineering", "Sales", "HR", "Finance", "Operations", "Executive"], size=num_identities),
            "hr_source_system": np.random.choice(["Workday", "BambooHR", "ADP", "Microsoft Entra ID"], size=num_identities, p=[0.6, 0.2, 0.1, 0.1]),
            "is_active": np.random.choice([True, False], size=num_identities, p=[0.95, 0.05]),
            "mfa_registered": np.random.choice([True, False], size=num_identities, p=[0.61, 0.39]), # ~61% target
            "conditional_access_enforced": np.random.choice([True, False], size=num_identities, p=[0.45, 0.55]), # ~44.8% target
            "risk_level": np.random.choice(["Low", "Medium", "High"], size=num_identities, p=[0.9, 0.08, 0.02]),
            "last_login": [self.start_date + timedelta(days=np.random.randint(20, 31)) for _ in range(num_identities)]
        }
        return pd.DataFrame(data)

    def generate_observability_data(self):
        """
        Generate 20k+ deep observability records (Network Flows, Packets, Logs, Traces).
        """
        num_events = 20000
        data = {
            "event_id": [f"EVT-{str(uuid.uuid4())[:8].upper()}" for _ in range(num_events)],
            "timestamp": [self.start_date + timedelta(days=np.random.randint(0, 31), hours=np.random.randint(0, 24)) for _ in range(num_events)],
            "event_type": np.random.choice(["Network Flow", "Packet Inspection", "Application Trace", "System Log", "API Access"], size=num_events, p=[0.4, 0.2, 0.15, 0.15, 0.1]),
            "source_ip": [f"10.{np.random.randint(0, 255)}.{np.random.randint(0, 255)}.{np.random.randint(1, 254)}" for _ in range(num_events)],
            "dest_ip": [f"10.{np.random.randint(0, 255)}.{np.random.randint(0, 255)}.{np.random.randint(1, 254)}" for _ in range(num_events)],
            "protocol": np.random.choice(["TCP", "UDP", "HTTPS", "DNS", "SSH", "RDP"], size=num_events),
            "bytes_transferred": np.random.randint(100, 5000000, size=num_events),
            "anomaly_score": np.random.randint(1, 100, size=num_events),
        }
        return pd.DataFrame(data).sort_values("timestamp").reset_index(drop=True)

    def generate_financial_data(self):
        """Generates synthetic corporate spend data for Shadow IT discovery."""
        data = []
        vendors = ["AWS", "Azure", "GCP", "Salesforce", "Dropbox", "Slack", "Zoom", "Github", "Notion", "Miro", "Adobe", "Canva", "Monday.com"]
        departments = ["IT", "Sales", "Marketing", "HR", "Engineering", "Design", "Legal", "Finance"]
        
        for _ in range(200):
            vendor = np.random.choice(vendors)
            dept = np.random.choice(departments)
            amount = round(np.random.uniform(10.0, 5000.0), 2)
            timestamp = self.start_date + timedelta(days=np.random.randint(0, 30))
            is_sanctioned = np.random.choice([True, False], p=[0.7, 0.3])
            
            data.append({
                "transaction_id": str(uuid.uuid4())[:8].upper(),
                "timestamp": timestamp.strftime('%Y-%m-%d %H:%M'),
                "vendor": vendor,
                "department": dept,
                "amount": f"${amount}",
                "transaction_type": "Corporate Card" if amount < 1000 else "Purchase Order",
                "status": "Approved" if is_sanctioned else "Pending Audit",
                "compliance_flag": "Green" if is_sanctioned else "High Risk (Shadow IT)"
            })
        return pd.DataFrame(data)

    def generate_config_drift_logs(self, assets_df):
        """Generates explicit desired state vs actual state comparisons for Compliance Demos."""
        asset_ids = assets_df['asset_id'].tolist()
        data = []
        for _ in range(500):
            target = np.random.choice(["Public Cloud IAM", "S3/Storage Buckets", "Kubernetes RBAC", "Network Security Groups", "Endpoint Registry"])
            desired_state = np.random.choice(["Block Public Access", "Require MFA", "Port 22 Closed", "TLS 1.2 Minimum", "Restrict Admin Token"])
            actual_state = np.random.choice(["Public Access Allowed", "MFA Bypassed", "Port 22 Open (0.0.0.0/0)", "TLS 1.0 Enabled", "Token Exposed"])
            data.append({
                "drift_id": f"DRF-{str(uuid.uuid4())[:8].upper()}",
                "timestamp": (self.start_date + timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d %H:%M'),
                "asset_id": np.random.choice(asset_ids),
                "monitoring_target": target,
                "desired_state": desired_state,
                "actual_state": actual_state,
                "regulatory_impact": np.random.choice(["CIS v8", "NIST 800-53", "PCI-DSS", "HIPAA", "SOX"]),
                "deviation_severity": np.random.choice(["High", "Critical"])
            })
        return pd.DataFrame(data)

    def generate_policy_documents(self):
        """Generates human-readable compliance PDFs and written policies metadata."""
        data = []
        policies = ["Data Retention Policy", "Access Control Standard", "Cloud Security Benchmark", "Vendor Risk Policy", "Cryptography Standard"]
        for i in range(25):
            data.append({
                "doc_id": f"POL-{str(uuid.uuid4())[:6].upper()}",
                "policy_name": np.random.choice(policies) + f" v{np.random.randint(1, 5)}.0",
                "format": "PDF Document",
                "status": "Published",
                "last_reviewed": (self.start_date - timedelta(days=np.random.randint(30, 365))).strftime('%Y-%m-%d'),
                "extract": "All assets must employ multi-factor authentication and AES-256 encryption at rest."
            })
        return pd.DataFrame(data)

    def generate_iac_scripts(self):
        """Generates Target IaC code snippets (Terraform, Rego...) for Automated Remediation."""
        data = []
        files = ["main.tf", "s3_bucket.tf", "security_group.tf", "rbac.rego", "auth_policy.rego", "iam_baseline.bicep"]
        for _ in range(50):
            data.append({
                "script_id": f"IAC-{str(uuid.uuid4())[:6].upper()}",
                "file_name": np.random.choice(files),
                "language": np.random.choice(["Terraform (HCL)", "Open Policy Agent (Rego)", "AWS CloudFormation", "Azure Bicep"]),
                "associated_tool_api": np.random.choice(["AWS EC2 API", "Kubernetes API", "Azure Resource Manager", "Prisma Cloud API"]),
                "remediation_action": "Enforce desired configuration baseline",
                "last_commit": (self.start_date - timedelta(days=np.random.randint(1, 15))).strftime('%Y-%m-%d')
            })
        return pd.DataFrame(data)

if __name__ == "__main__":
    import time
    start = time.time()
    generator = SecurityDataGenerator()
    dataset = generator.generate_all()
    end = time.time()
    
    print(f"Dataset generated in {end - start:.2f} seconds.")
    for key, df in dataset.items():
        print(f" - {key}: {len(df)} records")

