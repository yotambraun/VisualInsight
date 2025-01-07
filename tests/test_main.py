import pytest
from unittest.mock import patch, MagicMock
import streamlit as st
from app.main import main

@pytest.mark.skip(reason="Streamlit tests require special handling")
def test_main_flow():
    """Test main application flow"""
    with patch('streamlit.file_uploader') as mock_uploader, \
         patch('streamlit.button') as mock_button, \
         patch('services.s3_service.S3Service') as mock_s3, \
         patch('services.llm_service.LLMService') as mock_llm:
        
        # Mock file upload
        mock_file = MagicMock()
        mock_file.name = 'test.png'
        mock_uploader.return_value = mock_file
        
        # Mock analyze button
        mock_button.return_value = True
        
        # Mock services
        mock_llm.return_value.analyze_document.return_value = {
            'analysis': 'Test analysis',
            'timestamp': '2024-01-01T00:00:00'
        }
        mock_s3.return_value.upload_file.return_value = 'https://test-url'
        
        main()
