# Pre-defense 1 submission (24 October 2026)

Submission note required by step 8 of the repository requirements: for every submission the
team provides the repository link, the tag of the submitted version, a summary of the work
done, known limitations and outstanding tasks.

| Item | Value |
|---|---|
| Repository | <https://github.com/kkfes/MedRisk> (public) |
| Tag | [`pre-defense-1`](../../../releases/tag/pre-defense-1) |
| Stage | Milestone **M0 — Concept** (pre-defense 1) |
| YouTrack | <https://medrisk.youtrack.cloud/projects/DIP> — tasks DIP-1 … DIP-46 |
| Date | 24 October 2026 |

## Summary of completed work

- **Analysis:** project proposal with problem statement, target users, aim, objectives,
  expected outcomes and scope.
- **Research:** literature review of 18 scientific sources (plus 3 grey sources) with a
  structured analysis table; comparison of 5 existing systems against 9 criteria with
  evidence; technology comparison covering 6 key decisions with 2–3 alternatives each.
- **Requirements:** 25 functional and non-functional requirements with MoSCoW priorities,
  acceptance criteria and a verification traceability table.
- **Design:** architecture description with system-context, use-case, component, sequence
  and ER diagrams — editable Mermaid sources plus SVG exports.
- **UX:** four static HTML mockups of the key user scenarios (landing, questionnaire,
  risk report, history). Marked as early sketches, not the final design.
- **Verification planning:** metrics, acceptance thresholds, baselines and evaluation
  procedure.
- **Management:** roles, milestones M0–M6, risks and dependencies; Git repository with
  traceable commits; YouTrack project with 46 prioritised, assigned and scheduled tasks.

All documents are preliminary and may change during implementation (changes are recorded
as ADRs and committed like any other change).

## Known limitations

- Runnable application code is not expected at M0 — implementation starts at M1.
- The ML models are not trained yet; no accuracy claims are made at this stage.
- The UI is a clickable sketch only, with illustrative calculations.
- The technology stack and architecture are an approximate variant for discussion.
- Evidence of relevance (user interviews) is collected but the interview log is completed
  during M0/M1.
- Supervisor review comments are recorded in `docs/supervisor/feedback-log.md`.

## Outstanding tasks

| Task | Owner | Milestone |
|---|---|---|
| DIP-44 Evidence of relevance: 3–5 interviews with user representatives | Team | M0 |
| DIP-43 Supervisor review of M1–M4 results | Supervisor | M5 |
| DIP-12 … DIP-46 Data, models, API, frontend, evaluation | Zarina, Sara, Muslim | M1–M6 |
