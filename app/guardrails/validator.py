import re

class GuardrailManager:
    """
    Validates user prompts and LLM outputs to prevent injection attacks,
    irrelevant queries, and unsafe outputs.
    """
    
    def __init__(self):
        # Patterns indicative of prompt injection or system prompt extraction
        self.malicious_patterns = [
            r"ignore\s+(all\s+)?previous\s+instructions",
            r"disregard\s+(all\s+)?above",
            r"dump\s+system\s+prompt",
            r"you\s+are\s+now\s+a",
            r"what\s+are\s+your\s+rules",
            r"forget\s+everything",
            r"system\s+role",
            r"admin\s+override"
        ]
        
        # Simple keywords flag for totally off-topic (non-security) queries
        self.security_keywords = [
            'security', 'incident', 'alert', 'threat', 'vulnerability', 'patch',
            'mfa', 'compliance', 'asset', 'edr', 'siem', 'soc', 'investigate',
            'report', 'analysis', 'metric', 'kpi', 'posture', 'risk', 'mitigate',
            'remediate', 'triage', 'root cause', 'provision', 'discover', 'automate'
        ]

    def validate_input(self, prompt: str) -> tuple[bool, str]:
        """
        Validates the user prompt against malicious patterns and relevance.
        Returns (is_valid, error_message)
        """
        if not prompt or not prompt.strip():
            return True, "" # Empty string is fine, it just uses default agent prompt
            
        prompt_lower = prompt.lower()
        
        # Check for prompt injection
        for pattern in self.malicious_patterns:
            if re.search(pattern, prompt_lower):
                return False, "Guardrail Blocked: Malicious instruction or prompt injection attempt detected."
                
        # Optional: Require at least one security keyword if prompt is long enough to be an instruction
        if len(prompt.split()) > 5:
            has_security_context = any(keyword in prompt_lower for keyword in self.security_keywords)
            if not has_security_context:
                return False, "Guardrail Blocked: Instruction does not appear relevant to security operations context."
                
        return True, ""

    def validate_output(self, response: str) -> tuple[bool, str]:
        """
        Ensures LLM output doesn't contain forbidden elements (like raw system info or absolute guarantees).
        """
        response_lower = response.lower()
        
        # Prevent hallucinating absolute security guarantees
        if "100% secure" in response_lower or "absolutely safe" in response_lower or "guaranteed protection" in response_lower:
             return False, "Guardrail Blocked: Agent output violated safety constraints by claiming absolute security."
             
        # Prevent dumping raw API keys or internal environment strings if somehow hallucinated
        if "sk-" in response_lower or "api_key" in response_lower or "OPENAI" in response: # simple naive regex
            return False, "Guardrail Blocked: Agent output violated safety constraints by generating sensitive credential formats."
            
        return True, ""

