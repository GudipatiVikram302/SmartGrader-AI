import os
import uuid
from flask import current_app
from PIL import Image
import fitz # PyMuPDF: used for PDF processing

def process_uploaded_file(file_path):
    """
    Processes the uploaded file (PDF or Image). 
    If PDF, converts the first page to a JPG image.
    The path to the image ready for grading is returned.
    """
    if not os.path.exists(file_path):
        # This should ideally not happen if file upload succeeded
        raise FileNotFoundError(f"File not found at path: {file_path}")

    filename, file_ext = os.path.splitext(file_path)
    file_ext = file_ext.lower()
    
    # 1. Handle PDF Conversion
    if file_ext == '.pdf':
        try:
            doc = fitz.open(file_path)
            if doc.page_count == 0:
                raise ValueError("PDF has no pages.")

            # Load the first page
            page = doc.load_page(0)
            
            # Render page to a pixmap
            pix = page.get_pixmap() 
            
            # Save the image as JPG in the UPLOAD_FOLDER
            output_filename = str(uuid.uuid4()) + '.jpg'
            output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], output_filename)
            pix.save(output_path)
            
            doc.close()
            return output_path
        
        except Exception as e:
            current_app.logger.error(f"Error processing PDF file: {e}")
            raise RuntimeError(f"Failed to process PDF: {e}")
    
    # 2. Handle Image Files (JPG, JPEG, PNG)
    elif file_ext in ['.jpg', '.jpeg', '.png']:
        return file_path
    
    else:
        raise ValueError("Unsupported file format for grading.")