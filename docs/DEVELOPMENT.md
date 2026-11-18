# Developer Guide

## 1. Prerequisites

- Git
- Python 3.11+ recommended for the backend environment
- MongoDB local instance or MongoDB Atlas database
- Node.js LTS and npm for the React frontend (frontend directory/package manifest must be confirmed in the repository before running frontend commands)

## 2. Clone and branch

```bash
git clone https://github.com/roshan-yadav-dev/Secure-Exam-Protal.git
cd Secure-Exam-Protal
git checkout feature/pdf-based-gate-exams
```

Use a feature branch for new work. Do not commit directly to `main`.

## 3. Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the API from the backend directory:

```bash
uvicorn app.main:app --reload
```

Expected local URLs:
- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: http://127.0.0.1:8000/health

The currently tracked requirements file should be checked as dependencies evolve. The settings module imports `pydantic_settings`; ensure `pydantic-settings` is declared in requirements before a clean installation. PDF/OCR libraries are not yet installed as part of the implemented application.

## 4. Environment configuration

Create `backend/.env` locally. Never commit it.

```dotenv
APP_NAME=Secure Exam Portal
APP_VERSION=0.2.0
MONGO_URI=mongodb://127.0.0.1:27017
DB_NAME=secure_exam_portal
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Generate a secret locally:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

The exact configuration names above match the existing settings module. Keep production values in the hosting provider's secret/environment settings.

## 5. Current backend layout

```text
backend/
  app/
    main.py
    config.py
    database.py
    middleware/
      auth.py
    models/
      user.py
    routes/
      auth.py
      dbtest.py
      health.py
      version.py
    schemas/
      exam.py
    services/
      scoring.py
    utils/
      hash.py
      token.py
  requirements.txt
```

The schemas and scoring service were added as initial product-foundation code. Additional document, exam, report, and frontend modules are planned.

## 6. Frontend setup

The repository frontend path and package manifest were not confirmed during this documentation pass. Once the frontend directory is present, install dependencies from its package manifest and configure its API base URL through a public frontend environment variable (for example, a Vite `VITE_API_BASE_URL`). Never place server secrets in frontend environment variables.

## 7. Development conventions

- Use Pydantic request/response schemas; avoid unvalidated `dict` request bodies.
- Keep route handlers thin; put business rules in services.
- Use type hints and explicit error handling.
- Keep database access owner-scoped.
- Use UTC timestamps and server-authoritative state transitions.
- Keep answer-key data out of Real Exam API responses.
- Keep source PDFs immutable.
- Add unit tests for parsing, verification, scoring and state transitions.
- Do not log passwords, JWTs, raw PDF contents, or private storage URLs.

## 8. Git workflow

```bash
git checkout -b feat/pdf-upload
# implement and test
git add .
git commit -m "feat: add secure question PDF upload"
git push -u origin feat/pdf-upload
```

Open a pull request into the agreed integration branch. Include summary, tests run, screenshots for UI changes, and migration/configuration notes.

## 9. Current implementation caveats

- Existing registration currently accepts a client-provided role; change this before production.
- Existing password helpers strip whitespace; avoid silently changing user passwords in the target implementation.
- Existing database test insertion endpoint is unauthenticated and uses hard-coded data; remove or disable it outside local development.
- Existing auth token payload is minimal; add token subject/issued-at identifiers and consider refresh/revocation strategy as needed.
- Add `pydantic-settings` to requirements if not already installed transitively; it is directly imported by config.
- The feature-branch schemas and scoring service have not yet been exercised by a runtime test suite.
