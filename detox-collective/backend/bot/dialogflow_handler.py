import os
from flask import Blueprint, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from backend.app import db
from datetime import datetime

bot_bp = Blueprint('bot', __name__, url_prefix='/api/bot')

# Simple helper to call Dialogflow detect intent

def detect_intent_texts(project_id, session_id, text, language_code='en'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response

@bot_bp.route('/message', methods=['POST'])
def handle_bot_message():
    try:
        data = request.json or {}
        user_message = data.get('message')
        user_id = data.get('userId')
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

        if not project_id:
            return jsonify({'error': 'GOOGLE_CLOUD_PROJECT not set'}), 500

        response = detect_intent_texts(project_id, user_id, user_message)
        intent = response.query_result.intent.display_name
        fulfillment_text = response.query_result.fulfillment_text

        # Example: intercept a 'get_credits' intent
        if intent.lower() == 'get_credits' and user_id:
            user_doc = db.collection('users').document(user_id).get()
            if user_doc.exists:
                credits = user_doc.to_dict().get('totalCredits', 0)
                fulfillment_text = f'You have {credits} Detox Credits! 🎯'

        return jsonify({'success': True, 'message': fulfillment_text, 'intent': intent}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
