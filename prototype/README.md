# MedRisk Prototype (mockups)

> **Status: early design sketches, not the final design.** These static pages exist to
> discuss and validate user scenarios with real users and the supervisor. Visual style,
> information architecture, wording and the set of screens **will change** after that
> feedback, and the current backend design is likewise an approximate variant that may
> change during implementation.

## Scenarios covered (UX / prototype, pre-defense 0)

| # | User scenario | Mockup | Requirements covered |
|---|---|---|---|
| S1 | First-time visitor understands what the system does and starts an assessment | [index.html](index.html) | FR-03 (disclaimer), NFR-05 (usability), NFR-06 (safety) |
| S2 | Guest fills the health questionnaire (incl. "I don't know" values) | [assessment.html](assessment.html) | FR-01, FR-05 (guest mode) |
| S3 | User receives the risk report: two risks, categories, factor attribution, next steps, disclaimer | [result.html](result.html) | FR-02, FR-03, FR-04, NFR-06 |
| S4 | Registered user views assessment history, trends and manages own data | [dashboard.html](dashboard.html) | FR-06, FR-07, NFR-04 (privacy) |

## How to view

```bash
cd prototype
python3 -m http.server 8000   # open http://localhost:8000
```

No build step is required; plain HTML/CSS, no JS framework — intentional at the sketch stage
(technology comparison, D4: the production frontend stack is decided later).
