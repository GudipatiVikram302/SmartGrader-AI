# File: core_ai/pipline_worker.py

from .nlp_grader import grade_text_content
# from .ocr_processor import extract_text_from_image # Not needed, grader is multimodal

def multimodal_grade_submission(image_for_grading_path: str, question_text: str) -> tuple[float, str]:
    """
    Orchestrates the grading pipeline. It sends the image and rubric directly
    to the multimodal grader, relying on Gemini to perform the internal OCR/CV/NLP.
    """
    
    # 1. Direct Multimodal Grading (Simplification)
    # The grade_text_content function is now fully multimodal.
    score, feedback = grade_text_content(image_for_grading_path, question_text)
    
    return score, feedback