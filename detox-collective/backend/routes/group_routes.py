from flask import Blueprint, request, jsonify, g
from datetime import datetime
import uuid

from firebase_admin import firestore
from backend.app import db  # import Firestore client
from backend.auth import require_auth

group_bp = Blueprint('groups', __name__, url_prefix='/api')

@group_bp.route('/groups', methods=['POST'])
@require_auth
def create_group():
    try:
        data = request.json or {}
        group_id = str(uuid.uuid4())

        # use authenticated user's uid as part of group creator metadata
        creator_uid = getattr(g, 'user', {}).get('uid', None)

        group_data = {
            'groupName': data.get('groupName', 'Untitled Group'),
            'members': data.get('members', []),
            'detoxDuration': int(data.get('detoxDuration', 60)),
            'status': 'created',
            'createdAt': datetime.utcnow(),
            'totalCredits': 0,
            'createdBy': creator_uid,
            'campus': data.get('campus', 'General')
        }

        db.collection('groups').document(group_id).set(group_data)

        # Create group chat document
        chat_data = {
            'groupId': group_id,
            'createdAt': datetime.utcnow()
        }
        db.collection('groupChats').document(group_id).set(chat_data)

        return jsonify({'success': True, 'groupId': group_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@group_bp.route('/groups/<group_id>', methods=['GET'])
def get_group(group_id):
    try:
        doc = db.collection('groups').document(group_id).get()
        if doc.exists:
            data = doc.to_dict()
            # Convert Firestore timestamps if necessary
            return jsonify(data), 200
        return jsonify({'error': 'Group not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@group_bp.route('/groups/<group_id>/members', methods=['POST'])
@require_auth
def add_member(group_id):
    try:
        data = request.json or {}
        email = data.get('email')
        if not email:
            return jsonify({'error': 'email required'}), 400

        group_ref = db.collection('groups').document(group_id)
        group_ref.update({
            'members': firestore.ArrayUnion([email])
        })
        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@group_bp.route('/groups/<group_id>/start', methods=['POST'])
@require_auth
def start_detox_session(group_id):
    try:
        data = request.json or {}
        # prefer authenticated uid; fallback to provided userId
        user_id = getattr(g, 'user', {}).get('uid') or data.get('userId')
        if not user_id:
            return jsonify({'error': 'userId required'}), 400

        session_id = str(uuid.uuid4())
        session_data = {
            'groupId': group_id,
            'userId': user_id,
            'checkInTime': datetime.utcnow(),
            'status': 'active',
            'breakTime': None,
            'creditsEarned': 0
        }

        db.collection('detoxSessions').document(session_id).set(session_data)

        # Notify group (lightweight: create a system message)
        db.collection('groupChats').document(group_id).collection('messages').add({
            'text': f'User {user_id} started a detox session',
            'timestamp': datetime.utcnow(),
            'type': 'system_notification'
        })

        return jsonify({'success': True, 'sessionId': session_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
