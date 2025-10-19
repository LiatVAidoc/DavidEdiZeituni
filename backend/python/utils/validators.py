"""
Request Validators - Utilities for validating HTTP requests
"""


class DicomRequestValidator:
    """Validator for DICOM-related requests"""
    
    def validate_dicom_metadata_request(self, request):
        """
        Validate request for DICOM metadata extraction
        
        Args:
            request: Flask request object
            
        Returns:
            dict: Validation result with 'valid', 'data', and 'error' keys
        """
        try:
            data = request.get_json()
            
            if not data:
                return {
                    'valid': False,
                    'error': 'Request body must contain JSON data',
                    'data': None
                }
            
            if 'file_path' not in data:
                return {
                    'valid': False,
                    'error': 'file_path is required in request body',
                    'data': None
                }
            
            file_path = data['file_path']
            if not file_path or not isinstance(file_path, str):
                return {
                    'valid': False,
                    'error': 'file_path must be a non-empty string',
                    'data': None
                }
            
            return {
                'valid': True,
                'data': {'file_path': file_path},
                'error': None
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Invalid request format: {str(e)}',
                'data': None
            }