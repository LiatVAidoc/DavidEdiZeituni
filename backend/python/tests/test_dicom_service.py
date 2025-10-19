"""
Test cases for DicomService
Tests DICOM file downloading and metadata parsing functionality
"""
import json
import os
import tempfile
import unittest
import sys

# Add the parent directory to the Python path to import our services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.dicom_service import DicomService


class TestDicomService(unittest.TestCase):
    """Test cases for DicomService class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.dicom_service = DicomService()
        self.test_file_path = "aidoc-dev-us-102-storage/production/scans/3041983076-1.2.826.0.1.3680043.9.6883.1.24209659964804056971019414433891120/anon-1.2.826.0.1.3680043.9.6883.1.11587754842360809093846306686786710.dcm"
        
        # Load expected results
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'data')
        with open(os.path.join(self.test_data_dir, 'good_result.json'), 'r') as f:
            self.expected_metadata = json.load(f)
    
    def test_get_metadata_from_s3(self):
        """Test downloading DICOM file from S3 and extracting metadata"""
        try:
            # Get metadata using the service
            actual_metadata = self.dicom_service.get_metadata_from_s3(self.test_file_path)
            
            # Verify that we got some metadata
            self.assertIsInstance(actual_metadata, dict)
            self.assertGreater(len(actual_metadata), 0)
            
            # Compare with expected results
            self.assertEqual(actual_metadata, self.expected_metadata, 
                           f"Metadata mismatch!\nExpected: {self.expected_metadata}\nActual: {actual_metadata}")
            
            print(f"✅ Metadata extraction test passed!")
            print(f"📋 Extracted metadata: {actual_metadata}")
            
        except Exception as e:
            self.fail(f"Failed to extract metadata: {str(e)}")
    
    def test_download_and_save_dicom(self):
        """Test downloading and saving DICOM file permanently"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Define local save path
            local_file_path = os.path.join(temp_dir, 'test_dicom.dcm')
            
            try:
                # Download and save the file
                saved_path = self.dicom_service.download_and_save_dicom(
                    self.test_file_path, 
                    local_file_path
                )
                
                # Verify file was saved
                self.assertEqual(saved_path, local_file_path)
                self.assertTrue(os.path.exists(saved_path))
                
                # Verify file has content
                file_size = os.path.getsize(saved_path)
                self.assertGreater(file_size, 0)
                
                print(f"✅ File download test passed!")
                print(f"📄 File saved to: {saved_path}")
                print(f"📊 File size: {file_size:,} bytes")
                
            except Exception as e:
                self.fail(f"Failed to download and save file: {str(e)}")
    
    def test_metadata_consistency(self):
        """Test that metadata is consistent across multiple extractions"""
        try:
            # Extract metadata twice
            metadata1 = self.dicom_service.get_metadata_from_s3(self.test_file_path)
            metadata2 = self.dicom_service.get_metadata_from_s3(self.test_file_path)
            
            # Verify consistency
            self.assertEqual(metadata1, metadata2, 
                           "Metadata should be consistent across multiple extractions")
            
            print("✅ Metadata consistency test passed!")
            
        except Exception as e:
            self.fail(f"Failed consistency test: {str(e)}")
    
    def test_metadata_fields_presence(self):
        """Test that all expected metadata fields are present"""
        try:
            metadata = self.dicom_service.get_metadata_from_s3(self.test_file_path)
            
            # Check that all expected fields are present
            expected_fields = set(self.expected_metadata.keys())
            actual_fields = set(metadata.keys())
            
            missing_fields = expected_fields - actual_fields
            extra_fields = actual_fields - expected_fields
            
            self.assertEqual(len(missing_fields), 0, 
                           f"Missing expected fields: {missing_fields}")
            
            # Extra fields are okay, but we should log them
            if extra_fields:
                print(f"ℹ️  Extra fields found (not in expected): {extra_fields}")
            
            print("✅ Metadata fields presence test passed!")
            
        except Exception as e:
            self.fail(f"Failed fields presence test: {str(e)}")


def run_dicom_service_tests():
    """Function to run all DICOM service tests with detailed output"""
    print("🧪 Running DICOM Service Tests")
    print("=" * 80)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDicomService)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    if result.wasSuccessful():
        print("🎉 All tests passed successfully!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        
        # Print failure details
        for test, traceback in result.failures:
            print(f"\n❌ FAILURE in {test}:")
            print(traceback)
        
        for test, traceback in result.errors:
            print(f"\n💥 ERROR in {test}:")
            print(traceback)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Run the tests
    success = run_dicom_service_tests()
    sys.exit(0 if success else 1)