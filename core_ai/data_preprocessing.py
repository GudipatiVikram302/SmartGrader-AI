import os
from pdf2image import convert_from_path

def process_uploaded_file(file_path):
    base_name, ext = os.path.splitext(file_path)
    
    if ext.lower() == '.pdf':
        # Requires Poppler installed on the system
        images = convert_from_path(file_path, first_page=1, last_page=1, dpi=300)
        image_path = f"{base_name}_page_1_temp.png"
        images[0].save(image_path, 'PNG')
        return image_path
    
    elif ext.lower() in ['.jpg', '.jpeg', '.png']:
        return file_path
        
    raise ValueError("Unsupported file type. Please upload a PDF, JPG, or PNG.")