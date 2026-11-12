# Secure Exam Portal

A PDF-based MCQ examination and review platform designed for GATE preparation.

## Product flow

1. Upload a question-paper PDF and its separate answer-key PDF.
2. Extract questions, options, and answer mappings.
3. Verify extracted questions and answer-key mappings before creating an exam.
4. Configure a timed Practice Mode or Real Exam Mode.
5. Attempt questions in a browser and submit the exam.
6. Review the score and question-wise answers.
7. Download the original question PDF annotated with correct and incorrect answers.

## Confirmed product decisions

- **Answer source:** separate answer-key PDF; verified mappings are the scoring source of truth.
- **PDF output:** annotate a copy of the original question paper.
- **Modes:** Practice Mode and Real Exam Mode.

## Technology

- Frontend: React + Tailwind CSS
- Backend: FastAPI (Python)
- Database: MongoDB
- Authentication: JWT
- PDF processing: PyMuPDF; OCR fallback planned for scanned PDFs

## Repository structure

- `backend/app`: FastAPI application
- `docs/PRODUCT_SPEC.md`: product requirements, workflows, API plan, and security requirements

## Development status

The product foundation is being migrated from a generic online-exam concept to a PDF-driven GATE practice workflow. PDF ingestion, verified answer-key mapping, timed attempts, evaluation, and annotated PDF generation are the MVP milestones.

## Important safeguards

- The answer-key PDF is the source of truth; AI must not decide correctness.
- Answer mappings must be verified before an exam can be started.
- Real Exam Mode must not expose answers before submission.
- Never commit `.env` files or credentials. Rotate any credentials that were previously exposed.
