# Tests (planned from milestone M1)

```
tests/unit/         # preprocessing, scoring, categorization, SHAP wrapper, auth utils
tests/integration/  # API + DB round-trips, history, deletion, model-version audit
tests/e2e/          # Playwright: guest flow, auth flow, disclaimers
tests/performance/  # k6/locust scripts (p95 latency budget, NFR-01)
```

Coverage target for the backend: ≥ 70 % (NFR-11). CI runs unit + integration + contract
tests on every pull request (see `CONTRIBUTING.md`).
