"""
Health Controller - Handles health check requests
"""
from utils.response_handler import ResponseHandler


class HealthController:
    """Controller responsible for handling health check requests"""
    
    def __init__(self):
        self.response_handler = ResponseHandler()
    
    def health_check(self):
        """
        Handle GET request for health check
        
        Returns:
            tuple: JSON response and HTTP status code
        """
        return self.response_handler.success_response(
            {"message": "The server is running"}
        )