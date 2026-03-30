from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from models import db, User 
import os
from dotenv import load_dotenv
# Absolute Blueprint Imports
from blueprints.auth.routes import auth_bp
from blueprints.student.routes import student_bp
from blueprints.teacher.routes import teacher_bp

load_dotenv() 

# Initialize Bcrypt globally
# This object MUST be defined outside the function for the local import to find it
bcrypt = Bcrypt()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')

    db.init_app(app)
    
    # Initialize the global bcrypt object with the app instance
    bcrypt.init_app(app)
    
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    
    # Ensure uploads folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- Register Blueprints ---
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all() 
        # --- Default User Setup ---
        # Use the global 'bcrypt' object directly for hashing
        if not User.query.filter_by(email='teacher@mail.com').first():
            teacher_pw = bcrypt.generate_password_hash('pass').decode('utf-8')
            student_pw = bcrypt.generate_password_hash('pass').decode('utf-8')
            db.session.add_all([
                User(email='teacher@mail.com', password=teacher_pw, is_teacher=True),
                User(email='student@mail.com', password=student_pw, is_teacher=False)
            ])
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)