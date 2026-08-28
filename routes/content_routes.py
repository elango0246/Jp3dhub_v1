# routes/content_routes.py
from flask import Blueprint, request, jsonify, current_app
from models.content import ContentModel
from models import get_db
from utils.auth import admin_required
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

content_bp = Blueprint('content', __name__, url_prefix='/api/content')

# Allowed file extensions
ALLOWED_IMAGES = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_VIDEOS = {'mp4', 'webm', 'mov'}

def save_file(file, file_type='image'):
    """Save uploaded file"""
    if not file:
        return None
    
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Determine upload folder
    if file_type == 'video':
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'videos')
    else:
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'images')
    
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    
    # Return relative URL
    return f"/uploads/{file_type}s/{unique_filename}"

# GET all content
@content_bp.route('/', methods=['GET'])
def get_all_content():
    """Get all content (public)"""
    try:
        category = request.args.get('category')
        db = get_db()
        content_model = ContentModel(db)
        
        contents = content_model.get_all_contents(category=category)
        return jsonify({'success': True, 'contents': contents}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET single content
@content_bp.route('/<content_id>', methods=['GET'])
def get_content(content_id):
    """Get single content"""
    try:
        db = get_db()
        content_model = ContentModel(db)
        
        content = content_model.get_content_by_id(content_id)
        if not content:
            return jsonify({'error': 'Content not found'}), 404
        
        return jsonify({'success': True, 'content': content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CREATE content (admin only)
@content_bp.route('/', methods=['POST'])
@admin_required
def create_content():
    """Create new content with file upload"""
    try:
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        content_type = request.form.get('type')
        order = int(request.form.get('order', 0))
        
        # Handle file upload
        file_url = None
        file_name = None
        file_size = None
        
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                file_name = file.filename
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(0)
                
                # Save file
                file_url = save_file(file, content_type)
        
        # Create content object
        content_data = {
            'type': content_type,
            'title': title,
            'description': description,
            'file_url': file_url,
            'file_name': file_name,
            'file_size': file_size,
            'category': category,
            'order': order,
            'is_active': True,
            'created_by': request.admin_email,
            'metadata': {
                'ip': request.remote_addr,
                'user_agent': request.headers.get('User-Agent')
            }
        }
        
        db = get_db()
        content_model = ContentModel(db)
        
        content = content_model.create_content(content_data)
        
        return jsonify({
            'success': True,
            'message': 'Content created successfully',
            'content': content
        }), 201
        
    except Exception as e:
        print(f"Create content error: {e}")
        return jsonify({'error': str(e)}), 500

# UPDATE content (admin only)
@content_bp.route('/<content_id>', methods=['PUT'])
@admin_required
def update_content(content_id):
    """Update existing content"""
    try:
        data = request.get_json() if request.is_json else request.form
        
        update_data = {}
        allowed_fields = ['title', 'description', 'category', 'type', 'order', 'is_active']
        
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        db = get_db()
        content_model = ContentModel(db)
        
        result = content_model.update_content(content_id, update_data)
        
        if result:
            return jsonify({'success': True, 'message': 'Content updated successfully'}), 200
        else:
            return jsonify({'error': 'Content not found'}), 404
            
    except Exception as e:
        print(f"Update content error: {e}")
        return jsonify({'error': str(e)}), 500

# DELETE content (admin only)
@content_bp.route('/<content_id>', methods=['DELETE'])
@admin_required
def delete_content(content_id):
    """Delete content"""
    try:
        db = get_db()
        content_model = ContentModel(db)
        
        # Get content to delete file
        content = content_model.get_content_by_id(content_id)
        
        result = content_model.delete_content(content_id)
        
        if result:
            # Delete physical file if exists
            if content and content.get('file_url'):
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], content['file_url'].replace('/uploads/', ''))
                if os.path.exists(filepath):
                    os.remove(filepath)
            
            return jsonify({'success': True, 'message': 'Content deleted successfully'}), 200
        else:
            return jsonify({'error': 'Content not found'}), 404
            
    except Exception as e:
        print(f"Delete content error: {e}")
        return jsonify({'error': str(e)}), 500

# GET gallery for frontend
@content_bp.route('/gallery', methods=['GET'])
def get_gallery():
    """Get gallery images for frontend"""
    try:
        db = get_db()
        content_model = ContentModel(db)
        
        gallery = content_model.get_gallery_images()
        return jsonify({'success': True, 'gallery': gallery}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET testimonials for frontend
@content_bp.route('/testimonials', methods=['GET'])
def get_testimonials():
    """Get testimonials for frontend"""
    try:
        db = get_db()
        content_model = ContentModel(db)
        
        testimonials = content_model.get_testimonials()
        return jsonify({'success': True, 'testimonials': testimonials}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500