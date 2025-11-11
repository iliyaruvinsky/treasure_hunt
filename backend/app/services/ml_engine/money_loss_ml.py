from typing import Dict, Any, Optional
import pickle
import os
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from app.models.finding import Finding
from app.models.issue_type import IssueType
from app.core.config import settings


class MoneyLossML:
    """ML-based money loss prediction"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or os.path.join(
            settings.STORAGE_PATH, "ml_models", "money_loss_model.pkl"
        )
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load trained model"""
        model_file = Path(self.model_path)
        if model_file.exists():
            try:
                with open(model_file, 'rb') as f:
                    self.model = pickle.load(f)
            except Exception:
                self.model = None
        else:
            self.model = None
    
    def calculate(self, finding: Finding,
                  issue_type: Optional[IssueType] = None) -> Dict[str, Any]:
        """
        Calculate money loss using ML model
        
        Returns:
            Dict with estimated_loss, confidence, etc.
        """
        if not self.model:
            # Return default if no model available
            return self._default_calculation(finding, issue_type)
        
        # Extract features
        features = self._extract_features(finding, issue_type)
        
        # Predict
        try:
            estimated_loss = float(self.model.predict([features])[0])
            confidence = 0.7  # ML confidence
            
            return {
                "estimated_loss": max(0, estimated_loss),  # Ensure non-negative
                "confidence": confidence,
                "reasoning": "ML model prediction based on historical data",
                "factors_considered": self._get_feature_names(),
                "breakdown": {}
            }
        except Exception:
            return self._default_calculation(finding, issue_type)
    
    def _extract_features(self, finding: Finding,
                         issue_type: Optional[IssueType]) -> list:
        """Extract features for ML model"""
        # Severity encoding
        severity_map = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        severity_encoded = severity_map.get(finding.severity, 2)
        
        # Risk score
        risk_score = finding.risk_assessment.risk_score if finding.risk_assessment else 50
        
        # Issue type encoding (simple hash)
        issue_type_code = issue_type.code if issue_type else "UNKNOWN"
        issue_type_hash = hash(issue_type_code) % 1000
        
        # Classification confidence
        confidence = finding.classification_confidence or 0.5
        
        # Focus area encoding
        focus_area_code = finding.focus_area.code
        focus_area_hash = hash(focus_area_code) % 100
        
        return [
            severity_encoded,
            risk_score,
            issue_type_hash,
            confidence,
            focus_area_hash
        ]
    
    def _get_feature_names(self) -> list:
        """Get feature names for explanation"""
        return [
            "severity",
            "risk_score",
            "issue_type",
            "classification_confidence",
            "focus_area"
        ]
    
    def _default_calculation(self, finding: Finding,
                           issue_type: Optional[IssueType]) -> Dict[str, Any]:
        """Default calculation when model not available"""
        base_estimates = {
            "Critical": 75000.0,
            "High": 35000.0,
            "Medium": 7500.0,
            "Low": 750.0
        }
        
        estimated_loss = base_estimates.get(finding.severity, 5000.0)
        
        return {
            "estimated_loss": estimated_loss,
            "confidence": 0.5,
            "reasoning": "Default calculation (ML model not trained)",
            "factors_considered": ["severity"],
            "breakdown": {}
        }

