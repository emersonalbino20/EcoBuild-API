#!/usr/bin/env bash

# set -Eeuo pipefail

# ============================================================
# EcoBuild-API - Development Environment Setup
# ============================================================

PROJECT_NAME="EcoBuild-API"

# PostgreSQL
DB_NAME="ecobuild"
DB_USER="postgres"
DB_PASSWORD="1234"
DB_HOST="localhost"
DB_PORT="5432"

VENV_DIR=".venv"


# ============================================================
# Helpers
# ============================================================

error() {
    echo
    echo "❌ ERROR: $1"
    echo
    exit 1
}

info() {
    echo "→ $1"
}

success() {
    echo "✓ $1"
}

trap 'echo; echo "❌ O setup falhou na linha $LINENO."; echo "   Comando: $BASH_COMMAND"; exit 1' ERR


# ============================================================
# Header
# ============================================================

echo
echo "=============================================="
echo "        $PROJECT_NAME - Setup"
echo "=============================================="
echo


# ============================================================
# 1. Check Python
# ============================================================

info "Verificando Python..."

if ! command -v python3 >/dev/null 2>&1; then
    error "Python3 não está instalado. pesquise na internet como instalar"
fi

PYTHON_VERSION=$(python3 -c \
    'import sys; print(".".join(map(str, sys.version_info[:3])))')

if ! python3 -c \
    'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'
then
    error "Python 3.10 ou superior é necessário.
Versão encontrada: $PYTHON_VERSION"
fi

success "Python $PYTHON_VERSION"


# ============================================================
# 2. Check uv
# ============================================================

info "Verificando uv..."

if ! command -v uv >/dev/null 2>&1; then
    error "uv não está instalado.

    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Carregar o uv para a sessão actual
    export PATH="$HOME/.local/bin:$PATH"

    if ! command -v uv >/dev/null 2>&1; then
        error "Não foi possível instalar o uv, pesquise na internet como instalar"
    fi
fi

UV_VERSION=$(uv --version)

success "$UV_VERSION"


# ============================================================
# 3. Create virtual environment
# ============================================================

info "Verificando ambiente virtual..."

if [[ -d "$VENV_DIR" ]]; then

    success "Ambiente virtual '$VENV_DIR' já existe."

else

    info "Criando ambiente virtual com uv..."

    if ! uv venv "$VENV_DIR"; then
        error "Não foi possível criar o ambiente virtual."
    fi

    success "Ambiente virtual criado."

fi


# ============================================================
# 4. Activate virtual environment
# ============================================================

info "Activando ambiente virtual..."

if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
    error "O ambiente virtual não possui o script de activação."
fi

source "$VENV_DIR/bin/activate"

success "Ambiente virtual activado."


# ============================================================
# 5. Verify Python inside virtual environment
# ============================================================

info "Verificando Python do ambiente virtual..."

VENV_PYTHON_VERSION=$(python -c \
    'import sys; print(".".join(map(str, sys.version_info[:3])))')

if ! python -c \
    'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)'
then
    error "O Python do ambiente virtual deve ser >= 3.12.
Versão encontrada: $VENV_PYTHON_VERSION"
fi

success "Python virtual: $VENV_PYTHON_VERSION"


# ============================================================
# 6. Check PostgreSQL
# ============================================================

info "Verificando PostgreSQL..."

if ! command -v psql >/dev/null 2>&1; then
    error "PostgreSQL/psql não está instalado."
fi

if ! command -v pg_isready >/dev/null 2>&1; then
    error "pg_isready não está disponível."
fi

success "PostgreSQL instalado."


# ============================================================
# 7. Check PostgreSQL server
# ============================================================

info "Verificando servidor PostgreSQL..."

if ! pg_isready \
    -h "$DB_HOST" \
    -p "$DB_PORT" >/dev/null 2>&1
then
    error "O PostgreSQL não está em execução em:

    $DB_HOST:$DB_PORT

Inicie o serviço PostgreSQL e execute o setup novamente."
fi

success "Servidor PostgreSQL disponível."


# ============================================================
# 8. Check PostgreSQL credentials
# ============================================================

info "Verificando credenciais PostgreSQL..."

if ! PGPASSWORD="$DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d postgres \
    -c "SELECT 1;" >/dev/null 2>&1
then
    error "Não foi possível autenticar no PostgreSQL.

Configuração esperada:

    User:     $DB_USER
    Password: $DB_PASSWORD
    Host:     $DB_HOST
    Port:     $DB_PORT"
fi

success "Credenciais PostgreSQL válidas."


# ============================================================
# 9. Create database
# ============================================================

info "Verificando database '$DB_NAME'..."

DB_EXISTS=$(PGPASSWORD="$DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d postgres \
    -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME';")

if [[ "$DB_EXISTS" == "1" ]]; then

    success "Database '$DB_NAME' já existe."

else

    info "Criando database '$DB_NAME'..."

    if ! PGPASSWORD="$DB_PASSWORD" createdb \
        -h "$DB_HOST" \
        -p "$DB_PORT" \
        -U "$DB_USER" \
        "$DB_NAME"
    then
        error "Não foi possível criar a database '$DB_NAME'."
    fi

    success "Database '$DB_NAME' criada."

fi


# ============================================================
# 10. Configure .env
# ============================================================

info "Verificando arquivo .env..."

if [[ -f ".env" ]]; then

    success ".env já existe."

else

    echo
    echo "A GOOGLE_API_KEY é necessária para os agentes de IA."
    echo

    read -rsp "Digite a GOOGLE_API_KEY: " GOOGLE_API_KEY
    echo

    if [[ -z "$GOOGLE_API_KEY" ]]; then
        error "GOOGLE_API_KEY não pode estar vazia."
    fi

    cat > .env <<EOF
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
GOOGLE_API_KEY=${GOOGLE_API_KEY}
EOF

    chmod 600 .env

    success ".env criado."

fi


# ============================================================
# 11. Validate .env
# ============================================================

info "Validando configuração do .env..."

if ! grep -q "^DATABASE_URL=" .env; then
    error "DATABASE_URL não encontrada no .env."
fi

if ! grep -q "^GOOGLE_API_KEY=" .env; then
    error "GOOGLE_API_KEY não encontrada no .env."
fi

success ".env válido."


# ============================================================
# 12. Install dependencies
# ============================================================

info "Instalando dependências..."

if ! uv sync; then
    error "Falha ao instalar as dependências com uv."
fi

success "Dependências instaladas."


# ============================================================
# 14. Final information
# ============================================================
echo "Entrando no directório api/"
cd api/;
echo "Rodando as Migrations"
alembic upgrade head
echo
echo "=============================================="
echo "       Setup concluído com sucesso!"
echo "=============================================="
echo
echo "Virtual environment:"
echo "  $VENV_DIR"
echo
echo "PostgreSQL:"
echo "  Host:     $DB_HOST"
echo "  Port:     $DB_PORT"
echo "  Database: $DB_NAME"
echo "  User:     $DB_USER"
echo "  Password: $DB_PASSWORD"
echo
echo "Python:"
echo "  $VENV_PYTHON_VERSION"
echo
echo "Subindo a API:"
echo "python3 api/main.py"
python3 main.py
echo
echo "=============================================="
echo "API NO NAVEGADOR: http://0.0.0.0:8000/docs"
echo


# ============================================================
# 15. Start API
# ============================================================

#exec uv run uvicorn api.main:app --reload


