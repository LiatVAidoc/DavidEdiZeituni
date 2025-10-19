"""
DICOM Service - Handles DICOM file processing operations
Combines downloading and metadata parsing functionality
"""
import os
import tempfile
from services.s3_dicom_downloader import S3DicomDownloader
from services.dicom_parser import DicomParser


class DicomService:
    """Service responsible for DICOM file operations"""
    
    def __init__(self, downloader=None, parser=None):
        """
        Initialize DICOM service with dependency injection support
        
        Args:
            downloader: DICOM downloader instance (defaults to S3DicomDownloader)
            parser: DICOM parser instance (defaults to DicomParser)
        """
        self.downloader = downloader if downloader is not None else S3DicomDownloader()
        self.parser = parser if parser is not None else DicomParser()
    
    def get_metadata_from_s3(self, file_path):
        """
        Downloads DICOM file from S3 and extracts metadata
        
        Args:
            file_path (str): S3 path to the DICOM file
            
        Returns:
            dict: Parsed DICOM metadata
            
        Raises:
            Exception: If download or parsing fails
        """
        # Create temporary file for downloaded DICOM
        with tempfile.NamedTemporaryFile(suffix='.dcm', delete=False) as temp_file:
            temp_file_path = temp_file.name
        
        try:
            # Download DICOM file from S3
            self.downloader.download_dicom_file(file_path, temp_file_path)
            
            # Parse metadata from downloaded file
            metadata = self.parser.parse_metadata(temp_file_path)
            
            return metadata
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    def download_and_save_dicom(self, s3_file_path, local_save_path):
        """
        Downloads DICOM file from S3 and saves it to a local path
        
        Args:
            s3_file_path (str): S3 path to the DICOM file
            local_save_path (str): Local path where to save the file
            
        Returns:
            str: Path where the file was saved
            
        Raises:
            Exception: If download fails
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(local_save_path), exist_ok=True)
        
        # Download DICOM file from S3
        self.downloader.download_dicom_file(s3_file_path, local_save_path)
        
        return local_save_path