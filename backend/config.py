import os

# Flask configuration
DEBUG = os.environ.get('FLASK_ENV') == 'development'
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

# Database configuration
POSTGRES_URL = os.environ.get('TIMESCALEDB_URL', 'postgres://postgres:postgres@localhost:5432/anomaly_detection')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Anomaly detection configuration
DETECTION_WINDOW_SIZE = 100
DETECTION_INTERVAL = 1.0  # seconds
DEFAULT_MODEL_TYPE = 'isolation_forest'  # 'isolation_forest' or 'lstm'

# API configuration
CORS_ORIGINS = ['http://localhost:3000']  # Frontend URL