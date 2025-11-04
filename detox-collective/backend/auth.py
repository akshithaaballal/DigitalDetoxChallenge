from functools import wraps
from flask import request, jsonify, g
import firebase_admin
from firebase_admin import auth as firebase_auth


def verify_firebase_token(id_token):
    """Verify a Firebase ID token and return decoded token or raise."""
    try:
        decoded = firebase_auth.verify_id_token(id_token)
        return decoded
    except Exception:
        raise


def require_auth(fn):
    """Flask decorator to require a valid Firebase ID token in Authorization header.

    Expects header: Authorization: Bearer <id_token>
    Sets `g.user` to decoded token on success.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization header missing or invalid'}), 401
        id_token = auth_header.split(' ', 1)[1].strip()
        try:
            decoded = verify_firebase_token(id_token)
            g.user = decoded
        except Exception:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return fn(*args, **kwargs)

    return wrapper
