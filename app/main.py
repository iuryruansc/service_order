from fastapi import FastAPI

from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router

app = FastAPI(title="Service Order API")

@app.get("/")
def health_check():
    return {"status": "Service is running", "message": "Welcome to the Service Order API!"}

app.include_router(users_router)
app.include_router(auth_router)