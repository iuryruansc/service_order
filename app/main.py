from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.users import router as users_router
from app.api.routes.clients import router as clients_router
from app.api.routes.auth import router as auth_router
from app.api.routes.service_orders import router as service_orders_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.attachment import router as attachments_router

app = FastAPI(title="Service Order API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        # "https://seu-app.vercel.app",  # URL do front após deploy
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Service is running", "message": "Welcome to the Service Order API!"}

app.include_router(users_router)
app.include_router(clients_router)
app.include_router(service_orders_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(attachments_router)