# Installation Requirements

## Prerequisites
- Python 3.11 or later
  - Download: https://www.python.org/downloads/windows/
  - ✅ CHECK "Add python.exe to PATH" during installation

- Node.js LTS
  - Download: https://nodejs.org/
  - Choose LTS (Long Term Support) version

## Verify Installation
Open a new PowerShell window and run:
```powershell
python --version  # Should show Python 3.11 or later
node --version   # Should show v18 or later
```

## Project Setup (After installing prerequisites)
1. Backend (Flask)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Frontend (React)
```powershell
npm install
npm start
```

## Common Issues
- If Python/Node commands not found: Close and reopen PowerShell

- For Python Windows Store error: Disable app execution aliases in Windows Settings
