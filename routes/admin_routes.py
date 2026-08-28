# routes/admin_routes.py
from flask import Blueprint, request, jsonify, render_template, send_from_directory
from models.admin import AdminModel, create_default_admin
from models import get_db
from utils.auth import generate_token, admin_required
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET'])
def login_page():
    """Admin login page"""
    return render_template('admin/login.html')

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard_page():
    """Admin dashboard page"""
    return render_template('admin/dashboard.html')

@admin_bp.route('/api/login', methods=['POST'])
def admin_login():
    """Admin login API"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        db = get_db()
        admin_model = AdminModel(db)
        
        admin = admin_model.verify_admin(email, password)
        
        if admin:
            token = generate_token(admin['_id'], admin['email'])
            return jsonify({
                'success': True,
                'token': token,
                'admin': {
                    'id': str(admin['_id']),
                    'username': admin['username'],
                    'email': admin['email']
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@admin_bp.route('/api/verify', methods=['GET'])
@admin_required
def verify_token():
    """Verify admin token"""
    return jsonify({'success': True, 'admin_id': request.admin_id}), 200

@admin_bp.route('/api/logout', methods=['POST'])
def admin_logout():
    """Admin logout"""
    return jsonify({'success': True}), 200