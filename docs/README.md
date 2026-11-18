# Documentation Index

This directory contains the product, architecture, API, data, development, security, and operations documentation for Secure Exam Portal.

## Start here

| Document | Audience | What it covers |
|---|---|---|
| [Product specification](PRODUCT_SPEC.md) | Product, developers | Scope, user journeys, requirements, modes, MVP |
| [Architecture](ARCHITECTURE.md) | Developers | Components, boundaries, processing flows, design decisions |
| [Data model](DATA_MODEL.md) | Backend developers | MongoDB collections, relationships, indexes, lifecycle |
| [API reference](API.md) | Frontend/backend developers | Current endpoints and planned API contracts |
| [Developer guide](DEVELOPMENT.md) | Contributors | Local setup, configuration, conventions, workflow |
| [User guide](USER_GUIDE.md) | Learners | PDF preparation, verification, exams, results, reports |
| [Security](SECURITY.md) | All contributors | Threat model, access control, file handling, secrets |
| [Testing and deployment](TESTING_DEPLOYMENT.md) | Developers/operators | Test strategy, deployment, monitoring, release checklist |

## Implementation status

The repository is in an initial product-foundation stage. Existing authentication and basic health/version endpoints are present. Exam schemas and a deterministic scoring service have been added on the feature branch. PDF upload, OCR, answer-key verification UI, exam-session APIs, persistence for attempts, and annotated PDF generation are planned and are not yet complete.

Treat API sections marked **Planned** as design contracts, not as endpoints that can currently be called.

## Product invariants

1. The separately uploaded answer-key PDF is the source of truth.
2. An answer-key mapping must be reviewed and verified before it can be used for scoring.
3. AI or OCR may extract candidate content but must never silently determine correctness.
4. Real Exam Mode must not expose answers or correctness until the attempt is submitted.
5. Annotated reports are generated as new files; original uploads are immutable.
6. Every resource access is scoped to its authenticated owner.
