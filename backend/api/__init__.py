from flask import Blueprint

# Create blueprint for API routes
api_bp = Blueprint('api', __name__)

# Import routes
from backend.api import routes