# auth.py - handles user authentication routes
# login, register, logout functionality

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('tasks_bp.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # find user by email
        user = User.query.filter_by(email=email).first()
        
        # check if user exists and password is correct
        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('auth.login'))
        
        # login successful
        login_user(user, remember=remember)
        flash('Welcome back!', 'success')
        return redirect(url_for('tasks_bp.dashboard'))
    
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('tasks_bp.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # basic validation
        if not username or not email or not password:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('auth.register'))
        
        # checking password match
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))
        
        # checking if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Try logging in.', 'error')
            return redirect(url_for('auth.register'))
        
        # check username too
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken.', 'error')
            return redirect(url_for('auth.register'))
        
        # create new user with hashed password
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        
        # save to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
