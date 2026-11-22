# Human API – Learning Prototype

A small educational MVP for the Human API project. It demonstrates task submission, transparent keyword-based candidate ranking, and evidence explanations using fictional employee data only.

## Team / project context
- Project: Human API – Intelligent Organizational Expertise Discovery System
- Students: Abdelrahman Dabash and Fares Farghaly
- Course context: SWE 401
- This folder is a learning prototype, not a production HR tool or submission-ready project.

## Key features
- Submit a task title and natural-language description.
- Compare task terms with fictional employee skills, project summaries and completed tasks.
- Return candidates ordered by a deterministic lexical score.
- Show matched terms, evidence sources and an evidence-strength label.
- Keep final hiring or assignment decisions with a human manager.

## Technologies
- Frontend: React, Vite, JavaScript
- Backend: Python, FastAPI, Pydantic
- Tests: pytest, FastAPI TestClient

## Prerequisites
- Python 3.10+
- Node.js 18+
- npm

## Installation and run

### 1. Start the backend
```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
The API runs at http://127.0.0.1:8000. Interactive API docs: http://127.0.0.1:8000/docs.

### 2. Start the frontend in a second terminal
```bash
cd frontend
npm install
npm run dev
```
Open the local URL printed by Vite (usually http://localhost:5173).

## Configuration
The learning MVP uses fictional in-memory sample records and does not connect to PostgreSQL. This keeps the demonstration easy to run. The Phase 4 design document specifies PostgreSQL as the intended persistent database for the next implementation increment. Do not use real employee information in this demo.

## How to test
From the `backend` directory, with the virtual environment active:
```bash
pytest -q
```
Tests cover health status, employee listing, matching output, required-field validation and unknown employee handling. Capture your own terminal output and screenshots after running the tests; do not claim tests passed before execution.

## Matching method and limitations
The prototype tokenizes the task title and description and calculates a simple overlap percentage against employee skills, project summaries and completed tasks. The score is a keyword indicator only. It is not a trained AI model, does not establish actual competence, and must not be used to make employment decisions. The prototype has no authentication, role-based authorization, audit logging, persistent database, or production security controls.

## Privacy and security
All records are fictional. Never commit passwords, API keys, tokens, real employee records or private company information. Any future deployment requires authentication, authorization, secure storage, retention rules, fairness evaluation and human oversight.\n