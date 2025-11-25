from typing import Dict, Any, Optional
from app.models.finding import Finding
from app.models.issue_type import IssueType
from .llm_client import get_llm_client, LLMClient
import json
import re


class MoneyLossLLM:
    """LLM-based money loss calculation"""
    
    SYSTEM_PROMPT = """You are a financial risk analyst specializing in SAP system security and business process analysis.
Your task is to estimate potential financial losses based on security incidents, fraud indicators, process bottlenecks, and compliance violations.

Consider:
- Type of issue (fraud, security breach, process bottleneck, compliance violation)
- Severity and risk level
- Potential impact on business operations
- Industry-standard cost estimates for similar incidents
- Regulatory fines and compliance costs
- Productivity losses
- Reputation damage costs

Provide your estimate in a structured format with reasoning."""

    PROMPT_TEMPLATE = """Analyze the following finding and estimate the potential financial loss:

Finding Title: {title}
Description: {description}
Issue Type: {issue_type}
Severity: {severity}
Risk Level: {risk_level}
Risk Category: {risk_category}

Additional Context:
{additional_context}

Provide your analysis in the following JSON format:
{{
    "estimated_loss": <number in currency units>,
    "confidence": <0.0 to 1.0>,
    "reasoning": "<detailed explanation>",
    "factors_considered": [
        "<factor 1>",
        "<factor 2>",
        ...
    ],
    "breakdown": {{
        "direct_losses": <number>,
        "indirect_losses": <number>,
        "compliance_fines": <number>,
        "productivity_loss": <number>,
        "reputation_damage": <number>
    }}
}}"""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        try:
            self.llm_client = llm_client or get_llm_client()
        except (ValueError, Exception):
            # If LLM client can't be initialized (no API key), set to None
            self.llm_client = None
    
    def calculate(self, finding: Finding, 
                  issue_type: Optional[IssueType] = None,
                  additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Calculate money loss using LLM
        
        Returns:
            Dict with estimated_loss, confidence, reasoning, etc.
        """
        # Build prompt
        prompt = self.PROMPT_TEMPLATE.format(
            title=finding.title,
            description=finding.description or "No description available",
            issue_type=issue_type.name if issue_type else "Unknown",
            severity=finding.severity,
            risk_level=finding.risk_assessment.risk_level if finding.risk_assessment else "Unknown",
            risk_category=finding.risk_assessment.risk_category if finding.risk_assessment else "Unknown",
            additional_context=self._format_additional_context(additional_context or {})
        )
        
        if not self.llm_client:
            # No LLM client available, use fallback
            return self._fallback_calculation(finding, issue_type)
        
        try:
            # Get LLM response
            response = self.llm_client.generate(prompt, self.SYSTEM_PROMPT)
            
            # Parse JSON from response
            result = self._parse_response(response)
            
            return result
            
        except Exception as e:
            # Fallback calculation
            return self._fallback_calculation(finding, issue_type)
    
    def _format_additional_context(self, context: Dict[str, Any]) -> str:
        """Format additional context for prompt"""
        if not context:
            return "No additional context available."
        
        lines = []
        for key, value in context.items():
            lines.append(f"{key}: {value}")
        
        return "\n".join(lines)
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from LLM response"""
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                result = json.loads(json_str)
                # Validate and normalize
                return {
                    "estimated_loss": float(result.get("estimated_loss", 0)),
                    "confidence": float(result.get("confidence", 0.5)),
                    "reasoning": result.get("reasoning", ""),
                    "factors_considered": result.get("factors_considered", []),
                    "breakdown": result.get("breakdown", {})
                }
            except json.JSONDecodeError:
                pass
        
        # If JSON parsing fails, try to extract numbers
        return self._extract_from_text(response)
    
    def _extract_from_text(self, text: str) -> Dict[str, Any]:
        """Extract estimate from unstructured text"""
        # Look for currency amounts
        amount_pattern = r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        matches = re.findall(amount_pattern, text)
        
        estimated_loss = 0.0
        if matches:
            # Take the largest number found
            amounts = [float(m.replace(',', '')) for m in matches]
            estimated_loss = max(amounts)
        
        return {
            "estimated_loss": estimated_loss,
            "confidence": 0.4,
            "reasoning": text[:500],  # First 500 chars
            "factors_considered": [],
            "breakdown": {}
        }
    
    def _fallback_calculation(self, finding: Finding, 
                             issue_type: Optional[IssueType]) -> Dict[str, Any]:
        """Fallback calculation when LLM fails"""
        # Base estimates by severity
        base_estimates = {
            "Critical": 100000.0,
            "High": 50000.0,
            "Medium": 10000.0,
            "Low": 1000.0
        }
        
        estimated_loss = base_estimates.get(finding.severity, 5000.0)
        
        # Adjust by issue type
        if issue_type:
            if "FRAUD" in issue_type.code:
                estimated_loss *= 2.0
            elif "SOD" in issue_type.code:
                estimated_loss *= 1.5
        
        return {
            "estimated_loss": estimated_loss,
            "confidence": 0.3,
            "reasoning": "Fallback calculation based on severity and issue type",
            "factors_considered": ["severity", "issue_type"],
            "breakdown": {
                "direct_losses": estimated_loss * 0.6,
                "indirect_losses": estimated_loss * 0.3,
                "compliance_fines": estimated_loss * 0.1
            }
        }

