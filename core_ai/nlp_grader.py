from google import genai
from flask import current_app
import os
import json
from PIL import Image # <-- Added missing import

def grade_text_content(image_path: str, question_text: str) -> tuple[float, str]:
    """
    Uses Gemini's multimodal ability to grade the submission. 
    It grades the text content (NLP) and any diagrams (CV) against the rubric.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        current_app.logger.error("API Key not set for NLP Grader.")
        return 0.0, "NLP Grading Failed: API Key Missing."

    try:
        client = genai.Client(api_key=api_key)
        
        # Ensure the image path is valid before opening
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at path: {image_path}")
            
        img = Image.open(image_path) # Pass the image here for full multimodal power

        prompt = (
            "You are an AI grader. Evaluate the attached student submission image against the "
            "provided rubric/question text. You MUST assess factual correctness, clarity, "
            "completeness of text, AND **accuracy/relevance of any diagrams or visual elements if present.** "
            "Provide the feedback in **exactly two concise sentences (maximum 25 words total).** "
            "Return a score out of 10 and the feedback.\n\n"
            "RUBRIC/QUESTION:\n---\n"
            f"{question_text}\n---\n\n"
            "Respond ONLY with a single JSON object: "
            '{"score": [YOUR_SCORE_OUT_OF_10], "feedback": "[YOUR_FEEDBACK_TEXT]"}'
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img], # Send both text and image
            config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "object",
                    "properties": {"score": {"type": "number"}, "feedback": {"type": "string"}},
                    "required": ["score", "feedback"]
                },
                "temperature": 0.0,
            }
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img], # Send both text and image
            config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "object",
                    "properties": {"score": {"type": "number"}, "feedback": {"type": "string"}},
                    "required": ["score", "feedback"]
                },
            }
        )

        # The model returns a string that must be parsed as JSON
        result = json.loads(response.text)
        score = float(result.get("score", 0.0))
        feedback = result.get("feedback", "NLP Grading Failed.")
        return max(0.0, min(10.0, score)), feedback

    except Exception as e:
        current_app.logger.error(f"NLP Grader Error: {e}")
        # Return specific error feedback to the user
        return 0.0, f"NLP Grading Failed: {e}"