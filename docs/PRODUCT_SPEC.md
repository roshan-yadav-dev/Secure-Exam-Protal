# Secure Exam Portal — Product Specification

## Product direction
A personal PDF-based MCQ examination and review platform for GATE preparation. A learner uploads a question-paper PDF and its separate answer-key PDF, configures a timed exam, attempts it in a browser, reviews the result, and downloads the original question paper annotated with answer correctness.

## Confirmed product decisions
- Answer source: a separate answer-key PDF.
- Result artifact: annotate the original question-paper PDF; preserve its pages and visual structure.
- Examination modes: Practice Mode and Real Exam Mode.

## Primary user journey
1. Authenticate and open the learner dashboard.
2. Upload a question-paper PDF and a separate answer-key PDF.
3. Extract question numbers, stems, options, and answer-key mappings.
4. Review and correct extracted content and answer mappings. The exam cannot be published until every included question has a verified answer mapping.
5. Configure an exam: title, selected questions, duration, marks for correct answers, negative marks, and mode.
6. Attempt the exam in a browser with question palette, previous/next navigation, save answer, mark-for-review, countdown, and submission confirmation.
7. Evaluate against the verified answer key.
8. Review question-wise correctness and score breakdown.
9. Download an annotated copy of the original question PDF.

## Modes
### Practice Mode
- Learner may choose immediate feedback after answering or feedback only after finishing.
- Correct answer and explanation are shown only when feedback is enabled.
- Attempts and review data are saved.

### Real Exam Mode
- Never reveal the answer key or correctness during the active attempt.
- Countdown timer; server-authoritative expiry and auto-submit.
- Results and answer review are available only after submission/expiry.

## PDF ingestion and verification
- Accept PDF files only; enforce configurable file-size and page-count limits.
- Store uploads privately and associate them with the authenticated owner.
- Extract text/layout with PyMuPDF. OCR is a fallback for scanned pages and should be added as a separate processing stage.
- Support question numbers and option labels A-D in the first release.
- Keep extraction confidence and page references so uncertain items can be reviewed.
- Never infer correctness from an AI answer. The answer-key PDF is the source of truth.
- Require human verification of answer-key mapping before an exam can be started.
- If question numbering is ambiguous or missing, require manual mapping.

## Annotated original PDF
- Generate a new file from the original question PDF; never overwrite the source upload.
- Preserve page order, diagrams, equations, and original text as much as possible.
- Green highlight/outline: verified correct option.
- Red highlight/outline: learner's selected incorrect option.
- For an unanswered question, mark the correct option green and label the question as unanswered.
- Add a compact legend and attempt summary page or header/footer without obscuring source content.
- If precise option coordinates cannot be confidently located, add a page-level review note rather than placing a misleading highlight.
- Store the generated report against the attempt and provide an authenticated download.

## Scoring
- Each question stores marks for correct and negative marks for incorrect; unanswered questions score zero.
- Total score = sum of per-question scores. Accuracy = correct / attempted * 100; show N/A when no questions were attempted.
- Store the scoring configuration as an immutable snapshot on the exam attempt.
- Only verified answer-key mappings are eligible for scoring.

## Core data entities
- users: identity, password hash, role, created_at.
- pdf_documents: owner_id, kind (question_paper/answer_key), storage_key, filename, page_count, processing_status.
- question_sets: owner_id, title, question_pdf_id, answer_pdf_id, verification_status.
- questions: question_set_id, question_number, stem, options, source_page, extraction_confidence.
- answer_keys: question_set_id, question_number, correct_option, verification_status, source_page.
- exams: owner_id, question_set_id, title, duration_seconds, mode, marks_correct, marks_incorrect, question_order.
- exam_attempts: exam_id, user_id, started_at, submitted_at, status, scoring_snapshot.
- responses: attempt_id, question_number, selected_option, marked_for_review, answered_at.
- results: attempt_id, correct_count, incorrect_count, unanswered_count, score, accuracy.
- generated_reports: attempt_id, storage_key, generated_at.

## API surface (planned)
- POST /api/documents/question-paper
- POST /api/documents/answer-key
- POST /api/question-sets/{id}/process
- GET /api/question-sets/{id}/preview
- PATCH /api/question-sets/{id}/verification
- POST /api/exams
- POST /api/exams/{id}/attempts
- PUT /api/attempts/{id}/responses/{question_number}
- POST /api/attempts/{id}/submit
- GET /api/attempts/{id}/result
- GET /api/attempts/{id}/review
- GET /api/attempts/{id}/annotated-pdf

## Security and reliability requirements
- Do not expose answer-key data to the browser during a Real Exam attempt.
- Enforce ownership checks on every document, question set, exam, attempt, and report.
- Use server-side time validation; client countdown is display-only.
- Validate MIME type and PDF signature, impose upload/page limits, and use random storage names.
- Keep files outside the public web root; authorize downloads.
- Remove public/debug database mutation endpoints before production.
- Never commit .env or secrets. Rotate any credentials previously committed to the repository.
- Use transactions or idempotent submission logic to prevent duplicate scoring on repeated submit requests.

## MVP scope and delivery order
1. Repository foundation, product docs, schemas, and scoring rules.
2. Secure PDF upload and document metadata.
3. Text extraction, OCR fallback, question/answer-key preview and manual verification.
4. Exam configuration and timed attempt engine.
5. Evaluation, history, and question-wise review.
6. Annotated original PDF generation.
7. Tests, deployment hardening, and accessibility/mobile polish.

## Explicitly out of scope for the first MVP
- Webcam proctoring, browser lockdown, coding compiler, AI-generated questions, and AI-decided answer keys.
- Automatic perfect reconstruction of arbitrary scanned/complex PDFs. Low-confidence layouts must be reviewed by the learner.
