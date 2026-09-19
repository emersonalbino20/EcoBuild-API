# EcoBuild-AI

## Requirements

- Python 3.12
- `uv` installed
- PostgreSQL 14+ (local or managed)
- Google AI / Gemini key configured in `GOOGLE_API_KEY`

## Local setup

Copy the environment variable template:

```bash
cp .env.example .env
```

Edit `.env` with the values for your local environment. Do not commit `.env` to Git.

Exemplo:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ecobuild
GOOGLE_API_KEY=your_google_ai_api_key_here
API_BASE_URL=http://127.0.0.1:8000
PORT=8000
UPLOAD_DIR=api/uploads
CORS_ALLOWED_ORIGINS=*
```

## Dependencies with `uv`

```bash
uv sync --frozen
```

## Migrations

Before starting the API, apply the Alembic migrations:

```bash
uv run alembic upgrade head
```

## Running the API locally

```bash
uv run uvicorn api.main:app --reload
```

Ou diretamente:

```bash
uv run uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

## Preparing PostgreSQL for production

Use a managed PostgreSQL instance (for example, Render Postgres) and set `DATABASE_URL` to the complete database URL.

Exemplo conceptual:

```env
DATABASE_URL=postgresql://user:password@host:5432/ecobuild
```

The application uses SQLAlchemy and asyncpg, so the compatible driver is `postgresql+asyncpg://...` when required. The project automatically converts `postgresql://` URLs to the correct driver.

## Deployment

### Render

No Docker is required. The project is prepared for direct deployment with Python and `uv`.

Build command:

```bash
uv sync --frozen
```

Start command:

```bash
uv run uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

Health check:

```text
/health
```

Configure no Render, em Environment Variables, apenas:

- `DATABASE_URL`
- `GOOGLE_API_KEY`
- `API_BASE_URL`
- `PORT`
- `UPLOAD_DIR`
- `CORS_ALLOWED_ORIGINS`

You can also use a simple `render.yaml` file to declare the service as code.

## Health check

The application exposes:

```http
GET /health
```

Resposta esperada:

```json
{ "status": "healthy" }
```

## Temporary uploads and filesystem

Uploads are stored in `api/uploads` by default for the MVP. This directory is suitable for temporary processing and must not be treated as permanent storage.

On free services, the filesystem may be ephemeral. The recommended flow is:

1. receber upload
2. processar
3. persistir os dados relevantes no PostgreSQL
4. remove temporary files when they are no longer needed

The storage abstraction is maintained so it can later be replaced with object storage (for example, S3 or MinIO) without breaking the Clean Architecture.

## Free filesystem limitations

- local files may disappear between restarts;
- do not use local storage as the source of truth for permanent data;
- keep PostgreSQL as the primary store for structured data.

## Final notes

- the project does not use Docker;
- migrations must be run explicitly before deployment or through an appropriate pre-deploy command;
- do not commit secrets or real `.env` files.
