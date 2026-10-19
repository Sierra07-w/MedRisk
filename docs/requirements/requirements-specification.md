# Requirements Specification — MedRisk

**Version:** 1.0 · **Stage:** pre-defense 0 · **Date:** 19 October 2026
**Priority model:** MoSCoW — **M**ust have (v1), **S**hould have (v1 if time),
**C**ould have (future), **W**on't have (out of scope).
Every **Must** requirement has a verifiable acceptance criterion that maps to a test
(see [verification plan](../verification/verification-and-evaluation-plan.md)).

---

## 1. Functional requirements

| ID | Requirement | Priority | Acceptance criterion (verifiable) |
|---|---|---|---|
| FR-01 | The system shall accept a structured health questionnaire (age, sex, smoking status, systolic/diastolic BP, total & HDL cholesterol, glucose/HbA1c, BMI or weight+height, physical activity level, family history of CVD/T2D, known hypertension/diabetes diagnosis) | **M** | Given the assessment page, When all required fields are filled with valid values, Then an assessment is accepted; invalid fields are rejected with a field-level message. Covered by ≥15 API contract test cases (boundary + invalid values) |
| FR-02 | The system shall compute a 10-year cardiovascular-disease risk estimate and a type-2-diabetes risk estimate for the same input | **M** | `POST /api/v1/assessments` returns both risks in one response; each with a probability (0–1) and a category (low / moderate / high / very high). Verified by API integration tests |
| FR-03 | Each risk shall be presented with its category, a plain-language summary and a "not a diagnosis" disclaimer | **M** | The result page contains the numeric value, category label, summary text and disclaimer for **both** risks (DOM assertions in E2E tests) |
| FR-04 | The system shall explain each risk with per-factor contributions (SHAP): the top ≥5 contributing factors with direction (increases/decreases) and relative magnitude | **M** | The result payload contains a `factors` array of ≥5 entries with `name`, `direction`, `contribution`; rendering shows them in descending |contribution| order. Verified by unit test on explainer output + E2E check |
| FR-05 | The system shall provide a guest mode (assessment without registration) and an authenticated mode (account: e-mail + password) | **M** | Guest can complete FR-01…FR-04 without any account; registered user additionally gets FR-06. Negative auth tests (wrong password, expired token) return 401 |
| FR-06 | A registered user shall have an assessment history (all previous assessments with date, both risks, category) and may delete a single record | **M** | After N≥3 assessments, `GET /api/v1/assessments` returns them ordered by date desc; `DELETE /api/v1/assessments/{id}` removes exactly that record and returns 204. Verified by integration tests |
| FR-07 | The system shall display a trend view of risk over time for a registered user (≥2 assessments) | **S** | With ≥2 assessments, the dashboard renders a line chart of each risk over time; with <2 assessments a hint is shown instead |
| FR-08 | The system shall provide an admin interface (or admin API endpoints) to list users, deactivate accounts and trigger model metadata view | **S** | Admin role can list users; non-admin gets 403 on all admin endpoints (authorization tests) |
| FR-09 | The system shall expose the model version, training-data description and evaluation metrics in the repository (model card) and via `GET /api/v1/models/current` | **M** | Endpoint returns model version, training date, dataset names and the headline metrics; the same data exists in `docs/` model card |
| FR-10 | The ML pipeline shall retrain both models from raw public data with a single reproducible command and produce the metrics report | **M** | `make train` (or documented command) reproduces test-set metrics within ±0.01 AUC of the committed report on the same data split (seeded) |
| FR-11 | The system shall log (locally, non-personally-identifiable) each risk computation: input hash, model version, output, timestamp | **S** | Every assessment record stores `model_version`; log entries contain no raw personal values. Verified by log-inspection test |
| FR-12 | The user interface shall be localized in English (v1); Russian and Kazakh are planned | **C** (RU/KZ) | v1: all UI strings via a translation table (i18n library) so RU/KZ can be added without code changes |
| FR-13 | The system shall provide an authenticated REST API documented by an OpenAPI 3 spec that is kept in sync with the implementation | **M** | OpenAPI spec is committed; CI check (schemathesis or openapi-diff) reports zero breaking changes vs. the committed spec |

## 2. Non-functional requirements

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| NFR-01 | **Performance:** risk computation round-trip (API, model inference, response) p95 ≤ 500 ms on the deployment host for a single user | **M** | Load test (k6/locust): 50 VU, 5 min, p95 ≤ 500 ms, error rate < 0.1 % |
| NFR-02 | **Availability:** the service shall be available ≥ 95 % during the diploma period (single-host deployment, restarts allowed) | **S** | Uptime log over 30 days; documented downtime causes |
| NFR-03 | **Security:** passwords stored as salted hashes (bcrypt/argon2); JWT access tokens ≤ 30 min; no credentials in the repository (`.env.example` with placeholders only) | **M** | Automated check: DB dump contains no plaintext passwords; `git secrets`/gitleaks scan passes; auth penetration checklist executed |
| NFR-04 | **Privacy:** guest assessments store no identity data; a user may delete their account with all assessment records (right to erasure) | **M** | After account deletion, `GET /api/v1/assessments` returns 401 and no rows remain in DB (integration test on a test DB) |
| NFR-05 | **Usability:** a first-time user completes questionnaire → report unassisted; SUS score ≥ 70 in the internal test (n ≥ 5) | **M** | Usability test protocol + SUS questionnaire results recorded in `docs/verification/` |
| NFR-06 | **Safety (decision support):** every risk output carries a visible disclaimer that this is not a medical diagnosis | **M** | E2E assertion on all result views (FR-03); disclaimer also present in API response text |
| NFR-07 | **Transparency:** a model card (data, features, metrics, limitations, intended use, subgroup results) is published in the repository | **M** | `docs/ml/model-card.md` exists, contains all sections of the template, and matches FR-09 endpoint data |
| NFR-08 | **Auditability:** every stored result references the model version that produced it | **M** | DB schema has `model_version` FK on results; verified by schema + integration tests |
| NFR-09 | **Fairness:** evaluation reports metrics per sex and per age group; any subgroup with >0.05 AUC gap vs. the overall model is documented as a limitation | **M** | Evaluation report contains per-subgroup AUC table; the model card lists limitations |
| NFR-10 | **Portability:** the whole system starts on a clean machine with Docker Compose (README steps) in ≤ 15 min | **S** | Clean-machine rehearsal recorded (time + steps) |
| NFR-11 | **Maintainability:** ≥ 70 % of the backend code covered by automated tests; linters (ruff/eslint) pass in CI | **S** | CI badge/coverage report; pipeline fails on lint errors |
| NFR-12 | **Reproducibility:** training is seeded; dataset download scripts pin dataset versions/URLs | **M** | Retraining reproduces metrics within FR-10 tolerance twice in a row |

## 3. Out-of-scope requirements (explicitly not required in v1)

Diagnosis or triage; treatment recommendations; EHR integration; native mobile apps;
regulatory certification; real patient data; LLM chatbot (see scope,
[project proposal §7](../proposal/project-proposal.md)).

## 4. Traceability

Each Must requirement is mapped to a verification method (unit / integration / E2E /
performance / usability / reproducibility run) in the
[verification plan](../verification/verification-and-evaluation-plan.md) §6 matrix and to at
least one YouTrack task in the [backlog](../management/youtrack-backlog.md).
