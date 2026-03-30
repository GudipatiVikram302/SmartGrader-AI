from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import uuid

# --- UPDATED IMPORTS FOR NEW AI PIPELINE ---
from core_ai.pipline_worker import multimodal_grade_submission
from core_ai.file_utils import process_uploaded_file 
# ------------------------------------------

from models import db, Assignment

student_bp = Blueprint('student', __name__)

def allowed_file(filename):
    # Ensure this list matches the ALLOWED_EXTENSIONS in your config.py
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', ['pdf', 'png', 'jpg', 'jpeg'])

@student_bp.route('/portal', methods=['GET'])
@login_required
def portal():
    if current_user.is_teacher:
        return redirect(url_for('teacher.dashboard'))
        
    student_assignments = Assignment.query.filter_by(user_id=current_user.id).order_by(Assignment.upload_date.desc()).all()
    return render_template('student_portal.html', assignments=student_assignments)

@student_bp.route('/upload', methods=['POST'])
@login_required
def upload_assignment():
    if current_user.is_teacher:
        flash("Teachers cannot upload assignments.", "warning")
        return redirect(url_for('teacher.dashboard'))
        
    # --- Retrieve All Form Fields ---
    student_name = request.form.get('student_name')
    roll_number = request.form.get('roll_number')
    title = request.form.get('title')
    question_text = request.form.get('question_text') 

    if 'assignment_file' not in request.files or not student_name or not roll_number or not title or not question_text:
        flash('Missing student details, title, question text, or assignment file.', 'danger')
        return redirect(url_for('student.portal'))

    file = request.files['assignment_file']

    if file.filename == '' or not allowed_file(file.filename):
        flash('Invalid or no selected file.', 'danger')
        return redirect(url_for('student.portal'))
        
    # 1. Save File to Disk
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = str(uuid.uuid4()) + '.' + file_ext
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(upload_path)
    
    try:
        # 2. Process the file (convert PDF to JPG if needed)
        image_for_grading_path = process_uploaded_file(upload_path)
        
        # 3. Multimodal Grading (The AI Call)
        score, feedback = multimodal_grade_submission(image_for_grading_path, question_text)

        # 4. Save Results to Database
        new_assignment = Assignment(
            user_id=current_user.id,
            student_name=student_name, 
            roll_number=roll_number,   
            title=title,              
            question_text=question_text, 
            file_path=upload_path,
            grade_score=score,
            feedback=feedback,
            is_graded=True # Mark as graded since AI processing completed
        )
        db.session.add(new_assignment)
        db.session.commit()
        
        flash(f'Assignment submitted and graded! Score: {score}/10', 'success')

    except RuntimeError as e:
        # Catch PDF conversion errors
        flash(f'Submission failed due to processing error: {e}', 'danger')
        # Clean up the original file if processing failed
        if os.path.exists(upload_path):
            os.remove(upload_path)
    except Exception as e:
        # Catch all other exceptions (including AI API errors)
        flash(f'Submission failed: {feedback if "API" in str(e) else "An unexpected error occurred."}', 'danger')
        current_app.logger.error(f"Error during grading or saving: {e}")


    return redirect(url_for('student.portal'))