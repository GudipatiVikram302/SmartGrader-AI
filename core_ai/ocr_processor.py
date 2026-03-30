from google import genai
from PIL import Image # <-- Added missing import
from flask import current_app
import os

def extract_text_from_image(image_path: str) -> str:
    """Uses Gemini to perform OCR and extract all text from the image."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        current_app.logger.error("API Key not set for OCR.")
        return "OCR Failed: API Key Missing."

    try:
        # Client initialization is often moved out of the function, but for robustness:
        client = genai.Client(api_key=api_key)
        
        # Ensure the image path is valid before opening
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at path: {image_path}")
            
        img = Image.open(image_path)
        
        # Prompt instructing Gemini to act as an OCR engine
        prompt = "Transcribe all handwritten and typed text from this image accurately, preserving numbered lists and formatting."

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img]
        )
        return response.text
        
    except Exception as e:
        current_app.logger.error(f"OCR Processor Error: {e}")
        # Return specific error feedback to the user
        return f"OCR Failed: {e}"