# MaktedCRM Backend

FastAPI + PostgreSQL + SQLAlchemy + Alembic ile backend iskeleti.

## Çalıştırma

```bash
docker compose up --build
```

## URL'ler

- API: http://localhost:8000
- Health (DB check): http://localhost:8000/health
- Swagger: http://localhost:8000/docs

`/health` endpoint'i veritabanına erişebildiğinde `200` döner, erişemediğinde `503` döner.
