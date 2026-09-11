# EcoBuild-AI

## Requisitos

- Python 3.12
- `uv` instalado
- PostgreSQL 14+ (local ou gerenciado)
- chave da Google AI / Gemini configurada em `GOOGLE_API_KEY`

## Configuração local

Copie o exemplo de variáveis de ambiente:

```bash
cp .env.example .env
```

Edite o `.env` com os valores do seu ambiente local. O arquivo `.env` não deve ser enviado ao Git.

Exemplo:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ecobuild
GOOGLE_API_KEY=your_google_ai_api_key_here
API_BASE_URL=http://127.0.0.1:8000
PORT=8000
UPLOAD_DIR=api/uploads
CORS_ALLOWED_ORIGINS=*
```

## Dependências com `uv`

```bash
uv sync --frozen
```

## Migrations

Antes de iniciar a API, aplique as migrations do Alembic:

```bash
uv run alembic upgrade head
```

## Executando a API localmente

```bash
uv run uvicorn api.main:app --reload
```

Ou diretamente:

```bash
uv run uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

## Preparando PostgreSQL para produção

Use um PostgreSQL gerenciado (ex.: Render Postgres) e defina `DATABASE_URL` com a URL completa do banco.

Exemplo conceptual:

```env
DATABASE_URL=postgresql://user:password@host:5432/ecobuild
```

A aplicação usa SQLAlchemy + asyncpg, logo o driver compatível é o `postgresql+asyncpg://...` quando necessário. O projeto converte automaticamente URLs `postgresql://` para o driver correto.

## Deployment

### Render

Sem Docker. O projeto foi preparado para deploy direto com Python e `uv`.

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

Você também pode usar um `render.yaml` simples para declarar o serviço como código.

## Health check

A aplicação expõe:

```http
GET /health
```

Resposta esperada:

```json
{ "status": "healthy" }
```

## Uploads temporários e filesystem

Os uploads são armazenados em `api/uploads` por padrão para o MVP. Esse diretório é adequado para processamento temporário, mas não deve ser tratado como armazenamento permanente.

Em serviços gratuitos, o filesystem pode ser efêmero; por isso, o fluxo ideal é:

1. receber upload
2. processar
3. persistir os dados relevantes no PostgreSQL
4. remover arquivos temporários quando não forem mais necessários

A abstração do storage foi mantida para permitir uma troca futura por object storage (ex.: S3/MinIO) sem quebrar a Clean Architecture.

## Limitações do filesystem gratuito

- o arquivo local pode desaparecer entre reinicializações;
- não usar o storage local como fonte de verdade para dados permanentes;
- manter o banco PostgreSQL como armazenamento principal dos dados estruturados.

## Observações finais

- o projeto não usa Docker;
- as migrações devem ser executadas explicitamente antes do deploy ou em um pre-deploy command apropriado;
- não versionar secrets nem arquivos `.env` reais.
