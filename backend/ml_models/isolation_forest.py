import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyIsolationForest:
    """Anomaly detection using Isolation Forest algorithm"""
    
    def __init__(self, contamination=0.05):
        """Initialize the Isolation Forest model
        
        Args:
            contamination: The proportion of outliers in the data set
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        self.is_fitted = False
        
    def fit(self, data):
        """Fit the model to the data
        
        Args:
            data: numpy array of shape (n_samples, n_features)
        """
        # Ensure data is 2D
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
            
        self.model.fit(data)
        self.is_fitted = True
        
    def predict(self, data):
        """Predict if points are anomalies
        
        Args:
            data: numpy array of shape (n_samples, n_features)
        
        Returns:
            numpy array where 1 is normal, -1 is anomaly
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before prediction")
            
        # Ensure data is 2D
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
            
        return self.model.predict(data)
    
    def anomaly_score(self, data):
        """Calculate anomaly score
        
        Args:
            data: numpy array of shape (n_samples, n_features)
        
        Returns:
            numpy array of anomaly scores (higher = more anomalous)
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before scoring")
            
        # Ensure data is 2D
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
            
        # Convert decision function to positive anomaly score
        return -self.model.decision_function(data)