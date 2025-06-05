from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import os

from backend.api import api_bp
from backend.services.data_stream import DataStream
from backend.services.anomaly_detector import AnomalyDetector
from backend.services.db_service import DatabaseService
import backend.config as config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Set up CORS
CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})

# Set up Socket.IO
socketio = SocketIO(app, cors_allowed_origins=config.CORS_ORIGINS)

# Initialize services
data_stream = DataStream()
anomaly_detector = AnomalyDetector(
    window_size=config.DETECTION_WINDOW_SIZE,
    model_type=config.DEFAULT_MODEL_TYPE
)
db_service = DatabaseService(
    postgres_url=config.POSTGRES_URL,
    redis_url=config.REDIS_URL
)

# Register blueprint
app.register_blueprint(api_bp, url_prefix='/api')

# Set socketio instance in services
data_stream.set_socketio(socketio)
anomaly_detector.set_socketio(socketio)

@app.route('/')
def index():
    return "Anomaly Detection API is running"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('start_stream')
def handle_start_stream(data):
    """Start data stream simulation"""
    num_points = data.get('num_points', 1000)
    include_anomalies = data.get('include_anomalies', True)
    
    # Start data simulation
    data_stream.start_simulation(num_points, include_anomalies)
    
    # Start anomaly detection
    anomaly_detector.start_detection(interval=config.DETECTION_INTERVAL)
    
    return {'status': 'started'}

@socketio.on('stop_stream')
def handle_stop_stream():
    """Stop data stream simulation"""
    data_stream.stop()
    anomaly_detector.stop()
    
    return {'status': 'stopped'}

@socketio.on('data_point')
def handle_data_point(data):
    """Process incoming data point"""
    # Add to anomaly detector
    anomaly_detector.add_data_point(data['value'])
    
    # Store in database (async in production)
    try:
        db_service.store_data_point(
            data['timestamp'],
            data['value'],
            data.get('is_anomaly', False)
        )
    except Exception as e:
        print(f"Error storing data point: {e}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=config.DEBUG)