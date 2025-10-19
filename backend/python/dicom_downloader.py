import boto3
import json
import os

# Get the directory of the current script and build path to secrets.json
current_dir = os.path.dirname(os.path.abspath(__file__))
secrets_path = os.path.join(current_dir, 'keys', 'secrets.json')

with open(secrets_path) as r:
    aws_secrets = json.loads(r.read())  

class S3DicomDownloader:
    def __init__(self):
        self.s3 = boto3.client('s3', region_name=aws_secrets["REGION"],
                         aws_access_key_id=aws_secrets["AWS_ACCESS_KEY_ID"],
                         aws_secret_access_key=aws_secrets["AWS_SECRET_ACCESS_KEY"],
                         aws_session_token=aws_secrets["AWS_SESSION_TOKEN"])

    def download_dicom_file(self, s3_path, local_file_path):
        """
        Downloads a DICOM file from S3 to a local file path.

        Parameters:
        - s3_path: The S3 object path (e.g., 'BUCKET_NAME/folder/subfolder/dicomfile.dcm').
        - local_file_path: The local file path to save the DICOM file (e.g., '/local/path/dicomfile.dcm').
        """
        # Parse bucket name and key from s3_path
        if '/' not in s3_path:
            raise ValueError("Invalid S3 path format. Expected format: 'bucket_name/key'")
        
        parts = s3_path.split('/', 1)
        bucket_name = parts[0]
        key = parts[1]
        
        try:
            # Download file from S3
            self.s3.download_file(bucket_name, key, local_file_path)
        except Exception as e:
            raise Exception(f"Failed to download DICOM file from S3: {str(e)}")

