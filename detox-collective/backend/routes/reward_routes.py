from flask import Blueprint, request, jsonify, g
from datetime import datetime
import uuid
import random
import string

from firebase_admin import firestore
from backend.app import db
from backend.auth import require_auth

reward_bp = Blueprint('rewards', __name__, url_prefix='/api')

@reward_bp.route('/check-group-completion', methods=['POST'])
@require_auth
def check_group_completion():
    try:
        data = request.json or {}
        group_id = data.get('groupId')
        if not group_id:
            return jsonify({'error': 'groupId required'}), 400

        group_ref = db.collection('groups').document(group_id)
        group_doc = group_ref.get()
        if not group_doc.exists:
            return jsonify({'error': 'Group not found'}), 404
        group_data = group_doc.to_dict()

        sessions_query = db.collection('detoxSessions').where('groupId', '==', group_id)
        sessions = [s.to_dict() for s in sessions_query.stream()]

        if not sessions:
            return jsonify({'error': 'No sessions found'}), 404

        # NOTE: For reliability, sessions should include a batchId. Here we consider latest checkInTime.
        latest_sessions = sorted(sessions, key=lambda x: x.get('checkInTime', datetime.min), reverse=True)
        latest_time = latest_sessions[0].get('checkInTime')

        # Keep sessions where checkInTime matches latest_time (this is approximate)
        batch_sessions = [s for s in latest_sessions if s.get('checkInTime') == latest_time]

        members = group_data.get('members', [])
        completed_count = sum(1 for s in batch_sessions if s.get('status') == 'completed')
        failed_count = sum(1 for s in batch_sessions if s.get('status') == 'failed')

        if failed_count > 0:
            # Group failed
            db.collection('groupChats').document(group_id).collection('messages').add({
                'text': 'Group contract broken! Better luck next time!',
                'timestamp': datetime.utcnow(),
                'type': 'system_notification'
            })
            return jsonify({'status': 'failed', 'reason': 'Someone broke the contract'}), 200

        elif completed_count == len(members):
            # Award credits
            for member in members:
                user_ref = db.collection('users').document(member)
                user_doc = user_ref.get()
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    current = user_data.get('totalCredits', 0)
                    user_ref.update({'totalCredits': current + 100})
                else:
                    # create user doc with credits
                    user_ref.set({'totalCredits': 100, 'createdAt': datetime.utcnow()})

            # Create badge
            badge_id = str(uuid.uuid4())
            badge_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            badge_data = {
                'badgeName': 'Detox Champion',
                'description': 'Completed group detox challenge',
                'rewardCode': badge_code,
                'createdAt': datetime.utcnow(),
                'groupId': group_id,
                'earnedBy': members,
                'partner': 'Campus Vendor'
            }
            db.collection('badges').document(badge_id).set(badge_data)

            group_ref.update({
                'status': 'completed',
                'totalCredits': firestore.Increment(100 * len(members)),
                'badgeId': badge_id
            })

            db.collection('groupChats').document(group_id).collection('messages').add({
                'text': f'🎉 Group success! Everyone earned 100 credits! Badge code: {badge_code}',
                'timestamp': datetime.utcnow(),
                'type': 'system_notification'
            })

            return jsonify({'status': 'success', 'creditsAwarded': 100}), 200

        else:
            return jsonify({'status': 'pending', 'completed': completed_count, 'total': len(members)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reward_bp.route('/badges/redeem', methods=['POST'])
@require_auth
def redeem_badge():
    try:
        data = request.json or {}
        badge_code = data.get('badgeCode')
        user_id = data.get('userId')
        if not badge_code or not user_id:
            return jsonify({'error': 'badgeCode and userId required'}), 400

        badges_query = db.collection('badges').where('rewardCode', '==', badge_code)
        badges = list(badges_query.stream())

        if not badges:
            return jsonify({'error': 'Invalid badge code'}), 404

        badge_doc = badges[0]
        badge_data = badge_doc.to_dict()

        badge_doc.reference.update({
            'usedBy': firestore.ArrayUnion([user_id]),
            'redeemedAt': datetime.utcnow()
        })

        return jsonify({'success': True, 'message': f"Congratulations! Redeem at: {badge_data.get('partner')}", 'reward': badge_data.get('description')}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
