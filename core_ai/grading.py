import os
from google import genai
from google.genai.errors import APIError
from PIL import Image

# Client initialization uses API key from the environment automatically
client = genai.Client()
MODEL_NAME = "gemini-2.5-flash"

def build_grading_prompt(question):
    return f"""
    You are an expert academic grader. Your task is to automatically evaluate the student's submission shown in the image.
    The student was asked the following question: "{question}".

    Evaluate both the written content (text, labels, and explanations) and the diagram (accuracy, labeling, and completeness) against general scientific and academic knowledge for the given topic. Use a critical, but fair, and professional tone.

    Provide the final grade as a number (0-10) and comprehensive, structured feedback.
    Format your response STRICTLY as follows (DO NOT ADD EXTRA TEXT):
    SCORE:[X]/10
    FEEDBACK:[
    * Diagram Evaluation: [Specific comments on the diagram's accuracy and labeling.]
    * Written Content: [Specific comments on the textual explanation and completeness.]
    * Overall Justification: [A brief summary of why the final score was given.]
    ]
    """

def multimodal_grade_submission(image_path, question):
    if not os.path.exists(image_path):
        return 0.0, f"Error: Image file not found at {image_path}"

    try:
        img = Image.open(image_path)
        prompt = build_grading_prompt(question)
        content = [prompt, img]

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=content,
            config={"temperature": 0.1, "max_output_tokens": 1024}
        )

        text = response.text.strip()
        score_match = [line for line in text.split('\n') if line.startswith('SCORE:')]
        feedback_match = [line for line in text.split('\n') if line.startswith('FEEDBACK:')]

        score = 0.0
        feedback = "Could not parse feedback."

        if score_match:
            try:
                score = float(score_match[0].split('[')[1].split(']/')[0])
            except:
                score = 0.0

        if feedback_match:
            feedback = '\n'.join(text.split('FEEDBACK:')[1].split('\n'))

        # Clean up temporary PNG file if created from PDF
        if "page_1_temp.png" in image_path and os.path.exists(image_path):
            os.remove(image_path)

        return score, feedback

    except APIError as e:
        print(f"Gemini API Error: {e}")
        return 0.0, f"API Error during grading: {e}. Check your GEMINI_API_KEY."
    except Exception as e:
        print(f"General Grading Error: {e}")
        return 0.0, f"An unexpected error occurred: {e}"