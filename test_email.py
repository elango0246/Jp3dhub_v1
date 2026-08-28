# test_email.py - Test email configuration
import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message

load_dotenv()

def test_email():
    """Test email configuration"""
    print("=" * 50)
    print("📧 Testing Email Configuration")
    print("=" * 50)
    
    # Create a minimal Flask app
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
    
    mail = Mail(app)
    
    print(f"📧 MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
    print(f"📧 MAIL_PASSWORD: {'*' * len(app.config['MAIL_PASSWORD']) if app.config['MAIL_PASSWORD'] else 'NOT SET'}")
    print(f"📧 ADMIN_EMAIL: {os.environ.get('ADMIN_EMAIL')}")
    
    with app.app_context():
        try:
            msg = Message(
                subject="Test Email from Blaster3D",
                recipients=[os.environ.get('ADMIN_EMAIL')],
                body="This is a test email to verify SMTP configuration."
            )
            mail.send(msg)
            print("\n✅ Test email sent successfully!")
            return True
        except Exception as e:
            print(f"\n❌ Failed to send test email: {e}")
            return False

if __name__ == "__main__":
    test_email()