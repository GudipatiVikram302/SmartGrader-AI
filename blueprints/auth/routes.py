from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user
from models import User, db 
from flask_bcrypt import Bcrypt 
# REMOVED: from app import bcrypt (This was the source of the circular import)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('teacher.dashboard' if current_user.is_teacher else 'student.portal'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('That email is already registered. Please log in.', 'warning')
        else:
            # CRITICAL FIX: Local import of bcrypt is delayed until this function runs
            from app import bcrypt 
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            is_teacher = (role == 'teacher')

            new_user = User(
                email=email,
                password=hashed_password,
                is_teacher=is_teacher
            )
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account created for {email}! Please log in.', 'success')
            return redirect(url_for('auth.login'))
            
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_teacher:
            return redirect(url_for('teacher.dashboard'))
        return redirect(url_for('student.portal'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        # CRITICAL FIX: Local import of bcrypt is delayed until this function runs
        if user and user.password:
            from app import bcrypt 
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!', 'success')
                if user.is_teacher:
                    return redirect(url_for('teacher.dashboard'))
                return redirect(url_for('student.portal'))

        flash('Login Unsuccessful. Check email and password', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))