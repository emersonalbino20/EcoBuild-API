# EcoBuild-AI

API assíncrona para gerenciamento de usuários, organizações, planos e análises de projetos de construção.

## Pré-requisitos

- Python 3.12 ou superior
- PostgreSQL em execução
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Configuração

Na raiz do projeto, crie o arquivo `.env` a partir do exemplo:

```bash
cp .env-example .env
```

Edite `DATABASE_URL` com os dados do seu PostgreSQL. O banco informado na URL precisa existir antes de executar as migrações, por exemplo:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ecobuild
```

Instale as dependências:

```bash
uv sync
```

## Banco de dados

Execute as migrações a partir do diretório `api`:

```bash
cd api
uv run alembic upgrade head
cd ..
```

## Subir a API

Ainda na raiz do projeto, execute:

```bash
cd api
uv run uvicorn main:app --reload
```

A API ficará disponível em `http://localhost:8000`.

Documentação interativa:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testar

Não há uma suíte de testes automatizados no repositório. Para validar se a aplicação subiu corretamente, em outro terminal execute:

```bash
curl -i http://localhost:8000/
```

A resposta esperada é `200 OK` com o conteúdo:

```json
{"status":"ok"}
```

Também é possível verificar o contrato da API em `http://localhost:8000/docs` ou executar chamadas diretamente pelo terminal. Por exemplo, para criar um usuário:

```bash
curl -X POST http://localhost:8000/users/ \
	-H "Content-Type: application/json" \
	-d '{"name":"John Doe","email":"john@example.com","password_hash":"Password123"}'
```

Os planos são criados por upload de arquivos `.pdf`, `.txt` ou `.json`:

```bash
curl -X POST http://localhost:8000/plans/1 \
	-F "file=@/caminho/para/plano.pdf"
```

Para encerrar o servidor em desenvolvimento, pressione `Ctrl+C` no terminal em que o Uvicorn está rodando.
