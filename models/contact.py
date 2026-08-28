from datetime import datetime
import re
from email_validator import validate_email, EmailNotValidError

class ContactModel:
    def __init__(self, db):
        self.collection = db.contacts
    
    def validate_phone(self, phone):
        """Validate Indian phone number"""
        pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,10}$'
        return re.match(pattern, phone) is not None
    
    def validate_email(self, email):
        """Validate email address"""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    def create_contact(self, data):
        """Create new contact entry"""
        # Validate required fields
        required = ['name', 'email', 'phone', 'service', 'message']
        for field in required:
            if not data.get(field):
                return {'error': f'{field} is required'}, 400
        
        # Validate email
        if not self.validate_email(data['email']):
            return {'error': 'Invalid email address'}, 400
        
        # Validate phone
        if not self.validate_phone(data['phone']):
            return {'error': 'Invalid phone number'}, 400
        
        # Validate service
        valid_services = ['FDM Printing', 'Resin / SLA', 'Rapid Prototyping', 'Production Run', '3D Design']
        if data['service'] not in valid_services:
            return {'error': 'Invalid service selected'}, 400
        
        # Validate message length
        if len(data['message']) < 10:
            return {'error': 'Message must be at least 10 characters'}, 400
        
        # Check for duplicate submission (same email within 5 minutes)
        recent = self.collection.find_one({
            'email': data['email'].lower(),
            'created_at': {'$gte': datetime.utcnow().timestamp() - 300}
        })
        
        if recent:
            return {'error': 'Please wait before submitting another request'}, 429
        
        contact = {
            'name': data['name'].strip(),
            'email': data['email'].lower().strip(),
            'phone': data['phone'].strip(),
            'service': data['service'],
            'message': data['message'].strip(),
            'status': 'pending',
            'ip_address': data.get('ip_address'),
            'user_agent': data.get('user_agent'),
            'created_at': datetime.utcnow().timestamp(),
            'updated_at': datetime.utcnow().timestamp()
        }
        
        result = self.collection.insert_one(contact)
        contact['_id'] = str(result.inserted_id)
        
        return {'success': True, 'message': 'Contact created successfully', 'id': str(result.inserted_id)}, 201
    
    def get_all_contacts(self, limit=100, skip=0):
        """Get all contacts with pagination"""
        contacts = list(self.collection.find()
                       .sort('created_at', -1)
                       .skip(skip)
                       .limit(limit))
        
        for contact in contacts:
            contact['_id'] = str(contact['_id'])
        
        return contacts
    
    def get_contact_by_id(self, contact_id):
        """Get single contact by ID"""
        from bson.objectid import ObjectId
        try:
            contact = self.collection.find_one({'_id': ObjectId(contact_id)})
            if contact:
                contact['_id'] = str(contact['_id'])
            return contact
        except:
            return None
    
    def update_status(self, contact_id, status):
        """Update contact status"""
        from bson.objectid import ObjectId
        valid_statuses = ['pending', 'contacted', 'quoted', 'completed', 'archived']
        
        if status not in valid_statuses:
            return {'error': 'Invalid status'}, 400
        
        result = self.collection.update_one(
            {'_id': ObjectId(contact_id)},
            {'$set': {'status': status, 'updated_at': datetime.utcnow().timestamp()}}
        )
        
        if result.modified_count == 0:
            return {'error': 'Contact not found'}, 404
        
        return {'success': True, 'message': 'Status updated'}, 200
    
    def get_stats(self):
        """Get contact statistics"""
        total = self.collection.count_documents({})
        pending = self.collection.count_documents({'status': 'pending'})
        contacted = self.collection.count_documents({'status': 'contacted'})
        quoted = self.collection.count_documents({'status': 'quoted'})
        completed = self.collection.count_documents({'status': 'completed'})
        
        week_ago = datetime.utcnow().timestamp() - (7 * 24 * 60 * 60)
        last_week = self.collection.count_documents({'created_at': {'$gte': week_ago}})
        
        return {
            'total': total,
            'pending': pending,
            'contacted': contacted,
            'quoted': quoted,
            'completed': completed,
            'last_week': last_week
        }