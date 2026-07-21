"""
LSTM Model for Time Series Prediction
Uses neural networks for NSE price forecasting
"""

import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import logging

logger = logging.getLogger(__name__)


class LSTMModel:
    """LSTM Model for price prediction"""
    
    def __init__(self, lookback: int = 60, units: int = 128, dropout: float = 0.2):
        """
        Initialize LSTM model
        
        Args:
            lookback: Number of past days to use
            units: Number of LSTM units
            dropout: Dropout rate
        """
        self.lookback = lookback
        self.units = units
        self.dropout = dropout
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
    def build_model(self, input_shape: tuple):
        """Build LSTM neural network"""
        self.model = Sequential([
            LSTM(self.units, return_sequences=True, input_shape=input_shape),
            Dropout(self.dropout),
            LSTM(self.units, return_sequences=False),
            Dropout(self.dropout),
            Dense(25),
            Dense(1)
        ])
        
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        logger.info("LSTM model built successfully")
        
    def prepare_data(self, data: np.ndarray):
        """
        Prepare data for LSTM training
        
        Args:
            data: Price data array
            
        Returns:
            Normalized data
        """
        scaled_data = self.scaler.fit_transform(data.reshape(-1, 1))
        return scaled_data
    
    def create_sequences(self, data: np.ndarray):
        """
        Create sequences for LSTM
        
        Args:
            data: Prepared data
            
        Returns:
            Tuple of (X, y) sequences
        """
        X, y = [], []
        
        for i in range(len(data) - self.lookback):
            X.append(data[i:i + self.lookback])
            y.append(data[i + self.lookback])
            
        return np.array(X), np.array(y)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, epochs: int = 100, batch_size: int = 32):
        """
        Train the LSTM model
        
        Args:
            X_train: Training features
            y_train: Training targets
            epochs: Number of training epochs
            batch_size: Batch size
        """
        if self.model is None:
            self.build_model((X_train.shape[1], 1))
            
        logger.info("Starting LSTM training...")
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
        logger.info("LSTM training completed")
    
    def predict(self, data: np.ndarray):
        """
        Make predictions
        
        Args:
            data: Input data
            
        Returns:
            Predictions (denormalized)
        """
        predictions = self.model.predict(data, verbose=0)
        predictions = self.scaler.inverse_transform(predictions)
        return predictions
    
    def save_model(self, filepath: str):
        """Save model to file"""
        if self.model:
            self.model.save(filepath)
            logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model from file"""
        self.model = keras.models.load_model(filepath)
        logger.info(f"Model loaded from {filepath}")
