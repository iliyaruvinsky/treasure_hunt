"""
ML Model Training Pipeline
Trains models for money loss prediction based on historical data
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import os
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from app.models.finding import Finding
from app.models.money_loss import MoneyLossCalculation
from app.core.config import settings


class ModelTrainer:
    """Train ML models for money loss prediction"""
    
    def __init__(self, db: Session):
        self.db = db
        self.model_dir = Path(settings.STORAGE_PATH) / "ml_models"
        self.model_dir.mkdir(parents=True, exist_ok=True)
    
    def train(self, model_version: Optional[str] = None) -> Dict[str, Any]:
        """
        Train money loss prediction model
        
        Returns:
            Dict with training metrics
        """
        # Load training data
        X, y = self._load_training_data()
        
        if len(X) < 10:
            return {
                "success": False,
                "message": "Insufficient training data (need at least 10 samples)"
            }
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Save model
        version = model_version or "latest"
        model_path = self.model_dir / f"money_loss_model_{version}.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        # Also save as latest
        latest_path = self.model_dir / "money_loss_model.pkl"
        with open(latest_path, 'wb') as f:
            pickle.dump(model, f)
        
        return {
            "success": True,
            "model_version": version,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "mean_absolute_error": float(mae),
            "r2_score": float(r2),
            "model_path": str(model_path)
        }
    
    def _load_training_data(self) -> tuple:
        """Load training data from database"""
        # Get findings with money loss calculations
        findings = self.db.query(Finding).join(
            MoneyLossCalculation
        ).all()
        
        X = []
        y = []
        
        for finding in findings:
            # Extract features
            features = self._extract_features(finding)
            if features:
                X.append(features)
                y.append(finding.money_loss_calculation.estimated_loss)
        
        return np.array(X), np.array(y)
    
    def _extract_features(self, finding: Finding) -> Optional[list]:
        """Extract features from finding"""
        try:
            severity_map = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
            severity_encoded = severity_map.get(finding.severity, 2)
            
            risk_score = finding.risk_assessment.risk_score if finding.risk_assessment else 50
            
            issue_type_code = finding.issue_type.code if finding.issue_type else "UNKNOWN"
            issue_type_hash = hash(issue_type_code) % 1000
            
            confidence = finding.classification_confidence or 0.5
            
            focus_area_code = finding.focus_area.code
            focus_area_hash = hash(focus_area_code) % 100
            
            return [
                severity_encoded,
                risk_score,
                issue_type_hash,
                confidence,
                focus_area_hash
            ]
        except Exception:
            return None

