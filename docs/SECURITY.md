# Security and Privacy Guide

## 1. Security objectives

Protect learner accounts, uploaded PDFs, answer keys, active exam integrity, attempt records, and generated reports. The platform is intended for personal exam preparation, but it must still treat answer keys and uploaded study materials as private user data.

## 2. Authentication and authorization

- Hash passwords with bcrypt (or a currently supported password-hashing configuration).
- Never store or log plaintext passwords.
- Normalize email addresses and enforce a unique index.
- Public registration must assign the learner role server-side.
- Do not permit a user to self-register as examiner/admin.
- Validate JWT signature, algorithm, expiry and subject.
- Use short-lived access tokens in production; consider refresh-token rotation and revocation.
- Apply authorization to every document, question set, exam, attempt and report.
- Query resources by both resource ID and authenticated owner ID to prevent insecure direct object references.

## 3. Answer-key secrecy and exam integrity

- Never send correct answers in Real Exam question payloads.
- Do not include answer keys in frontend bundles, local storage, hidden DOM fields, or client-side scoring code.
- Do not trust client-submitted score, correctness, user ID, role, start time, deadline or answer-key data.
- Check the deadline on the server for every answer write and submit request.
- Reject response changes after submission/expiry.
- Make submit and evaluation idempotent.
- Store a scoring and answer-key snapshot with the attempt so later edits to a question set do not rewrite historical results.
- Practice Mode may reveal feedback only according to its configured feedback policy.

## 4. PDF upload security

- Accept only PDF documents and validate file signature/magic bytes, not only extension or browser MIME type.
- Enforce maximum file size, page count, processing time and extracted-content limits.
- Use random storage names; never trust user-provided paths.
- Store uploads outside the public web root or in private object storage.
- Do not execute or render embedded active content.
- Consider malware scanning for a public multi-user deployment.
- Use timeouts and resource limits for parsing and OCR.
- Treat extracted text as untrusted input.
- Keep source PDFs immutable and generate reports as separate files.
- Authorize downloads and use short-lived signed URLs only when necessary.

## 5. Secrets and configuration

- Never commit `.env`, database credentials, JWT secrets, API keys or private storage credentials.
- Keep a restrictive `.gitignore` and provide a sanitized `.env.example`.
- Rotate credentials immediately if they were committed or exposed.
- Use separate secrets for local, staging and production.
- Use TLS in production.
- Avoid placing secrets in frontend variables; frontend variables are public.

The repository review previously found a committed backend `.env` file. Treat all credentials that were present in that file as exposed: rotate them, remove the file from current tracking, and review Git history. Deleting a file in a later commit does not erase it from past commits.

## 6. Existing code requiring remediation

The initial backend contains:
- Registration that accepts a role from the request body.
- A development database insertion endpoint without authentication.
- Raw dictionary request bodies without Pydantic validation.
- Password helpers that strip whitespace before hashing/verifying.
- JWT error responses that include exception detail.

Address these before a public deployment. Remove or protect the DB test route, force the default role server-side, validate inputs, preserve exact password bytes/characters, and return generic authentication errors.

## 7. Privacy and retention

- Collect only data needed for accounts, documents and exam history.
- Define a user-facing retention/deletion policy before public launch.
- Delete stored PDF files when a user deletes a document, subject to attempt/report retention rules.
- Avoid logging extracted question text or answer keys unless necessary for debugging and explicitly protected.
- Restrict operational access to production documents.

## 8. Security release checklist

- [ ] All previously exposed secrets rotated.
- [ ] No secrets tracked by Git or present in build artifacts.
- [ ] Role escalation blocked.
- [ ] Ownership checks applied to all resource routes.
- [ ] Answer key hidden during Real Exam Mode.
- [ ] Server-side deadline enforcement enabled.
- [ ] Upload signature, size and page-count validation enabled.
- [ ] Private storage and authorized downloads configured.
- [ ] Rate limits and request-size limits configured.
- [ ] Generic error responses; no stack traces or secrets exposed.
- [ ] Dependency and container image scanning completed.
