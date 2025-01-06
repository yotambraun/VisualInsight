import google.generativeai as genai
import os
from datetime import datetime
from PIL import Image
from utils.logger import setup_logger

logger = setup_logger()

class LLMService:
    def __init__(self):
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash-002')
        
        self.prompt = """
        Analyze this document and provide:
        1. Document type
        2. Key information
        3. Important details
        4. Notable observations
        """

    def analyze_document(self, image: Image.Image) -> dict:
        try:
            logger.info("Sending request to LLM")
            # Generate content directly with the PIL image
            response = self.model.generate_content([
                self.prompt, 
                image
            ])
            
            return {
                "analysis": response.text,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"LLM analysis failed: {str(e)}")
            raise Exception(f"Failed to analyze document: {str(e)}")