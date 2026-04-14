🎯 1. Risk Score (0–100, Higher = Lower Risk)
What it means: "How exposed are we to a security breach?"

How it's calculated: It's a weighted average of your 4 biggest gaps:

30% from Patch Compliance (are systems patched?)
30% from Baseline Compliance (do configs follow CIS/NIST standards?)
20% from MFA Adoption (are users using multi-factor auth?)
20% from Asset Coverage (do we have EDR on all endpoints?)
Example: If patch compliance is 48% and baseline is 42%, that means 52% and 58% of those areas are exposed. Those gaps pull the risk score down to ~49.

🛡️ 2. Resilience Index (0–100%)
What it means: "If we got hit, how well could we bounce back?"

How it's calculated: Simple average of the same 4 pillars:

(Asset Coverage + Patch Compliance + Baseline Compliance + MFA) / 4
Example: (51 + 48 + 42 + 61) / 4 = 50.5% — we can only recover from half the scenarios.

📊 3. Security Posture (0–100)
What it means: "How solid is our overall defense stance?"

How it's calculated: Weighted blend of compliance + AI capability:

40% from Baseline Compliance (config standards)
30% from Patch Compliance (vulnerability coverage)
30% from Prediction Accuracy (how well our AI detects real threats vs. false positives)
Prediction Accuracy = 100 - False Positive Rate. If 72% of alerts are false positives, only 28% are real → AI accuracy is 28%. That drags posture down hard.

📈 4. Program Maturity (1–5, CMMI Scale)
What it means: "On a 1-to-5 maturity scale, where does our security program sit?"

How it's calculated: Average of 4 capabilities, mapped to a 1–5 scale:

(Asset Coverage + MFA + Prediction Accuracy + Auto-Remediation Rate) / 4 / 20
Example: (51 + 61 + 28 + 21) / 4 = 40.25 → 40.25 / 20 = 2.0/5 — we're at "Repeatable" level, far from "Optimized" (5.0).

💰 5. ROSI — Return on Security Investment (%)
What it means: "For every dollar we spend on security tools, how much value are we getting back?"

How it's calculated:

ROSI = (Savings from AI) / (Annual Security Tooling Cost) × 100
Where:

Annual Tooling Cost = Total Assets × $150/asset/year (industry benchmark for EDR/SIEM licensing)
Savings = Two sources:
Analyst Time Saved: hours_saved_per_week × 52 weeks × $75/hr (analyst hourly rate)
Cost Leakage Found: Shadow IT & non-compliant SaaS costs identified × 12 months
Example: With 10,000 assets → annual cost = $1.5M. AI saves ~9 analyst hrs/week ($35K/yr) + finds $21K/mo in shadow IT ($252K/yr). Total savings $287K ÷ $1.5M = 19% ROSI — we're barely breaking even, justifying more investment in AI automation.