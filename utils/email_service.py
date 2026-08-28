# utils/email_service.py (Simplest - No Thread Pool Issues)
from flask_mail import Mail, Message
from flask import current_app
import threading

mail = Mail()

def send_async_email(app, msg):
    """Send email in background thread"""
    with app.app_context():
        try:
            mail.send(msg)
            print("✅ Email sent successfully")
        except Exception as e:
            print(f"❌ Email error: {e}")

def send_admin_notification(contact_data):
    """Send email notification to admin"""
    try:
        app = current_app._get_current_object()
        
        msg = Message(
            subject=f"🔧 New 3D Printing Quote Request from {contact_data['name']}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['ADMIN_EMAIL']],
            html=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #f5f5f5;">
                <div style="background: #ff4d00; padding: 20px; text-align: center; color: white;">
                    <h1 style="margin: 0;">BLASTER3D</h1>
                    <p style="margin: 5px 0 0;">New Quote Request</p>
                </div>
                <div style="background: white; padding: 25px; border-radius: 8px; margin-top: 20px;">
                    <h2 style="color: #333; margin-top: 0;">Customer Details</h2>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px 0;"><strong>Name:</strong></td>
                        <td>{contact_data['name']}</td>
                        </tr>
                        <tr><td style="padding: 8px 0;"><strong>Email:</strong></td>
                        <td>{contact_data['email']}</td>
                        </tr>
                        <tr><td style="padding: 8px 0;"><strong>Phone:</strong></td>
                        <td>{contact_data['phone']}</td>
                        </tr>
                        <tr><td style="padding: 8px 0;"><strong>Service:</strong></td>
                        <td>{contact_data['service']}</td>
                        </tr>
                    </table>
                    <h3 style="color: #333; margin-top: 20px;">Project Details</h3>
                    <div style="background: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 4px solid #ff4d00;">
                        {contact_data['message']}
                    </div>
                </div>
            </div>
            """
        )
        
        # Start background thread
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.daemon = True
        thread.start()
        return True
    except Exception as e:
        print(f"Admin email error: {e}")
        return False

def send_customer_confirmation(contact_data):
    """Send confirmation email to customer"""
    try:
        app = current_app._get_current_object()
        
        msg = Message(
            subject="Thank you for contacting Blaster3D - Quote Request Received",
            sender=app.config['MAIL_USERNAME'],
            recipients=[contact_data['email']],
            html=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: #ff4d00; padding: 20px; text-align: center;">
                    <h1 style="margin: 0; color: white;">BLASTER3D</h1>
                </div>
                <div style="background: white; padding: 25px; border-radius: 8px;">
                    <h2>Hello {contact_data['name']},</h2>
                    <p>Thank you for reaching out to Blaster3D! We've received your quote request for <strong>{contact_data['service']}</strong>.</p>
                    <p>Our team will review your project details and get back to you within <strong>2-4 business hours</strong>.</p>
                    
                    <div style="background: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px;">
                        <h3 style="margin-top: 0;">Your Request Summary:</h3>
                        <p><strong>Service:</strong> {contact_data['service']}</p>
                        <p><strong>Project Details:</strong></p>
                        <p>{contact_data['message']}</p>
                    </div>
                    
                    <p>In the meantime, you can:</p>
                    <ul>
                        <li>📞 Call us at +91 98765 43210 for urgent inquiries</li>
                        <li>💬 Chat with us on WhatsApp at the same number</li>
                        <li>📧 Reply to this email with additional files or specifications</li>
                    </ul>
                    
                    <hr style="margin: 25px 0; border-color: #eee;">
                    <p style="font-size: 12px; color: #666;">
                        Best regards,<br>
                        <strong>The Blaster3D Team</strong><br>
                        Premium 3D Printing Services | Chennai, India
                    </p>
                </div>
            </div>
            """
        )
        
        # Start background thread
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.daemon = True
        thread.start()
        return True
    except Exception as e:
        print(f"Customer email error: {e}")
        return False