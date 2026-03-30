from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from flask_bcrypt import Bcrypt 

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_teacher = db.Column(db.Boolean, default=False)
    assignments = db.relationship('Assignment', backref='submitter', lazy=True)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # --- STUDENT DETAILS AND TITLE ---
    student_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    # --- END NEW FIELDS ---
    question_text = db.Column(db.String(500), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    grade_score = db.Column(db.Float, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    is_graded = db.Column(db.Boolean, default=False)