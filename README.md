# Service Order API

API para gerenciamento de ordens de servico, desenvolvida com FastAPI,
SQLAlchemy, Alembic e SQLite.

## Funcionalidades atuais

- Cadastro de usuarios
- Login com JWT
- Rota autenticada para usuario atual
- Cadastro de clientes
- Listagem de clientes protegida por autenticacao
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

## Fluxo basico para testar

1. Crie um usuario em `POST /users/`.
2. Faca login em `POST /auth/login`.
3. Autorize no Swagger com o token.
4. Teste `GET /auth/me`.
5. Crie um cliente em `POST /clients/`.
6. Liste clientes em `GET /clients/`.

## Estrutura principal

```text
app/
  api/
    deps.py
    routes/
      auth.py
      clients.py
      users.py
  core/
    config.py
    database.py
    security.py
  models/
    client.py
    user.py
  repositories/
    client_repository.py
    user_repository.py
  schemas/
    auth.py
    client.py
    user.py
  services/
    auth_service.py
    client_service.py
    user_service.py
```

## Proximos passos

- Criar o fluxo de ordens de servico
- Adicionar status e prioridade para ordens
- Criar historico de alteracoes
- Adicionar testes automatizados
