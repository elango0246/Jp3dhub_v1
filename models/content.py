# models/content.py
from datetime import datetime
from bson.objectid import ObjectId

class ContentModel:
    def __init__(self, db):
        self.collection = db.contents
    
    def create_content(self, data):
        """Create new content (image/video/text)"""
        content = {
            'type': data.get('type'),  # 'image', 'video', 'text', 'gallery'
            'title': data.get('title'),
            'description': data.get('description'),
            'file_url': data.get('file_url'),
            'file_name': data.get('file_name'),
            'file_size': data.get('file_size'),
            'category': data.get('category'),  # 'hero', 'gallery', 'service', 'testimonial'
            'order': data.get('order', 0),
            'is_active': data.get('is_active', True),
            'metadata': data.get('metadata', {}),
            'created_by': data.get('created_by'),
            'created_at': datetime.utcnow().timestamp(),
            'updated_at': datetime.utcnow().timestamp()
        }
        
        result = self.collection.insert_one(content)
        content['_id'] = str(result.inserted_id)
        return content
    
    def get_all_contents(self, category=None, limit=100, skip=0):
        """Get all contents with filters"""
        query = {}
        if category:
            query['category'] = category
        
        contents = list(self.collection.find(query)
                       .sort('order', 1)
                       .sort('created_at', -1)
                       .skip(skip)
                       .limit(limit))
        
        for content in contents:
            content['_id'] = str(content['_id'])
        
        return contents
    
    def get_content_by_id(self, content_id):
        """Get single content by ID"""
        try:
            content = self.collection.find_one({'_id': ObjectId(content_id)})
            if content:
                content['_id'] = str(content['_id'])
            return content
        except:
            return None
    
    def update_content(self, content_id, data):
        """Update content"""
        try:
            data['updated_at'] = datetime.utcnow().timestamp()
            result = self.collection.update_one(
                {'_id': ObjectId(content_id)},
                {'$set': data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete_content(self, content_id):
        """Delete content"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(content_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def get_gallery_images(self):
        """Get gallery images"""
        return self.get_all_contents(category='gallery')
    
    def get_hero_content(self):
        """Get hero section content"""
        return self.get_all_contents(category='hero', limit=1)
    
    def get_testimonials(self):
        """Get testimonials"""
        return self.get_all_contents(category='testimonial')
    
    def get_services(self):
        """Get services content"""
        return self.get_all_contents(category='service')