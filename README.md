# Service Order API

![CI](https://github.com/iuryruansc/service_order/actions/workflows/ci.yml/badge.svg)

API REST para gerenciamento de ordens de servico, com autenticacao JWT, regras de negocio, historico de alteracoes e deploy em producao.

## Demo

Documentacao interativa (Swagger UI) em producao:

**https://serviceorder-production.up.railway.app/docs**

Health check: [https://serviceorder-production.up.railway.app/](https://serviceorder-production.up.railway.app/)

No Swagger, use **Authorize** com `username` = e-mail do usuario e `password` = senha.

**Postman / Insomnia:** importe a colecao em [`docs/service_order_api.postman_collection.json`](docs/service_order_api.postman_collection.json) (veja [`docs/README.md`](docs/README.md)).

## Funcionalidades

- Cadastro e listagem de usuarios (ativar/desativar)
- Login com JWT e rota do usuario autenticado (`/auth/me`)
- Papeis de usuario (admin e operador)
- CRUD de clientes (rotas protegidas)
- Ordens de servico: criacao, consulta, listagem com filtros e paginacao
- Atualizacao de status com regras de negocio e historico
- Dashboard com metricas agregadas
- Anexos por ordem de servico (upload, listagem, exclusao)
- Exportacao de ordens em PDF e Excel (admin)
- Notificacoes por e-mail em eventos da ordem (quando configurado)
- Migrations com Alembic
- Testes automatizados com pytest
- Container Docker e PostgreSQL

## Stack

- Python 3.14
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (Docker e producao)
- Pydantic / pydantic-settings
- JWT (`python-jose`)
- Passlib + bcrypt
- pytest + httpx
- Docker / Docker Compose
- Deploy: [Railway](https://railway.app)

## Como executar

### Opcao 1 — Docker (recomendado)

Requisitos: Docker e Docker Compose.

```powershell
Copy-Item .env.example .env
docker compose up --build
```

A API fica em `http://127.0.0.1:8000` e o Swagger em `http://127.0.0.1:8000/docs`.

O `entrypoint.sh` aguarda o Postgres, roda `alembic upgrade head` e inicia o Uvicorn.

### Opcao 2 — Local (venv)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Ajuste o `.env` (principalmente `SECRET_KEY` e `DATABASE_URL`).

Com PostgreSQL local ou via compose apenas do banco:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/service_order
```

Aplique as migrations e inicie a API:

```powershell
alembic upgrade head
uvicorn app.main:app --reload
```

Swagger local: `http://127.0.0.1:8000/docs`

### Dados de exemplo (seed)

Com o banco configurado e migrations aplicadas:

```powershell
python seed.py
```

O script cria usuario admin, tres clientes e ordens de servico com historico de status. Detalhes e uso em producao na secao [Deploy (Railway)](#deploy-railway).

## Variaveis de ambiente

Copie `.env.example` para `.env`:

| Variavel                      | Descricao                                         |
| ----------------------------- | ------------------------------------------------- |
| `APP_NAME`                    | Nome exibido da aplicacao                         |
| `ENVIRONMENT`                 | `development` ou `production`                     |
| `DATABASE_URL`                | URL do PostgreSQL                                 |
| `SECRET_KEY`                  | Chave para assinatura do JWT (troque em producao) |
| `ALGORITHM`                   | Algoritmo JWT (ex.: `HS256`)                      |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do token                                 |
| `MAIL_*`                      | SMTP para envio de e-mails (opcional)             |
| `MAIL_SUPPRESS_SEND`          | `true` em testes/CI para nao conectar ao SMTP     |

Em producao no Railway, configure essas variaveis no painel do servico (nunca commite o `.env`).

## Banco de dados

- **Desenvolvimento / Docker:** PostgreSQL via `docker-compose.yml`
- **Producao:** PostgreSQL gerenciado no Railway
- **Testes:** SQLite em memoria/arquivo isolado (`tests/conftest.py`)

Migrations:

```powershell
alembic upgrade head
```

## Testes

```powershell
pytest
```

A suite cobre autenticacao, clientes, ordens, status, dashboard, anexos e exportacao.

Os testes usam SQLite isolado (`tests/conftest.py`) e definem `MAIL_SUPPRESS_SEND=true` para nao enviar e-mail real.

**CI:** cada push/PR em `main` executa `pytest` via [GitHub Actions](.github/workflows/ci.yml).

## Deploy (Railway)

A API esta publicada no Railway:

| Recurso | URL                                                 |
| ------- | --------------------------------------------------- |
| Base    | https://serviceorder-production.up.railway.app      |
| Swagger | https://serviceorder-production.up.railway.app/docs |
| Health  | https://serviceorder-production.up.railway.app/     |

### Como a aplicacao sobe em producao

```mermaid
flowchart LR
  subgraph railway [Railway]
    IMG[Imagem Docker]
    EP[entrypoint.sh]
    MIG[alembic upgrade head]
    API[uvicorn :8000]
    DB[(PostgreSQL)]
  end
  IMG --> EP
  EP -->|aguarda conexao| DB
  EP --> MIG
  MIG --> DB
  EP --> API
  API --> DB
```

1. Railway builda a imagem a partir do `Dockerfile` (Python 3.14).
2. O `entrypoint.sh` aguarda o PostgreSQL ficar disponivel.
3. Roda `alembic upgrade head` (schema sempre atualizado no deploy).
4. Inicia o Uvicorn na porta `8000`.

### Variaveis no painel Railway

Configure em **Variables** do servico (nunca no Git):

| Variavel                      | Obrigatoria | Observacao                              |
| ----------------------------- | ----------- | --------------------------------------- |
| `DATABASE_URL`                | Sim         | URL do addon **PostgreSQL** do Railway  |
| `SECRET_KEY`                  | Sim         | String longa e aleatoria (producao)     |
| `ENVIRONMENT`                 | Sim         | Use `production`                        |
| `ALGORITHM`                   | Nao         | Padrao `HS256`                          |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Nao         | Ex.: `30`                               |
| `MAIL_*`                      | Nao         | SMTP; necessario para e-mails em ordens |
| `MAIL_SUPPRESS_SEND`          | Nao         | `false` em producao se usar e-mail      |

O addon PostgreSQL do Railway injeta `DATABASE_URL` automaticamente quando o servico do banco esta ligado ao app.

### Popular dados de demonstracao em producao

O `seed.py` e **idempotente** (nao duplica se ja existir). Cria admin, clientes e ordens de exemplo.

**Local ou Docker** (com banco acessivel):

```powershell
alembic upgrade head
python seed.py
```

**No Railway** (com [Railway CLI](https://docs.railway.app/develop/cli) instalada e projeto linkado):

```powershell
railway run python seed.py
```

Credenciais criadas pelo seed — **apenas para demo/teste**:

| Papel | E-mail              | Senha    |
| ----- | ------------------- | -------- |
| Admin | `admin@example.com` | `123456` |

Clientes de exemplo: `client1@example.com`, `client2@example.com`, `client3@example.com`.

> Em producao publica, troque senhas ou use apenas `POST /users/` para criar contas de teste temporarias.

### Verificacao pos-deploy

| Passo          | Como validar                                                   |
| -------------- | -------------------------------------------------------------- |
| Health         | `GET /` retorna `status: Service is running`                   |
| Swagger        | Abrir `/docs`                                                  |
| Auth           | `POST /auth/login` (form: `username`=e-mail, `password`=senha) |
| Rota protegida | `GET /auth/me` com header `Authorization: Bearer <token>`      |
| Persistencia   | Redeploy no Railway; dados no Postgres devem permanecer        |

### Decisoes tecnicas

- **Camadas separadas** (`routes` → `services` → `repositories`): facilita testes, regras de negocio e manutencao.
- **JWT** para rotas protegidas; senhas com bcrypt via Passlib.
- **PostgreSQL** em Docker e producao; SQLite apenas na suite de testes.
- **Alembic** versiona o schema; no container, migrations rodam no `entrypoint.sh` antes do servidor subir.
- **Docker** garante o mesmo ambiente local e no Railway.

## Endpoints principais

### Health check

```http
GET /
```

### Autenticacao

```http
POST /auth/login
GET /auth/me
```

### Usuarios

```http
POST /users/
GET /users/
PATCH /users/{user_id}/activate
PATCH /users/{user_id}/deactivate
```

### Clientes

```http
POST /clients/
GET /clients/
```

### Ordens de servico

```http
POST /service-orders/
GET /service-orders/
GET /service-orders/export?format=excel|pdf
GET /service-orders/{service_order_id}
PATCH /service-orders/{service_order_id}/status
GET /service-orders/{service_order_id}/history
POST /service-orders/{service_order_id}/attachments
GET /service-orders/{service_order_id}/attachments
DELETE /service-orders/{service_order_id}/attachments/{attachment_id}
```

Listagem com filtros opcionais: `status`, `priority`, `client_id`, `responsible_user_id`, `skip`, `limit`.

**Status:** `open`, `in_progress`, `waiting`, `done`, `canceled`

**Prioridades:** `low`, `medium`, `high`, `urgent`

### Dashboard

```http
GET /dashboard/
```

Rotas de clientes, ordens, dashboard, anexos e export exigem JWT. Export exige usuario **admin**.

## Fluxo rapido de teste

1. Acesse a [demo no Swagger](https://serviceorder-production.up.railway.app/docs) ou rode localmente.
2. Crie um usuario em `POST /users/` ou use o seed (`admin@example.com` / `123456`).
3. Faca login em `POST /auth/login`.
4. Clique em **Authorize** e informe e-mail e senha.
5. Crie um cliente em `POST /clients/`.
6. Crie uma ordem em `POST /service-orders/`.
7. Atualize o status em `PATCH /service-orders/{id}/status`.
8. Consulte o historico em `GET /service-orders/{id}/history`.

Exemplo de criacao de ordem:

```json
{
  "title": "Troca de tela",
  "description": "Cliente solicitou troca de tela do notebook",
  "priority": "high",
  "client_id": 1,
  "responsible_user_id": 1
}
```

Exemplo de alteracao de status:

```json
{
  "status": "in_progress",
  "note": "Atendimento iniciado"
}
```

## Arquitetura

### Camadas da aplicacao

```mermaid
flowchart LR
  Client[Cliente HTTP] --> API[FastAPI routes]
  API --> SVC[Services]
  SVC --> REPO[Repositories]
  REPO --> DB[(PostgreSQL)]
```

- **routes:** entrada HTTP, validacao e status codes
- **services:** regras de negocio (status, permissoes, e-mail)
- **repositories:** consultas e persistencia SQLAlchemy
- **models / schemas:** tabelas e contratos JSON

### Estrutura de pastas

```text
app/
  api/
    deps.py
    routes/
      auth.py
      users.py
      clients.py
      service_orders.py
      dashboard.py
      attachment.py
  core/
    config.py
    database.py
    security.py
    mail.py
  models/
  schemas/
  repositories/
  services/
  utils/
tests/
alembic/
```
