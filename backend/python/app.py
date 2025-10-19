from flask import Flask, request, jsonify
from flask_cors import CORS
from dicom_parser import DicomParser
from dicom_downloader import S3DicomDownloader
import os
import tempfile

app = Flask(__name__)

# Configure CORS to allow requests from localhost
CORS(app, origins=[
    "http://localhost:3000",  # React default port
    "http://localhost:8080"  # Vue default port
])

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"message": "The server is running"}), 200

# /api/dicom-metadata
# Accepts POST requests with an S3 path in the request body
# Downloads the DICOM file from the provided S3 path
# Extracts metadata using the appropriate DICOM library
# Returns the metadata as JSON
@app.route('/api/dicom-metadata', methods=['POST'])
def dicom_metadata():
    try:
        # Get the file_path from request JSON
        data = request.get_json()
        if not data or 'file_path' not in data:
            return jsonify({"error": "file_path is required in request body"}), 400
        
        file_path = data['file_path']
        
        # Create temporary file for downloaded DICOM
        with tempfile.NamedTemporaryFile(suffix='.dcm', delete=False) as temp_file:
            temp_file_path = temp_file.name
        
        try:
            # Download DICOM file from S3
            downloader = S3DicomDownloader()
            downloader.download_dicom_file(file_path, temp_file_path)
            
            # Parse metadata from downloaded file
            metadata = DicomParser.parse_metadata(temp_file_path)
            
            return jsonify(metadata), 200
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
