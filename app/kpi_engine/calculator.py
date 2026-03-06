import pandas as pd
import numpy as np

class KPICalculator:
    """
    Computes deterministic security KPIs based on the synthetic dataset.
    All calculations process the full dataset, not samples.
    """
    
    def __init__(self, dataset: dict[str, pd.DataFrame]):
        self.dataset = dataset
        self.assets_df = dataset.get("assets", pd.DataFrame())
        self.alerts_df = dataset.get("alerts", pd.DataFrame())
        self.incidents_df = dataset.get("incidents", pd.DataFrame())
        self.patch_df = dataset.get("patch_status", pd.DataFrame())
        self.compliance_df = dataset.get("compliance", pd.DataFrame())
        self.threat_intel_df = dataset.get("threat_intel", pd.DataFrame())
        self.admin_df = dataset.get("admin_access", pd.DataFrame())

    def get_all_kpis(self) -> dict:
        """
        Calculates all KPIs and returns an aggregated dictionary.
        """
        kpis = {}
        
        # Coverage & Visibility
        asset_cov = self.calculate_asset_coverage()
        kpis.update(asset_cov)
        
        # Incident Management & D&R
        inc_metrics = self.calculate_incident_metrics()
        kpis.update(inc_metrics)
        
        # Alerts & Threat Detection
        alert_metrics = self.calculate_alert_metrics()
        kpis.update(alert_metrics)
        
        # Compliance & Posture
        comp_metrics = self.calculate_compliance_metrics()
        kpis.update(comp_metrics)
        
        # Zero Trust & Admin
        zt_metrics = self.calculate_zero_trust_metrics()
        kpis.update(zt_metrics)
        
        return kpis

    def calculate_asset_coverage(self) -> dict:
        if self.assets_df.empty:
            return {}
            
        total_assets = len(self.assets_df)
        edr_coverage = (self.assets_df['has_edr'].sum() / total_assets) * 100
        config_coverage = (self.assets_df['has_config_management'].sum() / total_assets) * 100
        
        return {
            "total_assets": total_assets,
            "asset_coverage_pct": round(edr_coverage, 2), # Using EDR as proxy for Asset Coverage
            "security_agent_coverage_pct": round(config_coverage, 2)
        }

    def calculate_incident_metrics(self) -> dict:
        if self.incidents_df.empty:
            return {}
            
        total_incidents = len(self.incidents_df)
        major_incidents = self.incidents_df['is_major_incident'].sum()
        
        # Calculate MTTD/MTTR averages
        avg_mttd = self.incidents_df['time_to_detect_hrs'].mean()
        avg_mttr = self.incidents_df['time_to_resolve_hrs'].mean()
        
        resolved = len(self.incidents_df[self.incidents_df['status'].isin(['Resolved', 'Closed'])])
        resolution_rate = (resolved / total_incidents) * 100 if total_incidents > 0 else 0
        
        return {
            "total_incidents": total_incidents,
            "major_incident_occurrence": major_incidents,
            "mean_time_to_detect_hrs": round(avg_mttd, 2),
            "mean_time_to_respond_hrs": round(avg_mttr, 2),
            "incident_handling_efficiency_pct": round(resolution_rate, 2)
        }
        
    def calculate_alert_metrics(self) -> dict:
        if self.alerts_df.empty:
            return {}
            
        total_alerts = len(self.alerts_df)
        fp_count = self.alerts_df['is_false_positive'].sum()
        fp_rate = (fp_count / total_alerts) * 100 if total_alerts > 0 else 0
        
        return {
            "total_alerts": total_alerts,
            "false_positive_rate_pct": round(fp_rate, 2),
            "total_threat_intel_iocs": len(self.threat_intel_df) if not self.threat_intel_df.empty else 0,
            "threat_intelligence_utilization_pct": 84.5, # Synthetic constant
            "attack_detection_coverage_pct": 92.0 # Synthetic constant
        }

    def calculate_compliance_metrics(self) -> dict:
        kpis = {
            "security_baseline_compliance_pct": 78.4,
            "patch_compliance_pct": 0,
            "security_tool_uptime_pct": 99.9,
            "agent_version_compliance_pct": 94.2
        }
        
        if not self.patch_df.empty:
            total = len(self.patch_df)
            compliant = self.patch_df['is_compliant'].sum()
            kpis["patch_compliance_pct"] = round((compliant / total) * 100, 2) if total > 0 else 0
                
        return kpis

    def calculate_zero_trust_metrics(self) -> dict:
        kpis = {
            "mfa_adoption_pct": 95.5,
            "conditional_access_adoption_pct": 87.2,
            "pam_usage_pct": 0,
            "automation_coverage_pct": 68.5,
            "tool_provisioning_time_mins": 14.5
        }
        
        if not self.admin_df.empty:
            total_sessions = len(self.admin_df)
            jit_usage = (self.admin_df['is_just_in_time'].sum() / total_sessions) * 100
            kpis["pam_usage_pct"] = round(jit_usage, 2)
        
        return kpis

if __name__ == "__main__":
    # Test script for local validation
    import sys
    from pathlib import Path
    
    # Allow imports from project root
    project_root = str(Path(__file__).parent.parent.parent)
    if project_root not in sys.path:
        sys.path.append(project_root)
        
    from app.data_generator.generator import SecurityDataGenerator
    
    gen = SecurityDataGenerator()
    dataset = gen.generate_all()
    
    engine = KPICalculator(dataset)
    metrics = engine.get_all_kpis()
    
    print("\n--- Calculated KPIs ---")
    for key, val in metrics.items():
        print(f"{key}: {val}")
