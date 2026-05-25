# Documentacao auxiliar

## Postman

Arquivo: [`service_order_api.postman_collection.json`](service_order_api.postman_collection.json)

### Importar

1. Abra o [Postman](https://www.postman.com/downloads/) ou [Insomnia](https://insomnia.rest/) (importe JSON compativel com Postman v2.1).
2. **Import** → selecione o arquivo da colecao.
3. Na colecao, edite a variavel `baseUrl` se for testar localmente:
   - Producao: `https://serviceorder-production.up.railway.app`
   - Local: `http://127.0.0.1:8000`
4. Execute **Auth > Login** — o token e salvo em `accessToken` automaticamente.
5. Use as outras requisicoes (Bearer ja configurado na colecao).

### Variaveis uteis

| Variavel | Uso |
|----------|-----|
| `baseUrl` | URL da API |
| `accessToken` | Preenchido apos login |
| `serviceOrderId`, `clientId`, `userId`, `attachmentId` | IDs para rotas com path |

### Alternativa: OpenAPI

O FastAPI expoe o schema em `/openapi.json`. No Postman: **Import** → **Link** → `{{baseUrl}}/openapi.json`.
