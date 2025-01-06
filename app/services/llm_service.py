import os
import base64
import requests
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.logger import setup_logger

logger = setup_logger()

class LLMService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-002",
            temperature=0,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
        
        self.analysis_prompt = """
        Analyze this document and provide:
        1. Document type
        2. Key information
        3. Important details
        4. Notable observations
        
        Format the response as structured data.
        """

    def analyze_document(self, image_url: str) -> dict:
        try:
            # Download image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Convert to base64
            image_data = base64.b64encode(response.content).decode("utf-8")
            
            # Prepare content for LLM
            content = [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                },
                {
                    "type": "text",
                    "text": self.analysis_prompt
                }
            ]
            
            # Get analysis
            logger.info("Sending request to LLM")
            result = self.llm.invoke(content)
            
            return {
                "analysis": result.content,
                "timestamp": datetime.now().isoformat(),
                "source_url": image_url
            }
            
        except Exception as e:
            logger.error(f"LLM analysis failed: {str(e)}")
            raise Exception(f"Failed to analyze document: {str(e)}")