from flask import jsonify, request
from backend.api import api_bp
from backend.services.anomaly_detector import AnomalyDetector
from backend.services.data_stream import DataStream

# Initialize services
data_stream = DataStream()
anomaly_detector = AnomalyDetector()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

@api_bp.route('/anomalies', methods=['GET'])
def get_anomalies():
    """Get detected anomalies"""
    # In a real app, this would fetch from database
    return jsonify({'anomalies': []})

@api_bp.route('/data/recent', methods=['GET'])
def get_recent_data():
    """Get recent data points"""
    # In a real app, this would fetch from database
    return jsonify({'data': []})

@api_bp.route('/data/simulate', methods=['POST'])
def simulate_data():
    """Simulate data stream with optional anomalies"""
    params = request.json or {}
    include_anomalies = params.get('include_anomalies', False)
    num_points = params.get('num_points', 100)
    
    # Start data simulation in background
    data_stream.start_simulation(num_points, include_anomalies)
    
    return jsonify({'status': 'simulation_started'})