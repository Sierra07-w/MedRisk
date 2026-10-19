# Project Management — MedRisk

**Stage:** pre-defense 0 · **Date:** 19 October 2026

## 1. Team, roles and responsibilities

| Member | Role | Owns (directories) | Key responsibilities |
|---|---|---|---|
| **Muslim Syzdykov** (SE-2425) | Backend lead, team lead | `src/`, `docs/architecture/` | Architecture, REST API, DB, auth, ML integration, repo & CI administration, PR reviews |
| **Zarina Kosaman** (SE-2429) | Data / ML lead | `ml/`, `data/`, `docs/literature/` | Datasets, cleaning, training, evaluation, model card, metric reports |
| **Sara Mukhammad** (SE-2419) | Frontend / UX lead | `frontend/`, `prototype/` | Design, UI implementation, usability testing, user-facing texts |
| **Aigerim Bakiyeva** | Supervisor | `docs/supervisor/` | Methodology, review of deliverables, approval of milestones |

**RACI (Responsible / Accountable / Consulted / Informed)** — see
[project-management table below](#4-decision-and-review-rules).

## 2. Milestones

| ID | Milestone | Deliverable | Target date | Status |
|---|---|---|---|---|
| **M0** | Concept & pre-defense 0 | Proposal, literature review, comparisons, requirements, diagrams, prototype, verification plan, repo + YouTrack | **24 Oct 2026** | ✅ prepared |
| **M1** | Data & baselines | Data pipeline, data-quality report, logistic-regression + Framingham-style baselines with metrics | 15 Nov 2026 | planned |
| **M2** | ML models & explanations | LightGBM models, SHAP explanations, model card v1, evaluation report v1 | 06 Dec 2026 | planned |
| **M3** | Backend API | FastAPI service, DB schema, auth, OpenAPI spec, contract tests | 27 Dec 2026 | planned |
| **M4** | Frontend & integration | React app, end-to-end guest + auth flows, usability test, performance test | 24 Jan 2027 | planned |
| **M5** | Pre-defense-1 | Tag `pre-defense-1`, full documentation update, demo | 07 Feb 2027 | planned |
| **M6** | Final | Thesis, final evaluation, tag `final-pre-defense` | Mar 2027 | planned |

**Cadence:** weekly meeting with the supervisor (demo + blockers), weekly internal sync,
two-week iterations, PR review within 48 h.

## 3. Risks and mitigations

| # | Risk | P | I | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | Public datasets too small → models below AUC target | M | H | Use CV + boosting; document honest results; fallback to "≥ baseline" success criterion agreed with supervisor | Zarina |
| R2 | Framingham dataset unavailable for baseline | M | M | Compute Framingham-style score on Cleveland with published coefficients; state approximation | Zarina |
| R3 | Team workload (study + jobs) slips milestones | H | H | Small vertical slices; tasks ≤ 3 days; weekly sync; scope cuts pre-agreed (drop FR-07 → FR-08 → FR-12) | Muslim |
| R4 | Integration failure between ML and API | M | H | Model bundle contract (input schema + metadata) defined in M1; inference wrapped in a versioned module with tests | Muslim |
| R5 | Privacy incident (real personal data in repo) | L | H | `.gitignore` rules, gitleaks in CI, only public datasets, config examples with placeholders | Muslim |
| R6 | Usability test below SUS 70 | M | M | Test the prototype early (M3), iterate; Sara owns UX debt backlog | Sara |
| R7 | Bias/fairness gap in subgroup metrics | M | M | Subgroup reporting mandatory (NFR-09); limitations documented, not hidden | Zarina |
| R8 | Supervisor unavailable during travel | M | M | Questions batched weekly; decisions recorded in PR descriptions + feedback log | All |
| R9 | Single-host deployment downtime | M | L | Docker Compose restart policies; demo prepared offline (recorded video backup) | Muslim |

P = probability, I = impact (H/M/L).

## 4. Decision and review rules

- **main** is always deployable; protected: no direct pushes, PR required.
- Every PR: 1 reviewer from the team (not the author), supervisor reviews documentation and
  significant architectural PRs at checkpoints (M0, M2, M4, M5).
- Decisions are recorded as **ADR** documents in `docs/adr/` (one per technology/architecture
  change after M1).
- Blocking disagreements escalate to the supervisor; the decision is logged in
  [feedback log](../supervisor/feedback-log.md).

## 5. Dependencies

| Dependency | Type | Needed by | Status |
|---|---|---|---|
| Topic approval by dean & supervisor | External | M0 | in progress (statements filed) |
| YouTrack project creation | Tooling | M0 | pending — backlog ready for import |
| GitHub repository access for team + supervisor | Tooling | M0 | pending (repo prepared locally) |
| Public dataset availability (UCI, Kaggle Framingham) | Data | M1 | UCI confirmed; Framingham — to verify |
| Supervisor feedback turnaround ≤ 1 week | Human | all | agreed |
| Hosting for demos (university server or cloud) | Infra | M3–M4 | to be decided |

## 6. Individual contribution tracking

- Each meaningful work item = a YouTrack task with assignee, acceptance criteria and deadline.
- Branch naming: `DIP-<id>-<slug>`; commit messages start with the task ID; PR links the task.
- Contribution evidence per member: Git author history + merged PRs + YouTrack task completion
  (required by the diploma process: "evidence of progressive contributions from each team member").
- Commits must be frequent and coherent; uploading everything right before a pre-defense is
  not acceptable (see repository requirements, step 5).
