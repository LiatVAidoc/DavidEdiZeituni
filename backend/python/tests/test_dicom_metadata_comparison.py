"""
Focused test for DICOM file processing and metadata comparison
Tests the specific file against the good_result.json expectations
"""
import json
import os
import sys
import pytest

# Add the parent directory to the Python path to import our services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.dicom_service import DicomService


class TestDicomFileComparison:
    """Test class for comparing DICOM metadata against expected results"""
    
    @classmethod
    def setup_class(cls):
        """Set up test fixtures for the class"""
        cls.dicom_service = DicomService()
        cls.test_file_path = "aidoc-dev-us-102-storage/production/scans/3041983076-1.2.826.0.1.3680043.9.6883.1.24209659964804056971019414433891120/anon-1.2.826.0.1.3680043.9.6883.1.11587754842360809093846306686786710.dcm"
        
        # Load expected results
        test_data_dir = os.path.join(os.path.dirname(__file__), 'data')
        with open(os.path.join(test_data_dir, 'good_result.json'), 'r') as f:
            cls.expected_metadata = json.load(f)
    
    def test_dicom_metadata_matches_expected(self):
        """Test that the extracted DICOM metadata exactly matches the expected result"""
        # Extract metadata from the specified DICOM file
        actual_metadata = self.dicom_service.get_metadata_from_s3(self.test_file_path)
        
        # Assert exact match
        assert actual_metadata == self.expected_metadata, (
            f"DICOM metadata does not match expected result!\n"
            f"Expected: {json.dumps(self.expected_metadata, indent=2)}\n"
            f"Actual:   {json.dumps(actual_metadata, indent=2)}"
        )
        
        print(f"✅ DICOM metadata test passed!")
        print(f"📋 File: {self.test_file_path}")
        print(f"📄 Metadata: {json.dumps(actual_metadata, indent=2)}")


if __name__ == '__main__':
    # Run with pytest-like behavior
    test_instance = TestDicomFileComparison()
    test_instance.setup_class()
    
    try:
        test_instance.test_dicom_metadata_matches_expected()
        print("\n🎉 Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        sys.exit(1)