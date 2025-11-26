from fastapi import FastAPI

from app.auth.routes import router as auth_router
from app.pedidos.routes import router as pedidos_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(pedidos_router)