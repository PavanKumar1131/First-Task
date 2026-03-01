# app.py - main application file
# this is the entry point for the flask app

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import db, User
from auth import auth
from tasks import tasks_bp
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # configuration - using environment variables for security
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///productivity.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # initialize database
    db.init_app(app)
    
    # setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(tasks_bp)
    
    # create tables if they don't exist
    with app.app_context():
        db.create_all()
        # create exports folder if needed
        if not os.path.exists('exports'):
            os.makedirs('exports')
    
    return app


# create the app instance
app = create_app()


# root redirect
@app.route('/')
def index():
    return redirect(url_for('auth.login'))


# run the app
if __name__ == '__main__':
    # debug mode for development
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
