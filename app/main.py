import streamlit as st
import os
from dotenv import load_dotenv
from services.s3_service import S3Service
from services.llm_service import LLMService
from utils.logger import setup_logger
from PIL import Image

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger()

# Initialize services
s3_service = S3Service()
llm_service = LLMService()

def main():
    st.title("Document Analyzer")
    
    uploaded_file = st.file_uploader("Upload a document", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Document', use_column_width=True)
        
        if st.button('Analyze Document'):
            with st.spinner('Processing...'):
                try:
                    # Analyze with LLM directly
                    logger.info("Starting document analysis")
                    analysis = llm_service.analyze_document(image)
                    
                    # Upload to S3 for storage
                    logger.info(f"Uploading file: {uploaded_file.name}")
                    s3_url = s3_service.upload_file(uploaded_file)
                    
                    # Display results
                    st.success("Analysis Complete!")
                    st.json(analysis)
                    
                except Exception as e:
                    logger.error(f"Error processing document: {str(e)}")
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()