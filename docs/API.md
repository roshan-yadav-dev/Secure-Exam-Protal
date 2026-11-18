# API Reference

## 1. Status and conventions

Base path: `/api` unless otherwise noted.

- Authentication: `Authorization: Bearer <access-token>`.
- JSON request/response bodies unless an endpoint accepts multipart upload.
- IDs are MongoDB ObjectId strings at the API boundary.
- Dates are UTC ISO-8601 strings.
- Error responses use FastAPI's standard `detail` field.
- This document distinguishes **Implemented** endpoints from **Planned** contracts. Planned routes are not available until their implementation is merged and deployed.

## 2. Existing endpoints

| Method | Path | Status | Description |
|---|---|---|---|
| GET | `/health` | Implemented | Basic process health |
| GET | `/api/version` | Implemented | App name/version |
| POST | `/auth/register` | Implemented, hardening required | Register user |
| POST | `/auth/login` | Implemented | Authenticate user |
| GET | `/auth/me` | Implemented | Return token payload for current user |
| POST | `/api/insert-user` | Development-only, remove/disable | Hard-coded DB test insertion |

The current registration handler accepts a raw dictionary and currently accepts a client-provided role. This is not a production-safe contract. Replace it with typed schemas and assign the normal learner role server-side.

## 3. Authentication

### POST /auth/register
Current request shape inferred from the existing handler:

```json
{
  "name": "Example Learner",
  "email": "learner@example.com",
  "password": "use-a-strong-password"
}
```

Target behavior:
- Validate email and password.
- Normalize email.
- Assign the default learner role on the server.
- Never accept an arbitrary privileged role from public registration.
- Return a safe user profile; never return a password hash.

### POST /auth/login
Request:

```json
{
  "email": "learner@example.com",
  "password": "use-a-strong-password"
}
```

Response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### GET /auth/me
Requires bearer token. Target response is a safe profile with user ID, name, email and role. Current implementation returns the token payload and should be refined.

## 4. Planned document and question-set endpoints

### POST /api/documents/question-paper
Multipart form:
- `file`: question-paper PDF.

Returns document ID, status and safe metadata.

### POST /api/documents/answer-key
Multipart form:
- `file`: separate answer-key PDF.

Returns document ID, status and safe metadata.

### POST /api/question-sets
JSON body:

```json
{
  "title": "GATE CSE - Operating Systems Practice",
  "question_pdf_id": "65f000000000000000000001",
  "answer_pdf_id": "65f000000000000000000002"
}
```

### POST /api/question-sets/{question_set_id}/process
Starts extraction for both source PDFs. Return a processing job/status identifier.

### GET /api/question-sets/{question_set_id}/preview
Returns extracted questions, options, source pages, confidence, and answer-key candidates. Do not use this endpoint to expose the verified answer key during a Real Exam attempt.

### PATCH /api/question-sets/{question_set_id}/verification
Persists learner corrections and verification. The server must validate question numbers and option labels, and only set the question set to verified when all required mappings are verified.

## 5. Planned exam endpoints

### POST /api/exams
Request:

```json
{
  "title": "GATE CSE Mock Test 01",
  "question_set_id": "65f000000000000000000003",
  "duration_minutes": 180,
  "mode": "real",
  "marks_correct": 1,
  "marks_incorrect": -0.33,
  "question_numbers": [1, 2, 3, 4]
}
```

Validation:
- Question set must belong to caller and be verified.
- All question numbers must exist in the set.
- Duration must be bounded.
- `marks_correct >= 0`; `marks_incorrect <= 0`.
- Supported modes: `practice`, `real`.

### POST /api/exams/{exam_id}/attempts
Creates an attempt. The server records `started_at` and `deadline_at`. The response contains the exam questions but never answer-key values in Real Exam Mode.

### GET /api/attempts/{attempt_id}
Returns attempt status, deadline, question list and saved response state, scoped to owner.

### PUT /api/attempts/{attempt_id}/responses/{question_number}
Request:

```json
{
  "selected_option": "B",
  "marked_for_review": false
}
```

Save idempotently by attempt and question. Reject writes after submission or deadline.

### POST /api/attempts/{attempt_id}/submit
Closes an attempt and evaluates it. Must be idempotent: repeated calls return the same final result.

### GET /api/attempts/{attempt_id}/result
Returns aggregate score, correct/incorrect/unanswered counts and accuracy.

### GET /api/attempts/{attempt_id}/review
Returns per-question selected answer, correct answer, status and explanation if available. Only available after submission in Real Exam Mode.

### GET /api/attempts/{attempt_id}/annotated-pdf
Returns an authenticated PDF download or a short-lived authorized download URL.

## 6. Standard response examples

Successful result:

```json
{
  "attempt_id": "65f000000000000000000010",
  "status": "evaluated",
  "summary": {
    "correct_count": 52,
    "incorrect_count": 18,
    "unanswered_count": 30,
    "attempted_count": 70,
    "score": 46.06,
    "accuracy_percent": 74.2857
  }
}
```

Error:

```json
{
  "detail": "Question set has unverified answer-key entries"
}
```

## 7. HTTP status guidance

- 200: successful read/update.
- 201: resource created.
- 202: processing accepted.
- 400: invalid state or malformed business input.
- 401: missing/invalid/expired authentication.
- 403: authenticated but not authorized.
- 404: resource absent or not visible to caller.
- 413: upload too large.
- 415: unsupported media type.
- 422: request validation failure.
- 429: rate limit exceeded.
- 500: unexpected server error; do not expose stack traces.

## 8. API security rules

- Enforce owner scoping in database queries, not only in frontend navigation.
- Do not return answer keys in Real Exam question payloads.
- Check the server deadline on every response write and submit.
- Validate every question number against the attempt's frozen question list.
- Do not trust client-supplied score, correctness, timestamps, role, owner ID, or report path.
- Apply upload quotas, rate limits, and file validation.
