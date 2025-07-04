from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import clientes
from routers import servicio
from routers import categoria  # importa tu router
from database import Base, engine
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)


# Habilitar CORS
origins = [
    "http://localhost:8080",  # donde está el frontend
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # puedes usar ["*"] en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router de clientes
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(servicio.router, prefix="/servicios", tags=["Servicios"])
app.include_router(categoria.router, prefix="/categoria", tags=["categoria"])


Base.metadata.create_all(bind=engine)

