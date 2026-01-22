"""Application factory and extensions initialization."""
import os
from flask import Flask
from flask_login import LoginManager
from app.config import config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.config['INSTANCE_PATH'], exist_ok=True)
    except OSError:
        pass
    
    # Initialize extensions
    login_manager.init_app(app)
    
    # Initialize database
    from app.models import database
    database.init_db(app.config['DATABASE_PATH'])
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.get_by_id(int(user_id))
    
    # Register blueprints
    from app.routes import auth, main, transactions
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(transactions.bp)
    
    # Register error handlers
    from app.routes import errors
    app.register_blueprint(errors.bp)
    
    return app