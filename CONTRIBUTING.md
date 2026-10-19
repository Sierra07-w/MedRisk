# Contributing — MedRisk

Rules the whole team (and the supervisor) follows. Required by the diploma repository
requirements (steps 5–7).

## 1. Git workflow

- **main** is the reviewed baseline. Direct pushes to `main` are forbidden.
- Every change lives in a task branch: `DIP-<id>-<short-slug>`
  (example: `DIP-23-database-schema`).
- Commit messages start with the task ID and are descriptive:

  ```
  DIP-23: Add initial database schema and ER diagram

  - users, assessments, risk_results, factor_contributions tables
  - alembic migration with up/down
  - verified against docs/architecture/diagrams/er-diagram.mmd
  ```

- Commit as you go — each commit must be a coherent change. Documentation and diagram
  changes are committed the same way as code. Uploading everything the night before a
  pre-defense is not acceptable.
- Every team member commits under **their own account** with their real name and e-mail:
  `git config user.name "Zarina Kosaman"`, `git config user.email <their email>`.
  Shared accounts are forbidden.

## 2. Pull requests

1. Push the branch and open a PR against `main`.
2. PR description must contain: what changed and why, the YouTrack task ID, how it was
   checked (tests run, manual steps), screenshots for UI changes.
3. **Reviewer:** another team member (for documentation PRs, any team member; for
   architecture/ML PRs, the responsible lead). The supervisor reviews significant changes
   at agreed checkpoints (M0, M2, M4, M5).
4. Resolve review comments by pushing commits (do not force-push during review).
5. Merge only after approval + green CI.

## 3. Task rules

- Create a YouTrack task for every meaningful work item: responsible student, expected
  outcome, acceptance criteria, deadline.
- Mark a task Done **only** when its acceptance criteria are met; link the PR/commit in the task.

## 4. Repository hygiene

- No passwords, API keys, personal or patient data — ever. Use `.env.example` with
  placeholders; real `.env` is git-ignored.
- Public datasets only; download scripts go in `data/`, raw/processed data stays out of Git.
- Diagrams: commit the editable source (`.mmd`) **and** the rendered export.
- Documentation lives in `docs/`, generated reports in `ml/reports/`.

## 5. Tags (pre-defense submissions)

For each stage the team tags the exact submitted version — never move or replace an
existing tag:

```
git tag -a pre-defense-1 -m "Pre-defense 1 submission"
git push origin pre-defense-1
```

Stages: `pre-defense-1`, `pre-defense-2`, `final-pre-defense`.
