from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'online',
        'message': 'Anomaly Detection API is running'
    })

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)