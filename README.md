# Service Order API

API para gerenciamento de ordens de servico, desenvolvida com FastAPI,
SQLAlchemy, Alembic e SQLite.

## Funcionalidades atuais

- Cadastro de usuarios
- Login com JWT
- Rota autenticada para usuario atual
- Cadastro de clientes
- Listagem de clientes protegida por autenticacao
- Cadastro de ordens de servico
- Listagem e consulta de ordens de servico
- Atualizacao de status de ordens de servico
- Historico de alteracoes de status
- Migrations com Alembic

## Stack

- Python
- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Pydantic
- JWT com python-jose
- Passlib e bcrypt para hash de senha

## Configuracao do ambiente

Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

Crie o arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

Depois, ajuste a variavel `SECRET_KEY` no `.env`.

## Banco de dados

O projeto usa SQLite em desenvolvimento:

```env
DATABASE_URL=sqlite:///./service_order.db
```

Para criar ou atualizar o banco com as migrations:

```powershell
.\.venv\Scripts\alembic.exe upgrade head
```

O arquivo `service_order.db` e gerado localmente e nao deve ser versionado.

## Executando a API

Inicie o servidor local:

```powershell
uvicorn app.main:app --reload
```

Acesse a documentacao interativa:

```text
http://127.0.0.1:8000/docs
```

## Endpoints atuais

### Health check

```http
GET /
```

### Usuarios

```http
POST /users/
GET /users/
```

### Autenticacao

```http
POST /auth/login
GET /auth/me
```

O login retorna um token JWT. No Swagger, use o botao `Authorize`,
preenchendo:

```text
username = email do usuario
password = senha do usuario
```

### Clientes

```http
POST /clients/
GET /clients/
```

As rotas de clientes exigem token JWT.

### Ordens de servico

```http
POST /service-orders/
GET /service-orders/
GET /service-orders/{service_order_id}
PATCH /service-orders/{service_order_id}/status
GET /service-orders/{service_order_id}/history
```

As rotas de ordens de servico exigem token JWT.

Status aceitos:

```text
open
in_progress
waiting
done
canceled
```

Prioridades aceitas:

```text
low
medium
high
urgent
```

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

## Fluxo basico para testar

1. Crie um usuario em `POST /users/`.
2. Faca login em `POST /auth/login`.
3. Autorize no Swagger com o token.
4. Teste `GET /auth/me`.
5. Crie um cliente em `POST /clients/`.
6. Liste clientes em `GET /clients/`.
7. Crie uma ordem em `POST /service-orders/`.
8. Altere o status em `PATCH /service-orders/{service_order_id}/status`.
9. Consulte o historico em `GET /service-orders/{service_order_id}/history`.

## Estrutura principal

```text
app/
  api/
    deps.py
    routes/
      auth.py
      clients.py
      service_orders.py
      users.py
  core/
    config.py
    database.py
    security.py
  models/
    client.py
    service_order.py
    service_order_history.py
    user.py
  repositories/
    client_repository.py
    service_order_repository.py
    service_order_history_repository.py
    user_repository.py
  schemas/
    auth.py
    client.py
    service_order.py
    service_order_history.py
    user.py
  services/
    auth_service.py
    client_service.py
    service_order_service.py
    user_service.py
  utils/
    enums.py
```

## Proximos passos

- Adicionar filtros para ordens de servico
- Criar regras de transicao de status
- Adicionar testes automatizados
