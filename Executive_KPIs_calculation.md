1. Overall Risk Score
Concept: A composite representation of enterprise vulnerabilities. Calculation: 100 - ((Unpatched Assets * 0.3) + (Non-compliant Baseline * 0.3) + (Missing MFA * 0.2) + (Missing EDR Coverage * 0.2)) Why this approach: We look at the "inverse" of our compliance operational metrics and weight them. Missing patches and baselines are given heavier risk weights (30% each) than missing MFA or endpoint agents (20% each).

2. Resilience Index
Concept: The enterprise’s ability to withstand and recover from a cyber event based on structural hardening. Calculation: (Asset Coverage * 0.25) + (Patch Compliance * 0.25) + (Baseline Compliance * 0.25) + (MFA Adoption * 0.25) Why this approach: A straightforward equal-weight average (25% each) of the four core pillars of defensive architecture.

3. Security Posture Index
Concept: Represents the active operational state of security rather than just structural compliance. Calculation: (Baseline Compliance * 0.4) + (Patch Compliance * 0.3) + (AI Prediction Accuracy * 0.3) Why this approach: It blends traditional hygiene (baselines and patching) with the current effectiveness of the platform's AI (predictive threat accuracy) to show an operational score out of 100.

4. Security Program Maturity Score
Concept: A CMMI-aligned score measuring how advanced the security automation program is, graded on a standard 1.0 to 5.0 maturity scale. Calculation: Average of (Asset Coverage + MFA Adoption + Threat Prediction + Auto-Remediation Rate) / 20 Why this approach: By taking the average percentage of these 4 advanced metrics and dividing by 20, we translate a 0-100% scale into the industry-standard 1 to 5 scale (e.g., 4.2/5.0). It emphasizes how heavily the platform uses Auto-Remediation and AI Prediction alongside foundational coverage.

5. Return on Security Investment (ROSI)
Concept: A direct financial multiplier indicating how much value the AI automation is returning versus a standard enterprise SOC cost. Calculation: ((AI Analyst Time Saved * 52 weeks * roughly $100/hr) + (Cost Leakage Identified per month * 12 months)) / $150,000 assumed base security investment Why this approach: We take the direct hard-dollar savings (shadow IT/cloud leakage) and the soft-dollar savings (analyst hours returned to the business) over a full year, and compare it against an assumed standardized platform cost. This yields an executive-friendly percentage multiplier (e.g., 850%).