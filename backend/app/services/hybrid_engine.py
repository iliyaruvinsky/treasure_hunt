"""
Hybrid Money Loss Calculation Engine
Combines LLM reasoning with ML predictions
"""
from typing import Dict, Any, Optional
from app.models.finding import Finding
from app.models.issue_type import IssueType
from app.services.llm_engine.money_loss_llm import MoneyLossLLM
from app.services.ml_engine.money_loss_ml import MoneyLossML


class HybridMoneyLossEngine:
    """Hybrid engine combining LLM and ML for money loss calculation"""
    
    def __init__(self, llm_client=None):
        self.llm_calculator = MoneyLossLLM(llm_client)
        self.ml_calculator = MoneyLossML()
    
    def calculate(self, finding: Finding,
                  issue_type: Optional[IssueType] = None,
                  additional_context: Optional[Dict[str, Any]] = None,
                  use_llm: bool = True,
                  use_ml: bool = True) -> Dict[str, Any]:
        """
        Calculate money loss using hybrid approach
        
        Args:
            finding: Finding to calculate loss for
            issue_type: Associated issue type
            additional_context: Additional context for LLM
            use_llm: Whether to use LLM calculation
            use_ml: Whether to use ML calculation
        
        Returns:
            Dict with final estimate and breakdown
        """
        llm_result = None
        ml_result = None
        
        # Get LLM estimate
        if use_llm:
            try:
                llm_result = self.llm_calculator.calculate(
                    finding, issue_type, additional_context
                )
            except Exception as e:
                # Fallback to ML if LLM fails
                use_llm = False
        
        # Get ML estimate
        if use_ml:
            try:
                ml_result = self.ml_calculator.calculate(finding, issue_type)
            except Exception:
                use_ml = False
        
        # Combine results
        if llm_result and ml_result:
            # Weighted average: LLM gets higher weight for reasoning
            llm_weight = 0.6
            ml_weight = 0.4
            
            final_estimate = (
                llm_result["estimated_loss"] * llm_weight +
                ml_result["estimated_loss"] * ml_weight
            )
            
            # Combined confidence
            confidence = (
                llm_result["confidence"] * llm_weight +
                ml_result["confidence"] * ml_weight
            )
            
            return {
                "estimated_loss": final_estimate,
                "confidence": confidence,
                "calculation_method": "hybrid",
                "llm_estimate": llm_result["estimated_loss"],
                "ml_estimate": ml_result["estimated_loss"],
                "reasoning": llm_result.get("reasoning", ""),
                "factors_considered": list(set(
                    llm_result.get("factors_considered", []) +
                    ml_result.get("factors_considered", [])
                )),
                "breakdown": llm_result.get("breakdown", {})
            }
        
        elif llm_result:
            return {
                **llm_result,
                "calculation_method": "llm",
                "ml_estimate": None
            }
        
        elif ml_result:
            return {
                **ml_result,
                "calculation_method": "ml",
                "llm_estimate": None
            }
        
        else:
            # Fallback
            return {
                "estimated_loss": 5000.0,
                "confidence": 0.2,
                "calculation_method": "fallback",
                "reasoning": "Both LLM and ML calculations failed",
                "factors_considered": [],
                "breakdown": {}
            }

