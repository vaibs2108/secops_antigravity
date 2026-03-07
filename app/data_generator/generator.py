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
        
        return {
            "assets": assets_df,
            "alerts": alerts_df,
            "incidents": incidents_df,
            "patch_status": patch_df,
            "compliance": compliance_df,
            "threat_intel": intel_df,
            "security_tools": admin_df, # Retaining PAM table format but renaming to fit bundle
            "config_baselines": config_df,
            "identity_data": identity_df
        }
        
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
            # 85% coverage for EDR, 92% for config management
            "has_edr": np.random.choice([True, False], size=self.num_assets, p=[0.85, 0.15]),
            "has_config_management": np.random.choice([True, False], size=self.num_assets, p=[0.92, 0.08]),
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
            "is_false_positive": np.random.choice([True, False], size=self.num_alerts, p=[0.6, 0.4])
        }
        return pd.DataFrame(data).sort_values("timestamp").reset_index(drop=True)

    def generate_incidents(self, alerts_df):
        """
        Generate 500+ incidents. An incident is a collection of correlated alerts, investigated in SOC.
        """
        data = {
            "incident_id": [f"INC-{str(uuid.uuid4())[:8].upper()}" for _ in range(self.num_incidents)],
            "timestamp": [self.start_date + timedelta(days=np.random.randint(0, 31), hours=np.random.randint(0, 24)) for _ in range(self.num_incidents)],
            "severity": np.random.choice(["Critical", "High", "Medium", "Low"], size=self.num_incidents, p=[0.02, 0.08, 0.4, 0.5]),
            "status": np.random.choice(["New", "In Progress", "Resolved", "Closed"], size=self.num_incidents, p=[0.1, 0.3, 0.2, 0.4]),
            "is_major_incident": np.random.choice([True, False], size=self.num_incidents, p=[0.01, 0.99]),
            "time_to_detect_hrs": np.random.exponential(scale=2, size=self.num_incidents),
            "time_to_resolve_hrs": np.random.exponential(scale=12, size=self.num_incidents)
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
            "is_compliant": np.random.choice([True, False], size=self.num_assets, p=[0.88, 0.12]),
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
            "value_percentage": [95.5, 87.2, 78.4]
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
            "requires_mfa": np.random.choice([True, False], size=num_sessions, p=[0.98, 0.02]),
            "is_just_in_time": np.random.choice([True, False], size=num_sessions, p=[0.85, 0.15])
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
            "is_compliant": np.random.choice([True, False], size=self.num_assets, p=[0.78, 0.22]) # 78.4% target
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
            "mfa_registered": np.random.choice([True, False], size=num_identities, p=[0.955, 0.045]), # ~95.5% target
            "conditional_access_enforced": np.random.choice([True, False], size=num_identities, p=[0.87, 0.13]), # ~87.2% target
            "risk_level": np.random.choice(["Low", "Medium", "High"], size=num_identities, p=[0.9, 0.08, 0.02]),
            "last_login": [self.start_date + timedelta(days=np.random.randint(20, 31)) for _ in range(num_identities)]
        }
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
