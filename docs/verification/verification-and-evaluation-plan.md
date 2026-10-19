# Verification and Evaluation Plan — MedRisk

**Version:** 1.0 · **Stage:** pre-defense 0 · **Date:** 19 October 2026
**Goal of the plan:** demonstrate *how* the diploma aim will be shown to be achieved —
with measurable metrics, controlled conditions and explicit baselines.

---

## 1. What is being verified

| Layer | Statement to be demonstrated |
|---|---|
| ML | ML models over a short questionnaire predict CVD/T2D risk at least as well as clinical baselines, with acceptable calibration and no large subgroup gaps |
| Software | The system implements all **Must** requirements of the [requirements specification](../requirements/requirements-specification.md) and meets its NFRs |
| UX | Non-technical users can complete the assessment and understand their report |
| Process | Work is traceable (Git + YouTrack), reproducible (seeded training, pinned data) |

## 2. Datasets, splits and conditions

| Item | Condition |
|---|---|
| Data | UCI Cleveland Heart Disease (CVD, n≈303), Pima Indians Diabetes (T2D, n≈768); Framingham-derived dataset for the clinical-score baseline if obtainable; otherwise the baseline score is computed on Cleveland/Pima with the published Framingham equation |
| Split | Stratified 70/30 train/test, fixed random seed (42); 5-fold stratified CV on the train part for tuning |
| Preprocessing | Imputation (median + missingness indicators), scaling where required, class imbalance handled by class weights / resampling **inside CV folds only** (no leakage) |
| Missing data | Both a complete-case variant and an imputation variant are reported — the questionnaire allows "I don't know" |
| Environment | Recorded: Python version, library versions (`pip freeze`), hardware, seed |

## 3. Model metrics and acceptance thresholds

| Metric | CVD | T2D | Acceptance (v1) |
|---|---|---|---|
| ROC-AUC (test) | required | required | ≥ 0.78 each |
| ROC-AUC 95 % CI (DeLong / bootstrap) | reported | reported | CI lower bound > 0.70 |
| vs. logistic-regression baseline | ΔAUC reported | ΔAUC reported | ML model ≥ baseline (Δ ≥ 0 or documented why not) |
| vs. clinical baseline (Framingham-style) | AUC reported | — | Comparison mandatory; gap documented |
| Calibration | Brier score + calibration curve | same | Brier ≤ published reference range; slope 0.8–1.2 |
| Discrimination thresholds | Sensitivity/specificity at the chosen operating point | same | Reported; operating point justified |
| Subgroups (NFR-09) | AUC per sex, per age band | same | Gap ≤ 0.05 or documented limitation |
| Explainability (RQ2) | SHAP top-factors vs. clinically known factors | same | Face-validity table in the evaluation report |

## 4. Baselines (why comparison is meaningful)

1. **Logistic regression** on identical features — the classical statistical baseline.
2. **Framingham-style clinical score** computed from the same inputs — anchors the ML results
   to a clinically interpretable reference (D'Agostino et al., 2008).
3. **Dummy classifier** (stratified) — sanity floor for AUC ≈ 0.5.

## 5. Software verification activities

| Activity | Scope | Tool | When |
|---|---|---|---|
| Unit tests | preprocessing, scoring, categorization, SHAP wrapper, auth utils | pytest | continuous (CI) |
| API contract tests | every endpoint: valid, boundary, invalid, auth/negative | pytest + httpx, schemathesis vs OpenAPI | continuous |
| Integration tests | DB round-trips, history, deletion (NFR-04), model-version audit (NFR-08) | pytest + testcontainers/SQLite | continuous |
| E2E tests | guest flow: questionnaire → report → disclaimer; auth flow: history → delete | Playwright | weekly |
| Performance test | 50 VU × 5 min, p95 ≤ 500 ms, error rate < 0.1 % (NFR-01) | k6 or locust | before each pre-defense |
| Security checks | gitleaks scan, no plaintext passwords, JWT expiry, input validation | gitleaks + manual checklist | before each pre-defense |
| Reproducibility run | retrain twice, ΔAUC ≤ 0.01 (FR-10, NFR-12) | `make train` | milestone M4 |
| Clean-machine deployment | Docker Compose from README ≤ 15 min (NFR-10) | manual, recorded | milestone M4 |

## 6. Requirements → verification traceability (Must requirements)

| Req | Verification method | Evidence artifact |
|---|---|---|
| FR-01 | API contract tests (15+ cases) | test report |
| FR-02 | API integration tests | test report |
| FR-03 | E2E DOM assertions | Playwright report |
| FR-04 | Unit test on explainer + E2E | test report |
| FR-05 | Auth integration + negative tests | test report |
| FR-06 | Integration tests (list/delete) | test report |
| FR-09 | Endpoint test + doc consistency check | test report |
| FR-10 | Seeded retrain run, metrics diff | `ml/reports/` |
| FR-13 | schemathesis vs committed OpenAPI | CI log |
| NFR-01 | Load test | k6 report |
| NFR-03 | gitleaks + DB dump inspection | CI log |
| NFR-04 | Deletion integration test | test report |
| NFR-05 | Usability test, SUS | protocol + SUS scores |
| NFR-06 | E2E disclaimer assertion | Playwright report |
| NFR-07 | Model card existence & completeness | `docs/ml/model-card.md` |
| NFR-08 | Schema + integration test | test report |
| NFR-09 | Subgroup table in evaluation report | evaluation report |
| NFR-12 | Double retrain, metrics diff | `ml/reports/` |

## 7. Usability evaluation (NFR-05)

- **Method:** think-aloud task test, n ≥ 5 (mixed: students + non-technical adults).
- **Tasks:** (1) complete questionnaire as guest; (2) find the two risk numbers; (3) name
  your top risk factor; (4) save the assessment with an account.
- **Metrics:** task success rate (target ≥ 90 %), time on task, SUS score (target ≥ 70),
  comprehension questions (target ≥ 80 % correct).
- **Condition:** same prototype version for all participants; results recorded in
  `docs/verification/usability-report.md`.

## 8. Limitations acknowledged in advance

- Public datasets are small and population-specific (Cleveland: US, 1988; Pima: specific
  population) → external validity is limited; results are reported as *proof of method*.
- Self-reported questionnaire data differ from clinical measurements → we report an
  error-model caveat and design the UI to discourage self-diagnosis.
- Evaluation is retrospective; no prospective clinical study is planned (out of scope).

## 9. Reporting

All runs produce machine-readable artifacts committed under `ml/reports/` (metrics JSON +
plots) and summarized in `docs/evaluation/evaluation-report.md` before each pre-defense.
