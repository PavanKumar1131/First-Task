# models.py - database models for the productivity tracker
# using SQLAlchemy ORM for sqlite database

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# user model for authentication
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # relationship with tasks
    tasks = db.relationship('Task', backref='owner', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'


# task model - main feature of the app
class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='Personal')
    status = db.Column(db.String(20), default='Pending')  # Pending or Completed
    time_spent = db.Column(db.Integer, default=0)  # time in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    # helper to get time in readable format
    def get_formatted_time(self):
        hours = self.time_spent // 3600
        minutes = (self.time_spent % 3600) // 60
        seconds = self.time_spent % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# category options - kept simple
CATEGORIES = ['Work', 'Study', 'Personal', 'Health', 'Other']
