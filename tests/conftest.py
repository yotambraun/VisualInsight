import pytest
from PIL import Image
import io
import boto3
import os
from moto import mock_s3
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_env_vars():
    """Fixture to set up test environment variables"""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test-key'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret'
    os.environ['AWS_REGION'] = 'us-east-1'
    os.environ['S3_BUCKET_NAME'] = 'test-bucket'
    os.environ['GOOGLE_API_KEY'] = 'test-api-key'

@pytest.fixture
def sample_image():
    """Fixture to create a sample PIL Image for testing"""
    img = Image.new('RGB', (100, 100), color='red')
    return img

@pytest.fixture
def mock_s3_client():
    """Fixture to mock S3 client using moto"""
    with mock_s3():
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        yield s3