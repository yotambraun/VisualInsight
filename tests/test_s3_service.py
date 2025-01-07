import pytest
from app.services.s3_service import S3Service
import io


def test_s3_service_init(mock_env_vars):
    """Test S3Service initialization"""
    service = S3Service()
    assert service.bucket_name == 'test-bucket'

@mock_s3
def test_upload_file(mock_env_vars, mock_s3_client, sample_image):
    """Test file upload to S3"""
    service = S3Service()
    
    # Convert PIL Image to file-like object
    img_byte_arr = io.BytesIO()
    sample_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    img_byte_arr.name = 'test.png'
    
    url = service.upload_file(img_byte_arr)
    assert 'test-bucket' in url
    assert '.png' in url