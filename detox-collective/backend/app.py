import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Firebase admin
import firebase_admin
from firebase_admin import credentials, firestore, messaging

SERVICE_ACCOUNT = os.getenv('SERVICE_ACCOUNT_PATH') or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if SERVICE_ACCOUNT:
    cred = credentials.Certificate(SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred)
else:
    # Try default credentials (e.g. GCP environment)
    try:
        firebase_admin.initialize_app()
    except Exception as e:
        print('Warning: firebase_admin not initialized with explicit credentials. Ensure credentials are available in production.')

# Firestore client
db = firestore.client()

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False

# Register blueprints
from routes.group_routes import group_bp
from routes.reward_routes import reward_bp
from routes.notification_routes import notif_bp

app.register_blueprint(group_bp)
app.register_blueprint(reward_bp)
app.register_blueprint(notif_bp)

if __name__ == '__main__':
    # Simple dev run
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=os.environ.get('FLASK_ENV') == 'development')
