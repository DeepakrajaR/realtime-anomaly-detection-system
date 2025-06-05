import time
import numpy as np
import threading
from datetime import datetime
from flask_socketio import emit

class DataStream:
    """Service for generating and streaming data"""
    
    def __init__(self, socketio=None):
        """Initialize the data stream service
        
        Args:
            socketio: SocketIO instance for emitting events
        """
        self.socketio = socketio
        self.simulation_thread = None
        self.stop_simulation = False
        
    def set_socketio(self, socketio):
        """Set the SocketIO instance
        
        Args:
            socketio: SocketIO instance
        """
        self.socketio = socketio
        
    def generate_normal_data(self, n_points=1, n_features=1):
        """Generate normal data points
        
        Args:
            n_points: Number of data points to generate
            n_features: Number of features per data point
            
        Returns:
            numpy array of shape (n_points, n_features)
        """
        # Generate simple sine wave with noise
        t = np.linspace(0, 2*np.pi, n_points)
        data = np.sin(t).reshape(-1, 1)
        
        # Add noise
        noise = np.random.normal(0, 0.1, (n_points, n_features))
        data = data + noise
        
        return data
    
    def generate_anomaly_data(self, n_points=1, n_features=1):
        """Generate anomaly data points
        
        Args:
            n_points: Number of data points to generate
            n_features: Number of features per data point
            
        Returns:
            numpy array of shape (n_points, n_features)
        """
        # Generate outliers
        data = np.random.normal(0, 0.5, (n_points, n_features))
        
        # Shift data to create clear anomalies
        shift = np.random.choice([-2, 2], size=(n_points, n_features))
        data = data + shift
        
        return data
    
    def _simulate_stream(self, n_points=1000, include_anomalies=True):
        """Simulate a data stream
        
        Args:
            n_points: Total number of points to simulate
            include_anomalies: Whether to include anomalies
        """
        # Reset stop flag
        self.stop_simulation = False
        
        # Generate data
        for i in range(n_points):
            if self.stop_simulation:
                break
                
            # Randomly insert anomalies (about 5% of points)
            is_anomaly = include_anomalies and np.random.random() < 0.05
            
            if is_anomaly:
                data_point = self.generate_anomaly_data(1, 1)[0]
            else:
                data_point = self.generate_normal_data(1, 1)[0]
                
            # Create data point with timestamp
            timestamp = datetime.utcnow().isoformat()
            point = {
                'timestamp': timestamp,
                'value': float(data_point[0]),
                'is_anomaly': bool(is_anomaly)
            }
            
            # Emit data point through Socket.IO
            if self.socketio:
                self.socketio.emit('data_point', point)
                
            # Short delay to simulate real-time data
            time.sleep(0.1)
    
    def start_simulation(self, n_points=1000, include_anomalies=True):
        """Start data simulation in a background thread
        
        Args:
            n_points: Total number of points to simulate
            include_anomalies: Whether to include anomalies
        """
        # Stop any existing simulation
        self.stop_simulation = True
        if self.simulation_thread and self.simulation_thread.is_alive():
            self.simulation_thread.join(timeout=1.0)
            
        # Start new simulation thread
        self.simulation_thread = threading.Thread(
            target=self._simulate_stream,
            args=(n_points, include_anomalies)
        )
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
        
    def stop(self):
        """Stop the data simulation"""
        self.stop_simulation = True