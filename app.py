# app.py
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from config import config
from models import init_app as init_db, get_db
from models.admin import create_default_admin
from utils.email_service import mail
import os

# Initialize extensions
limiter = Limiter(get_remote_address)

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    if config_name in config:
        app.config.from_object(config[config_name])
    else:
        app.config.from_object(config['default'])
    
    # Override with environment variables
    app.config.from_prefixed_env()
    
    # Set upload folder
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'), exist_ok=True)
    
    # Initialize extensions
    CORS(app)
    limiter.init_app(app)
    mail.init_app(app)
    init_db(app)
    
    # Create default admin
    with app.app_context():
        db = get_db()
        create_default_admin(db)
    
    # Register blueprints
    from routes.contact_routes import contact_bp
    from routes.admin_routes import admin_bp
    from routes.content_routes import content_bp
    
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(content_bp)
    
    # Serve uploaded files
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # Serve frontend
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Health check
    @app.route('/api/health')
    def health_check():
        return {'status': 'OK', 'message': 'Blaster3D API is running'}, 200
    
    return app