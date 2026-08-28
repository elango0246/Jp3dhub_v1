# models/admin.py
from datetime import datetime
import bcrypt

class AdminModel:
    def __init__(self, db):
        self.collection = db.admins
    
    def create_admin(self, username, email, password):
        """Create admin user"""
        # Hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        admin = {
            'username': username,
            'email': email.lower(),
            'password': hashed,
            'role': 'admin',
            'created_at': datetime.utcnow().timestamp(),
            'last_login': None
        }
        
        result = self.collection.insert_one(admin)
        return str(result.inserted_id)
    
    def verify_admin(self, email, password):
        """Verify admin credentials"""
        admin = self.collection.find_one({'email': email.lower()})
        
        if admin and bcrypt.checkpw(password.encode('utf-8'), admin['password']):
            # Update last login
            self.collection.update_one(
                {'_id': admin['_id']},
                {'$set': {'last_login': datetime.utcnow().timestamp()}}
            )
            return admin
        return None
    
    def get_admin_by_email(self, email):
        """Get admin by email"""
        return self.collection.find_one({'email': email.lower()})
    
    def get_all_admins(self):
        """Get all admins"""
        admins = list(self.collection.find({}, {'password': 0}))
        for admin in admins:
            admin['_id'] = str(admin['_id'])
        return admins

# Create default admin if none exists
def create_default_admin(db):
    admin_model = AdminModel(db)
    existing = admin_model.get_admin_by_email('admin@blaster3d.in')
    if not existing:
        admin_model.create_admin('admin', 'admin@blaster3d.in', 'Admin@123')
        print("✅ Default admin created: admin@blaster3d.in / Admin@123")