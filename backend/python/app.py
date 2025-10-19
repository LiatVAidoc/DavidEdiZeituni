"""
Flask Application - Main entry point
Responsible only for application configuration and route registration
"""
from flask import Flask, request
from flask_cors import CORS
from controllers.health_controller import HealthController
from controllers.dicom_controller import DicomController

# Initialize Flask app
app = Flask(__name__)

# Configure CORS to allow requests from localhost and common development ports
CORS(app, 
     origins=[
         "http://localhost:3000",    # React default port
         "http://localhost:8080",    # Vue default port
         "http://127.0.0.1:3000",    # React with 127.0.0.1
         "http://127.0.0.1:8080",    # Vue with 127.0.0.1
         "http://localhost:8081",    # Alternative Vue port
         "http://127.0.0.1:8081",    # Alternative Vue port with 127.0.0.1
         "http://localhost:5173",    # Vite default port
         "http://127.0.0.1:5173",    # Vite with 127.0.0.1
         "http://localhost:4173",    # Vite preview port
         "http://127.0.0.1:4173"     # Vite preview with 127.0.0.1
     ],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'Accept', 'X-Requested-With'],
     supports_credentials=True,
     send_wildcard=False)

# Initialize controllers
health_controller = HealthController()
dicom_controller = DicomController()

# Route definitions
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return health_controller.health_check()

@app.route('/api/dicom-metadata', methods=['POST', 'OPTIONS'])
def dicom_metadata():
    """
    DICOM metadata extraction endpoint
    
    Accepts POST requests with an S3 path in the request body
    Downloads the DICOM file from the provided S3 path
    Extracts metadata using the appropriate DICOM library
    Returns the metadata as JSON
    """
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 200
    return dicom_controller.get_dicom_metadata()

if __name__ == '__main__':
    app.run(debug=True)
