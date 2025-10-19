"""
Response Handler - Utility for standardizing HTTP responses
"""
from flask import jsonify


class ResponseHandler:
    """Handler for standardizing HTTP responses"""
    
    def success_response(self, data, status_code=200):
        """
        Create a standardized success response
        
        Args:
            data: Response data
            status_code (int): HTTP status code (default: 200)
            
        Returns:
            tuple: JSON response and HTTP status code
        """
        return jsonify(data), status_code
    
    def error_response(self, error_message, status_code=500):
        """
        Create a standardized error response
        
        Args:
            error_message (str): Error message
            status_code (int): HTTP status code (default: 500)
            
        Returns:
            tuple: JSON response and HTTP status code
        """
        return jsonify({"error": error_message}), status_code