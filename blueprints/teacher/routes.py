from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import db, Assignment, User # Ensure User is imported

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_teacher:
        return redirect(url_for('student.portal'))

    # FIX: Use a simple filter and fetch all graded assignments.
    # We rely on the 'submitter' relationship defined in the Assignment model 
    # to access student details (name, roll_no.) in the template.

    assignments = Assignment.query.filter_by(is_graded=True).\
        order_by(Assignment.upload_date.desc()).\
        all()

    # NOTE: The template expects a list of tuples (Assignment, User).
    # Since we changed the query, we must format the results to match the template structure.
    # The teacher_dashboard.html template relies on the previous query structure.
    
    # Let's recreate the expected format for compatibility with teacher_dashboard.html
    assignments_with_users = []
    for assignment in assignments:
        # assignment.submitter accesses the related User object automatically
        assignments_with_users.append((assignment, assignment.submitter))


    return render_template('teacher_dashboard.html', assignments=assignments_with_users)