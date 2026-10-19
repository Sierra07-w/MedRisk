# Source code (planned from milestone M1)

Application code of the MedRisk backend, organized by component:

```
src/app/api/          # FastAPI routers, request/response schemas
src/app/services/     # risk, explanation, history, auth services
src/app/ml/           # inference wrapper, model bundle loading
src/app/db/           # SQLAlchemy models, migrations (alembic)
```

Nothing is implemented yet — at pre-defense 0 the repository contains analysis, design and
planning artifacts only. The architecture is an **approximate variant** and may change
(see `docs/architecture/architecture-description.md` §7).
