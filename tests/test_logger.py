from app.utils.logger import setup_logger
import logging

def test_logger_setup():
    """Test logger initialization and configuration"""
    logger = setup_logger()
    
    assert logger.name == 'visual_insight'
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)