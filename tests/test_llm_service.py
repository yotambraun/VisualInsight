from app.services.llm_service import LLMService
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

def test_llm_service_init(mock_env_vars):
    """Test LLMService initialization"""
    service = LLMService()
    assert service.prompt is not None

@patch('google.generativeai.GenerativeModel')
def test_analyze_document(mock_genai, mock_env_vars, sample_image):
    """Test document analysis with mocked Gemini response"""
    mock_response = MagicMock()
    mock_response.text = "Test analysis result"
    mock_genai.return_value.generate_content.return_value = mock_response
    
    service = LLMService()
    result = service.analyze_document(sample_image)
    
    assert 'analysis' in result
    assert 'timestamp' in result
    assert result['analysis'] == "Test analysis result"
