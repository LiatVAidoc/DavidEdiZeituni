import json
import os
import sys

# Add the parent directory to the Python path to import our services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from services.dicom_service import DicomService


def test_health_endpoint():
    """Test the health check endpoint"""
    test_app = app.test_client()
    test_app.testing = True
    
    response = test_app.get('/health')
    assert response.status_code == 200


def test_dicom_service_metadata_extraction():
    """Test DICOM service metadata extraction against known good result"""
    # Initialize service
    dicom_service = DicomService()
    
    # Test file path
    test_file_path = "aidoc-dev-us-102-storage/production/scans/3041983076-1.2.826.0.1.3680043.9.6883.1.24209659964804056971019414433891120/anon-1.2.826.0.1.3680043.9.6883.1.11587754842360809093846306686786710.dcm"
    
    # Load expected results
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')
    with open(os.path.join(test_data_dir, 'good_result.json'), 'r') as f:
        expected_metadata = json.load(f)
    
    # Extract actual metadata
    actual_metadata = dicom_service.get_metadata_from_s3(test_file_path)
    
    # Assert they match
    assert actual_metadata == expected_metadata, (
        f"DICOM metadata mismatch!\n"
        f"Expected: {expected_metadata}\n"
        f"Actual: {actual_metadata}"
    )