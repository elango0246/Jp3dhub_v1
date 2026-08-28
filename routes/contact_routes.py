# routes/contact_routes.py
from flask import Blueprint, request, jsonify, current_app
from models.contact import ContactModel
from utils.email_service import send_admin_notification, send_customer_confirmation
from models import get_db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from concurrent.futures import ThreadPoolExecutor
import time
import traceback

contact_bp = Blueprint('contact', __name__, url_prefix='/api/contact')
limiter = Limiter(get_remote_address)

# Thread pool for background tasks
_task_executor = ThreadPoolExecutor(max_workers=10)


def background_email_tasks(app, data):
    """Run email tasks in background with Flask app context"""
    with app.app_context():
        try:
            print(f"📧 Starting background email tasks for {data['email']}")

            # Send admin notification
            admin_result = send_admin_notification(data)
            print(f"✅ Admin email sent: {admin_result}")

            # Send customer confirmation
            customer_result = send_customer_confirmation(data)
            print(f"✅ Customer email sent: {customer_result}")

        except Exception as e:
            print(f"❌ Background email error: {e}")
            print(traceback.format_exc())


@contact_bp.route('/', methods=['POST'])
@limiter.limit("5 per 15 minutes")
def submit_contact():
    """Submit contact form - Returns immediately (<100ms)"""
    start_time = time.time()

    try:
        data = request.get_json()
        print(f"📝 Received contact request from {data.get('email')}")

        # Add request metadata
        data['ip_address'] = request.remote_addr
        data['user_agent'] = request.headers.get('User-Agent')

        # Save to database
        db = get_db()
        contact_model = ContactModel(db)

        result, status_code = contact_model.create_contact(data)

        if status_code == 201 and result.get('success'):

            # Get real Flask app object
            app = current_app._get_current_object()

            # Fire and forget - emails send in background
            _task_executor.submit(background_email_tasks, app, data)

            elapsed = time.time() - start_time
            print(f"✅ Contact submission processed in {elapsed:.3f} seconds")

            return jsonify({
                'success': True,
                'message': 'Thank you! We\'ll get back to you within 2-4 hours.',
                'elapsed_ms': int(elapsed * 1000)
            }), 201

        return jsonify(result), status_code

    except Exception as e:
        print(f"❌ Error in submit_contact: {e}")
        print(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500


@contact_bp.route('/', methods=['GET'])
def get_all_contacts():
    """Get all contacts (admin only)"""
    try:
        db = get_db()
        contact_model = ContactModel(db)

        limit = request.args.get('limit', 100, type=int)
        skip = request.args.get('skip', 0, type=int)

        contacts = contact_model.get_all_contacts(limit, skip)

        return jsonify({
            'success': True,
            'count': len(contacts),
            'contacts': contacts
        }), 200

    except Exception as e:
        print(f"Error fetching contacts: {e}")
        return jsonify({'error': str(e)}), 500


@contact_bp.route('/<contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Get single contact by ID"""
    try:
        db = get_db()
        contact_model = ContactModel(db)

        contact = contact_model.get_contact_by_id(contact_id)

        if not contact:
            return jsonify({'error': 'Contact not found'}), 404

        return jsonify({
            'success': True,
            'contact': contact
        }), 200

    except Exception as e:
        print(f"Error fetching contact: {e}")
        return jsonify({'error': str(e)}), 500


@contact_bp.route('/<contact_id>/status', methods=['PUT'])
def update_contact_status(contact_id):
    """Update contact status"""
    try:
        data = request.get_json()
        status = data.get('status')

        db = get_db()
        contact_model = ContactModel(db)

        result, status_code = contact_model.update_status(contact_id, status)

        return jsonify(result), status_code

    except Exception as e:
        print(f"Error updating status: {e}")
        return jsonify({'error': str(e)}), 500


@contact_bp.route('/stats/dashboard', methods=['GET'])
def get_stats():
    """Get contact statistics"""
    try:
        db = get_db()
        contact_model = ContactModel(db)

        stats = contact_model.get_stats()

        return jsonify({
            'success': True,
            'stats': stats
        }), 200

    except Exception as e:
        print(f"Error fetching stats: {e}")
        return jsonify({'error': str(e)}), 500