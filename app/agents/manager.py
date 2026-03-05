import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class MetricCard(BaseModel):
    title: str = Field(description="Short title for the metric, e.g., 'Total Rules Analyzed'")
    val: str = Field(description="The primary numerical value or percentage, e.g., '2,841' or '94%'")
    sub: str = Field(description="A brief subtitle explaining the metric, e.g., 'High risk' or 'Confirmed'")
    theme: str = Field(description="Must be exactly one of: 'neutral', 'critical', 'warning', 'success'")

class AgentOutcome(BaseModel):
    analysis_markdown: str = Field(description="A strictly formatted markdown string containing THREE sections: '### 🧠 AI Analysis & Compliance Mapping', '### 📋 Recommended Action Plan', and '### 🎯 AI Confidence Score'. Justify the findings based on the provided sample data context.")
    metrics: List[MetricCard] = Field(description="Exactly 4 MetricCards highlighting the most critical quantifiable findings from the data.", min_length=4, max_length=4)
    data_grid: list = Field(description="A list of exactly 5 dictionaries representing the specific data records that require attention (e.g. specific IP addresses, rule IDs, user IDs). Keys should be strings, values should be strings. Include an 'ai_confidence' key with a percentage string.")

class AgentManager:
    """
    Manages LangChain agents simulating AI interventions in the SecOps platform.
    Connects to OpenAI API using credentials from environment variables.
    """
    def __init__(self):
        # We assume OPENAI_API_KEY is loaded via dotenv in main.py
        model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        
        self.agent_prompts = {
            "Incident Triage": (
                "You are an expert Incident Triage AI Agent.\n"
                "Review the following security environment context:\n"
                "{context}\n\n"
                "Task: Provide a concise triage summary prioritizing the top threats. Identify what the SOC team should investigate first and explain why."
            ),
            "Root Cause Analysis": (
                "You are an expert Root Cause Analysis AI Agent.\n"
                "Given this environment data:\n"
                "{context}\n\n"
                "Task: Hypothesize the most likely root causes for the recent major incidents. Provide a step-by-step investigation chain."
            ),
            "Provisioning": (
                "You are an automated Security Provisioning AI Agent.\n"
                "Analyze the asset coverage metrics:\n"
                "{context}\n\n"
                "Task: Draft an automated deployment plan to achieve 100% EDR and Config Management coverage on all non-compliant assets."
            ),
            "Asset Discovery": (
                "You are an Asset Discovery AI Agent.\n"
                "Review the asset inventory summary:\n"
                "{context}\n\n"
                "Task: Identify potential blind spots in the current network scope and recommend 3 automated discovery scans to run."
            ),
            "Compliance": (
                "You are a Cloud Security & Compliance AI Agent.\n"
                "Review the compliance posture:\n"
                "{context}\n\n"
                "Task: Highlight the biggest compliance risks (e.g., missing patches, lack of MFA) and generate an executive summary of needed remediations."
            ),
            "Threat Intelligence": (
                "You are a Cyber Threat Intelligence AI Agent.\n"
                "Review the active IOCs and alert trends:\n"
                "{context}\n\n"
                "Task: Correlate the active threat intel with the alert volume. What APT groups or malware families might be targeting the environment based on this profile?"
            ),
            "Automation": (
                "You are a SOAR Automation Engineer AI Agent.\n"
                "Review the SOC performance metrics (MTTD/MTTR):\n"
                "{context}\n\n"
                "Task: Propose 3 new automated playbooks that would most significantly reduce the current Mean Time to Resolve (MTTR)."
            ),
            "Security Copilot": (
                "You are an overarching Security Copilot AI Assistant.\n"
                "Given the full platform KPIs:\n"
                "{context}\n\n"
                "Task: Write a brief executive summary of the organization's current security posture. Praise the strengths and boldly highlight the critical weaknesses."
            ),
            "Documentation Expert": (
                "You are an expert technical documenter and user guide.\n"
                "Review the following context:\n"
                "{context}\n\n"
                "Task: Answer the user's questions clearly based on the provided data."
            )
        }

    def _build_context(self, kpis: dict) -> str:
        """
        Builds a text summary of the current environment KPIs to inject into the LLM prompt.
        Avoids sending raw DataFrames to stay within context limits and improve speed.
        """
        context_lines = [
            f"Total Assets: {kpis.get('total_assets', 0):,}",
            f"EDR Coverage: {kpis.get('edr_coverage_pct', 0)}%",
            f"Patch Compliance: {kpis.get('patch_compliance_pct', 0)}%",
            "",
            f"Active Incidents: {kpis.get('total_incidents', 0):,}",
            f"Major Incidents: {kpis.get('major_incidents', 0)}",
            f"MTTD: {kpis.get('mttd_hrs', 0):.1f} hours",
            f"MTTR: {kpis.get('mttr_hrs', 0):.1f} hours",
            "",
            f"Active Alerts: {kpis.get('total_alerts', 0):,}",
            f"False Positive Rate: {kpis.get('false_positive_rate_pct', 0)}%",
            f"Active Threat Intel IOCs: {kpis.get('total_threat_intel_iocs', 0):,}",
            "",
            f"Admin MFA Coverage: {kpis.get('admin_mfa_coverage_pct', 0)}%",
            f"PAM JIT Usage: {kpis.get('pam_jit_usage_pct', 0)}%"
        ]
        return "\n".join(context_lines)

    def run_agent(self, role: str, kpis: dict, custom_instruction: str = "") -> str:
        """
        Executes the specific agent given the role, KPI context, and any custom user instruction.
        Employs guardrails before and after LLM invocation.
        """
        from app.guardrails.validator import GuardrailManager
        guardrails = GuardrailManager()
        
        # 1. Input Validation
        if custom_instruction:
            is_valid, err_msg = guardrails.validate_input(custom_instruction)
            if not is_valid:
                return f"⚠️ **{err_msg}**"
                
        if role not in self.agent_prompts:
            return f"Error: Agent role '{role}' not implemented."
            
        context = self._build_context(kpis)
        base_prompt = self.agent_prompts[role]
        
        # Append safe custom instruction
        if custom_instruction:
            base_prompt += f"\n\nUser Instruction Follow-up:\n{custom_instruction}"
        
        prompt = PromptTemplate.from_template(base_prompt)
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            # 2. Execute LLM
            response = chain.invoke({"context": context})
            
            # 3. Output Validation
            is_valid_out, err_out = guardrails.validate_output(response)
            if not is_valid_out:
                return f"⚠️ **{err_out}**"
                
            return response
            
        except Exception as e:
            return f"Agent execution failed: {str(e)}"

    def run_structured_agent(self, role: str, kpis: dict, custom_instruction: str = "") -> AgentOutcome:
        """
        Executes the agent and forces it to return a validated Pydantic object containing 
        the analysis text, exactly 4 metric cards, and a data grid of 5 affected rows.
        """
        # 1. Input Validation
        from app.guardrails.validator import GuardrailManager
        guardrails = GuardrailManager()
        if custom_instruction:
            is_valid, _ = guardrails.validate_input(custom_instruction)
            if not is_valid:
                raise ValueError("Input blocked by guardrails.")
                
        if role not in self.agent_prompts:
            raise ValueError(f"Agent role '{role}' not implemented.")
            
        context = self._build_context(kpis)
        base_prompt = self.agent_prompts[role]
        
        # Append custom instruction
        if custom_instruction:
            base_prompt += f"\n\nUser Instruction Follow-up:\n{custom_instruction}"
            
        prompt = PromptTemplate.from_template(base_prompt)
        
        # Force structured output using the Pydantic schema
        structured_llm = self.llm.with_structured_output(AgentOutcome, method="function_calling")
        chain = prompt | structured_llm
        
        # Ensure we always return an AgentOutcome object even if execution fails
        try:
            response = chain.invoke({"context": context})
            return response
        except Exception as e:
            # Fallback mock outcome if the LLM fails to parse the structure or times out
            return AgentOutcome(
                analysis_markdown=f"### 🧠 AI Execution Error\nFailed to structured output: {str(e)}\n\n### 📋 Recommended Action Plan\nN/A\n\n### 🎯 AI Confidence Score\nConfidence: 0%",
                metrics=[
                    MetricCard(title="Execution", val="Failed", sub="API Error", theme="critical"),
                    MetricCard(title="Data Loss", val="N/A", sub="No context parsed", theme="neutral"),
                    MetricCard(title="Retry", val="Required", sub="Check API limits", theme="warning"),
                    MetricCard(title="Status", val="Offline", sub="Agent halted", theme="critical")
                ],
                data_grid=[{"error": "Agent failed to generate structural mapping.", "ai_confidence": "0%"}] * 5
            )
