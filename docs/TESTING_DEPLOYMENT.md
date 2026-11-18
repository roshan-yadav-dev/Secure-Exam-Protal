# Testing, Deployment and Operations

## 1. Testing strategy

The current repository foundation has not yet been validated with a complete automated test suite. Add tests alongside each feature rather than postponing testing until release.

### Unit tests
- Password hashing and verification.
- JWT creation, expiry and invalid-token handling.
- Question-number and option parsing.
- Answer-key extraction and manual correction.
- Verification-state rules.
- Scoring with correct, incorrect and unanswered responses.
- Negative-marking calculations.
- Accuracy when attempted count is zero.
- Report annotation coordinate mapping and fallback notes.

### Integration tests
- Register/login/current-user flow.
- User A cannot access User B's document, exam, attempt or report.
- Upload validation rejects non-PDF, oversized and malformed files.
- Question-set processing stores extracted page references.
- Unverified question sets cannot create exams.
- Real Exam response payload never includes correct answers.
- Responses cannot be changed after submit or deadline.
- Duplicate submission returns the same result.
- Report download requires ownership.

### Frontend tests
- Upload validation and progress state.
- Verification editor corrections.
- Exam navigation and answer persistence.
- Timer display and submit confirmation.
- Practice feedback versus Real Exam secrecy.
- Result summary and report download states.
- Keyboard accessibility and responsive layouts.

### End-to-end scenarios
1. Upload a text-based question paper and matching answer key.
2. Verify extracted questions and answers.
3. Create a Practice Mode exam and complete it.
4. Create a Real Exam and confirm no answer is revealed before submission.
5. Let an attempt expire and confirm server-side auto-submission.
6. Download the annotated source PDF and inspect each color/status.
7. Attempt cross-user resource access and confirm denial.

## 2. Scoring test examples

Given:
- Correct marks = 1
- Incorrect marks = -0.33
- Answer key = {1: A, 2: C, 3: B}
- Responses = {1: A, 2: D}

Expected:
- Correct = 1
- Incorrect = 1
- Unanswered = 1
- Attempted = 2
- Score = 0.67
- Accuracy = 50%

Use decimal precision consistently. Decide whether to store raw decimal scores and round only for display.

## 3. Local quality checks

From the backend directory, after installing test dependencies:

```bash
python -m compileall app
pytest -q
```

Add lint/type checks as the codebase grows. Do not claim a build or test passed unless it was run against the relevant branch and environment.

## 4. Deployment topology

Target:
- React frontend: Vercel.
- FastAPI backend: Render.
- MongoDB: MongoDB Atlas.
- PDF storage: private persistent storage or private object storage.

The frontend communicates with the backend through a configured API base URL. Configure CORS to allow only the deployed frontend origin(s).

## 5. Backend deployment checklist

- Set the production start command, for example:
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Set all environment variables in the hosting dashboard.
- Configure MongoDB network access and least-privilege database credentials.
- Use a strong unique JWT secret.
- Configure CORS, upload limits and request timeouts.
- Ensure PDF storage is persistent and private; do not rely on ephemeral local disk for durable uploads.
- Add health checks and structured logs.
- Do not expose development DB test routes.
- Confirm migrations/index creation and backup strategy.

## 6. Frontend deployment checklist

- Set the public API base URL.
- Never embed backend secrets in frontend variables.
- Configure the production backend CORS origin.
- Test authentication, upload, exam attempt and report download against production APIs.
- Verify mobile and keyboard usability.

## 7. Monitoring and operations

Track:
- API request latency and error rate.
- Upload rejection and processing failure rates.
- OCR duration and worker backlog.
- Exam submission failures.
- Report generation failures.
- Database connectivity and storage capacity.

Logs should include request/job identifiers and safe resource IDs, but not passwords, bearer tokens, answer-key contents, or raw uploaded document text.

## 8. Backup and recovery

- Enable managed MongoDB backups.
- Back up private PDF storage independently from database metadata.
- Test restore procedures.
- Keep generated reports reproducible where source files and attempt snapshots remain available.
- Define retention and deletion policies before multi-user production use.

## 9. Release checklist

- [ ] Product acceptance criteria met.
- [ ] Unit, integration and end-to-end tests pass.
- [ ] Security checklist in SECURITY.md complete.
- [ ] No exposed secrets or debug endpoints.
- [ ] Database indexes and backups configured.
- [ ] Persistent private PDF storage configured.
- [ ] CORS and TLS verified.
- [ ] Real Exam answer secrecy tested.
- [ ] Server-side timer and idempotent submit tested.
- [ ] Annotated PDF visually checked against original.
- [ ] Rollback plan documented.
