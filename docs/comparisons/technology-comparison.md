# Technology Comparison

**Project:** MedRisk · **Stage:** pre-defense 0 · **Date:** 19 October 2026

Six key technical decisions, 2–3 alternatives each, with the criteria taken from the
[requirements](../requirements/requirements-specification.md) and the team's skills
(see [project proposal](../proposal/project-proposal.md) § team). Scoring: ●●● best,
●●○ good, ●○○ acceptable, ○○○ not selected.

> **Note:** the selections below are the team's **preliminary (approximate) variant** for
> this stage. They are justified by the current requirements, but may be revised during
> implementation if practical experience proves otherwise — each revision will be recorded
> as an ADR (see [architecture description §7](../architecture/architecture-description.md)).

## D1. ML framework & modelling approach

| Criterion | scikit-learn (logistic regression + GBM) ●●● | LightGBM/XGBoost standalone ●●○ | Deep learning (PyTorch/TF) ●○○ |
|---|---|---|---|
| Fit to task (tabular clinical data) | Excellent for tabular; LR is the required baseline | Excellent; strongest tabular accuracy | Weak on small tabular sets; gains appear with EHR-scale data (Rajkomar et al., 2018) |
| Interpretability | Native coefficients + SHAP | SHAP-compatible | Harder (needs approximations) |
| Team skills | Zarina: pandas/NumPy/sklearn; Muslim: Python | Same + one extra library | Not in team skill set |
| Data scale | Cleveland ~300 rows, Pima ~768 rows — DL would overfit | Same | Same |
| Effort | Low | Low | High |

**Decision:** scikit-learn for preprocessing/pipelines/metrics + logistic regression as
baseline and **LightGBM as the main model** (usable through the same sklearn API and SHAP).
Deep learning is explicitly rejected for v1 with a documented rationale.

## D2. Backend platform

| Criterion | **FastAPI (Python)** ●●● | Spring Boot (Java) ●●○ | Django (Python) ●○○ |
|---|---|---|---|
| Shared code with ML layer | Same language — model loading, SHAP reuse are trivial | Requires an ML microservice or reimplementation | Same as FastAPI |
| Team skills | Muslim: Java/Spring **and** Python | Muslim's strongest stack | Less familiar |
| API docs | OpenAPI generated from Pydantic models | Manual/springdoc setup | DRF needs extra tooling |
| Performance | Async, ~Node/Go-class for I/O | Excellent | Good |
| Ecosystem fit | Best for ML-adjacent services | Best for large enterprise backends | Best for admin-heavy CRUD apps |

**Decision:** **FastAPI**. Rationale: one language for data/ML/backend minimizes integration
risk (Kelly et al., 2019 — the integration "last mile" is the main delivery risk); OpenAPI is
generated automatically; Muslim's Java/Spring experience transfers directly to service design.
Django was rejected (heavier than needed, no async benefit for this workload).

## D3. Data storage

| Criterion | **PostgreSQL 15** ●●● | SQLite ●●○ | MongoDB ●○○ |
|---|---|---|---|
| Relational integrity (users, assessments, model versions) | Full | Full (single-file) | Weak (document model) |
| JSON support for flexible questionnaire payloads | JSONB — excellent | JSON functions OK | Native |
| Production readiness | High (concurrent users, backups) | Low (single writer) | High |
| Ops burden | Medium (Docker service) | Minimal | Medium |
| Dev/test convenience | Good via Docker Compose | Best | Good |

**Decision:** **PostgreSQL in dev and prod (Docker service), SQLite allowed only for unit
tests.** Mongo was rejected: the data model is strongly relational (user → assessment →
result → factor contributions → model version), and auditability of model versions is a
requirement (NFR-8).

## D4. Frontend

| Criterion | **React + Vite + TypeScript** ●●○ | Vue 3 ●●● | Static HTML/CSS + htmx ●○○ |
|---|---|---|---|
| Team skills | Sara: design + basic JS; Muslim: JS/HTML/CSS | Not used by anyone yet | Simplest |
| Typed API client | OpenAPI codegen → TS types, excellent | Good via openapi-typescript | None |
| Long-term maintainability | Large ecosystem, many hiring resources | Equal or slightly smaller ecosystem | Limited for growing app |
| Effort for v1 | Medium | Medium | Low, but poor for dashboard/history |

**Decision:** **React + Vite + TypeScript.** Vue scored slightly higher on learning curve,
but the OpenAPI→TypeScript codegen (a must for a strict API contract with the backend) and
Muslim's existing JS experience outweigh it. The **prototype stage uses plain HTML/CSS**
(this folder), which keeps design iterations cheap and is fully committed to the repo.

## D5. Deployment & infrastructure

| Criterion | **Docker Compose (single host)** ●●● | PaaS (Railway/Render) ●●○ | Kubernetes ●○○ |
|---|---|---|---|
| Reproducibility for the committee | Perfect — one command | Depends on vendor | Poor |
| Cost | Zero (university host / laptop) | Free tier limits; vendor lock-in | High |
| Ops complexity | Low | Minimal | Far beyond project scope |
| Diploma-relevant skills | Containerization — valued | Some | Overkill |

**Decision:** Docker Compose with services: `api`, `db`, `frontend` (+ optional `ml-worker`).
Kubernetes rejected (NFR maintainability, 3-person team, single-host scale).

## D6. Model explainability tooling

| Criterion | **SHAP (TreeExplainer/KernelExplainer)** ●●● | Built-in feature importance ●●○ | LLM-generated explanations ●○○ |
|---|---|---|---|
| Per-prediction attribution | Yes, exact for tree models | No (global only) | No reliable attribution |
| Theoretical grounding | Shapley values (Lundberg & Lee, 2017) | Heuristic (impurity/gain) | None |
| Determinism / testability | Deterministic given the explainer | Deterministic | Non-deterministic, hard to test |
| Cost / integration | Local library, offline | Free | Extra API, privacy & cost concerns |

**Decision:** **SHAP** for quantitative attribution; plain-language templates render the top
factors into user-facing text. An **LLM module for free-text explanations is deferred**
(privacy, determinism, cost) and listed as future work in the scope.

## D7. Summary of selections

| # | Decision | Selected | Key reason |
|---|---|---|---|
| D1 | Modelling | scikit-learn + LightGBM | Tabular SOTA + interpretable + team skills |
| D2 | Backend | FastAPI (Python 3.11) | Shared language with ML, auto OpenAPI |
| D3 | Storage | PostgreSQL 15 | Relational integrity, JSONB, auditability |
| D4 | Frontend | React + TS (Vite) | Typed codegen from OpenAPI, ecosystem |
| D5 | Deployment | Docker Compose | Reproducible, zero cost |
| D6 | Explainability | SHAP (+ text templates) | Per-user, deterministic, grounded |

Each decision is revisitable: an ADR (architecture decision record) will be committed for
every change after M1.
