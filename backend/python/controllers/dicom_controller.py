"""
DICOM Controller - Handles HTTP requests for DICOM operations
"""
from flask import request, jsonify
from services.dicom_service import DicomService
from services.s3_dicom_downloader import S3DicomDownloader
from services.dicom_parser import DicomParser
from utils.validators import DicomRequestValidator
from utils.response_handler import ResponseHandler


class DicomController:
    """Controller responsible for handling DICOM-related HTTP requests"""
    
    def __init__(self):
        downloader = S3DicomDownloader()
        parser = DicomParser()
        self.dicom_service = DicomService(downloader=downloader, parser=parser)
        self.validator = DicomRequestValidator()
        self.response_handler = ResponseHandler()
    
    def get_dicom_metadata(self):
        """
        Handle POST request to extract DICOM metadata from S3 file
        
        Returns:
            tuple: JSON response and HTTP status code
        """
        try:
            # Validate request
            validation_result = self.validator.validate_dicom_metadata_request(request)
            if not validation_result['valid']:
                return self.response_handler.error_response(
                    validation_result['error'], 
                    400
                )
            
            file_path = validation_result['data']['file_path']
            
            # Get metadata through service
            metadata = self.dicom_service.get_metadata_from_s3(file_path)
            
            return self.response_handler.success_response(metadata)
            
        except Exception as e:
            return self.response_handler.error_response(str(e), 500)