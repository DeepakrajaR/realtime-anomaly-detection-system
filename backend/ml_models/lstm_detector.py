import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed

class LSTMAnomalyDetector:
    """Anomaly detection using LSTM autoencoder"""
    
    def __init__(self, seq_length=10, n_features=1):
        """Initialize the LSTM model
        
        Args:
            seq_length: Length of input sequences
            n_features: Number of features per time step
        """
        self.seq_length = seq_length
        self.n_features = n_features
        self.model = self._build_model()
        self.threshold = None
        self.is_fitted = False
        
    def _build_model(self):
        """Build LSTM autoencoder model"""
        model = Sequential([
            # Encoder
            LSTM(64, activation='relu', input_shape=(self.seq_length, self.n_features), return_sequences=False),
            
            # Bottleneck
            RepeatVector(self.seq_length),
            
            # Decoder
            LSTM(64, activation='relu', return_sequences=True),
            TimeDistributed(Dense(self.n_features))
        ])
        
        model.compile(optimizer='adam', loss='mse')
        return model
    
    def _create_sequences(self, data):
        """Create sequences from time series data
        
        Args:
            data: 1D numpy array of time series data
            
        Returns:
            numpy array of shape (n_samples, seq_length, n_features)
        """
        sequences = []
        for i in range(len(data) - self.seq_length + 1):
            seq = data[i:i+self.seq_length]
            sequences.append(seq)
        return np.array(sequences).reshape(-1, self.seq_length, self.n_features)
    
    def fit(self, data, epochs=50, batch_size=32, validation_split=0.1):
        """Fit the model to the data
        
        Args:
            data: 1D numpy array of time series data
            epochs: Number of training epochs
            batch_size: Training batch size
            validation_split: Fraction of data to use for validation
        """
        # Reshape to (n_samples, n_features) if needed
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
            
        # Create sequences
        sequences = self._create_sequences(data)
        
        # Train the model
        self.model.fit(
            sequences, sequences,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        
        # Calculate reconstruction error and set threshold
        reconstructions = self.model.predict(sequences)
        mse = np.mean(np.square(sequences - reconstructions), axis=(1, 2))
        self.threshold = np.percentile(mse, 95)  # 95th percentile as threshold
        self.is_fitted = True
    
    def predict(self, data):
        """Predict if points are anomalies
        
        Args:
            data: 1D numpy array of time series data
            
        Returns:
            numpy array where 1 is normal, -1 is anomaly
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before prediction")
            
        # Reshape to (n_samples, n_features) if needed
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
            
        # Create sequences
        sequences = self._create_sequences(data)
        
        # Calculate reconstruction error
        reconstructions = self.model.predict(sequences)
        mse = np.mean(np.square(sequences - reconstructions), axis=(1, 2))
        
        # Return predictions (1 for normal, -1 for anomaly)
        predictions = np.ones(len(mse))
        predictions[mse > self.threshold] = -1
        
        return predictions
    
    def anomaly_score(self, data):
        """Calculate anomaly score
        
        Args:
            data: 1D numpy array of time series data
            
        Returns:
            numpy array of anomaly scores (higher = more anomalous)
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before scoring")
            
        # Reshape to (n_samples, n_features) if needed
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
            
        # Create sequences
        sequences = self._create_sequences(data)
        
        # Calculate reconstruction error as anomaly score
        reconstructions = self.model.predict(sequences)
        return np.mean(np.square(sequences - reconstructions), axis=(1, 2))