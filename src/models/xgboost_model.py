"""
XGBoost Model for Trading Signal Generation
Gradient boosting for classification of buy/sell signals
"""

import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)


class XGBoostModel:
    """XGBoost Model for signal prediction"""
    
    def __init__(self, max_depth: int = 5, learning_rate: float = 0.1, n_estimators: int = 100):
        """
        Initialize XGBoost model
        
        Args:
            max_depth: Maximum tree depth
            learning_rate: Learning rate
            n_estimators: Number of boosting rounds
        """
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.model = None
        self.scaler = StandardScaler()
        
    def build_model(self):
        """Build XGBoost model"""
        self.model = xgb.XGBClassifier(
            max_depth=self.max_depth,
            learning_rate=self.learning_rate,
            n_estimators=self.n_estimators,
            objective='binary:logistic',
            random_state=42,
            n_jobs=-1
        )
        logger.info("XGBoost model built successfully")
    
    def train(self, X_train: pd.DataFrame, y_train: np.ndarray):
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training targets (0 = SELL, 1 = BUY)
        """
        if self.model is None:
            self.build_model()
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_train)
        
        logger.info("Starting XGBoost training...")
        self.model.fit(X_scaled, y_train, verbose=1)
        logger.info("XGBoost training completed")
    
    def predict(self, X: pd.DataFrame):
        """
        Predict signals
        
        Args:
            X: Features
            
        Returns:
            Predicted signals (0 or 1)
        """
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        return predictions
    
    def predict_proba(self, X: pd.DataFrame):
        """
        Get prediction probabilities
        
        Args:
            X: Features
            
        Returns:
            Probability of buy/sell
        """
        X_scaled = self.scaler.transform(X)
        probabilities = self.model.predict_proba(X_scaled)
        return probabilities
    
    def get_feature_importance(self):
        """Get feature importance"""
        if self.model:
            return self.model.feature_importances_
        return None
    
    def save_model(self, filepath: str):
        """Save model to file"""
        if self.model:
            self.model.save_model(filepath)
            logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model from file"""
        self.model = xgb.XGBClassifier()
        self.model.load_model(filepath)
        logger.info(f"Model loaded from {filepath}")
