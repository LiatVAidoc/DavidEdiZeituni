from abc import ABC, abstractmethod


class DicomDownloader(ABC):
    """Abstract base class for DICOM file downloaders."""
    
    @abstractmethod
    def download(self, source_path: str, dest_path: str) -> None:
        """
        Downloads a DICOM file from source to destination.
        
        Parameters:
        - source_path: The source path/identifier for the DICOM file
        - dest_path: The destination path where the file should be saved
        """
        pass

