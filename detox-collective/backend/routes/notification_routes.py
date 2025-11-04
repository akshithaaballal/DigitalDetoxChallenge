from flask import Blueprint, request, jsonify, g
from datetime import datetime

from firebase_admin import messaging
from firebase_admin import firestore
from backend.app import db
from backend.auth import require_auth

notif_bp = Blueprint('notifications', __name__, url_prefix='/api')

def _create_system_message(group_id, message, notification_type='general'):
    db.collection('groupChats').document(group_id).collection('messages').add({
        'text': message,
        'timestamp': datetime.utcnow(),
        'type': 'system_notification',
        'notificationType': notification_type
    })

@notif_bp.route('/notify-group', methods=['POST'])
@require_auth
def notify_group_endpoint():
    try:
        data = request.json or {}
        group_id = data.get('groupId')
        message = data.get('message')
        notification_type = data.get('type', 'general')

        if not group_id or not message:
            return jsonify({'error': 'groupId and message are required'}), 400

        # Create a system chat message
        _create_system_message(group_id, message, notification_type)

        # Send FCM messages to member tokens if available
        group_doc = db.collection('groups').document(group_id).get()
        if group_doc.exists:
            members = group_doc.to_dict().get('members', [])
            for member_email in members:
                # Find user document by email
                users_query = db.collection('users').where('email', '==', member_email).stream()
                for user_doc in users_query:
                    user = user_doc.to_dict()
                    fcm_token = user.get('fcmToken')
                    if fcm_token:
                        msg = messaging.Message(
                            notification=messaging.Notification(
                                title='Detox Collective',
                                body=message
                            ),
                            token=fcm_token,
                            data={'type': notification_type}
                        )
                        try:
                            messaging.send(msg)
                        except Exception as e:
                            print('FCM send error:', e)

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
