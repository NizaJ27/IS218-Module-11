# Reflection

This short reflection documents the experience implementing a secure user model and CI pipeline.

- Implemented SQLAlchemy `User` model with unique constraints and `created_at` timestamp.
- Added Pydantic schemas `UserCreate` and `UserRead` to validate input and hide password details.
- Used `passlib` (bcrypt) to hash passwords and verify them.
- Wrote unit tests for hashing and schema validation and integration tests that exercise the `/users` endpoint.
- Added a GitHub Actions workflow that runs tests against Postgres and pushes a Docker image to Docker Hub (requires repository secrets to be configured).

Challenges and notes:

- Ensuring tests run in both local and CI contexts required defaulting to SQLite when `DATABASE_URL` is not provided.
- GitHub Actions requires `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets for pushing images; configure those before relying on the deploy step.
- The integration tests assume the application creates tables at startup via `app.db.init_db()`; for production use, migration tooling (Alembic) is recommended.

Next steps (not performed here):

- Add authentication endpoints (login) and token-based auth.
- Add migrations and seed data for environments.

