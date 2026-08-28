from pymongo import MongoClient
from flask import current_app, g

def get_db():
    """Get database connection with connection pooling"""
    if 'db' not in g:
        client = MongoClient(current_app.config['MONGO_URI'])
        g.db = client.get_database()
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.client.close()

def init_app(app):
    """Register database teardown with app"""
    app.teardown_appcontext(close_db)