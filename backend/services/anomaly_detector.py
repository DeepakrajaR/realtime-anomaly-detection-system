import numpy as np
import threading
import time
from collections import deque
from backend.ml_models.isolation_forest import AnomalyIsolationForest
from backend.ml_models.lstm_detector import LSTMAnomalyDetector

class AnomalyDetector:
    """Service for detecting anomalies in data streams"""
    
    def __init__(self, window_size=100, model_type='isolation_forest', socketio=None):
        """Initialize the anomaly detector service
        
        Args:
            window_size: Size of the sliding window for detection
            model_type: Type of anomaly detection model ('isolation_forest' or 'lstm')
            socketio: SocketIO instance for emitting events
        """
        self.window_size = window_size
        self.model_type = model_type
        self.socketio = socketio
        
        # Initialize data buffer
        self.data_buffer = deque(maxlen=window_size)
        
        # Initialize models
        self.isolation_forest = AnomalyIsolationForest(contamination=0.05)
        self.lstm_detector = LSTMAnomalyDetector(seq_length=10, n_features=1)
        
        # Initialize detection thread
        self.detection_thread = None
        self.stop_detection = False
        
    def set_socketio(self, socketio):
        """Set the SocketIO instance
        
        Args:
            socketio: SocketIO instance
        """
        self.socketio = socketio
        
    def add_data_point(self, value):
        """Add a data point to the buffer
        
        Args:
            value: Numeric value of the data point
        """
        self.data_buffer.append(value)
        
    def _get_model(self):
        """Get the selected anomaly detection model
        
        Returns:
            Anomaly detection model instance
        """
        if self.model_type == 'isolation_forest':
            return self.isolation_forest
        elif self.model_type == 'lstm':
            return self.lstm_detector
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def detect_anomalies(self, data=None):
        """Detect anomalies in the data
        
        Args:
            data: numpy array of data points (uses buffer if None)
            
        Returns:
            Tuple of (data, predictions, scores)
        """
        # Use provided data or buffer
        if data is None:
            if len(self.data_buffer) < 10:  # Need enough data
                return None, None, None
            data = np.array(list(self.data_buffer))
        
        # Get the model
        model = self._get_model()
        
        # Fit the model if not fitted
        if not model.is_fitted:
            model.fit(data)
            
        # Get predictions and scores
        predictions = model.predict(data)
        scores = model.anomaly_score(data)
        
        return data, predictions, scores
    
    def _detection_loop(self, interval=1.0):
        """Run continuous anomaly detection
        
        Args:
            interval: Seconds between detection runs
        """
        # Reset stop flag
        self.stop_detection = False
        
        while not self.stop_detection:
            # Skip if not enough data
            if len(self.data_buffer) < 10:
                time.sleep(interval)
                continue
                
            # Run detection
            data, predictions, scores = self.detect_anomalies()
            
            # Skip if detection failed
            if data is None or predictions is None:
                time.sleep(interval)
                continue
                
            # Find anomalies
            anomaly_indices = np.where(predictions == -1)[0]
            
            # Emit results if anomalies found
            if len(anomaly_indices) > 0 and self.socketio:
                # Get most recent anomaly
                latest_idx = anomaly_indices[-1]
                latest_score = float(scores[latest_idx])
                
                # Emit anomaly event
                self.socketio.emit('anomaly_detected', {
                    'index': int(latest_idx),
                    'value': float(data[latest_idx]),
                    'score': latest_score,
                    'threshold': self.isolation_forest.threshold if self.model_type == 'isolation_forest' else self.lstm_detector.threshold
                })
                
            # Short delay
            time.sleep(interval)
    
    def start_detection(self, interval=1.0):
        """Start anomaly detection in a background thread
        
        Args:
            interval: Seconds between detection runs
        """
        # Stop any existing detection
        self.stop_detection = True
        if self.detection_thread and self.detection_thread.is_alive():
            self.detection_thread.join(timeout=1.0)
            
        # Start new detection thread
        self.detection_thread = threading.Thread(
            target=self._detection_loop,
            args=(interval,)
        )
        self.detection_thread.daemon = True
        self.detection_thread.start()
        
    def stop(self):
        """Stop the anomaly detection"""
        self.stop_detection = True