import boto3
import os
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger()

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')

    def upload_file(self, file):
        """Upload file to S3 and return the URL"""
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_key = f"uploads/{timestamp}_{file.name}"
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                file_key
            )
            
            # Generate URL
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_key}"
            logger.info(f"File uploaded successfully: {url}")
            return url
            
        except Exception as e:
            logger.error(f"S3 upload failed: {str(e)}")
            raise Exception(f"Failed to upload file to S3: {str(e)}")