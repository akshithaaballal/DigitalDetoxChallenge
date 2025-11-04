# Detox Collective

A hackathon-ready MVP scaffold for the Collective Digital Detox Challenge.

This repository contains a minimal backend (Flask) and a minimal frontend (React skeleton) to get started quickly.

Structure
```
/detox-collective
  /backend    # Flask app + blueprints
  /frontend   # React app skeleton
```

Quick start (PowerShell)

1) Backend (create a Python venv and install dependencies)

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
# Set Google credentials (service account) path for firebase admin
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\serviceAccountKey.json"
# Or set SERVICE_ACCOUNT_PATH env var pointing to the file
$env:SERVICE_ACCOUNT_PATH="C:\path\to\serviceAccountKey.json"
cd backend
python app.py
```

2) Frontend (basic dev server)

```powershell
cd frontend
npm install
npm start
```

Notes
- Do NOT commit your Firebase service account JSON. Use environment variables or secret managers for production.
- Firestore security rules are required before deploying to production. See `firestore.rules`.

Next steps
- Wire Firebase project and add client config to `frontend/src/firebase.js`
- Replace placeholders in backend env example with real values
- Add Dialogflow credentials and enable webhook if using chatbot
