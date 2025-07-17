from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import clientes
from routers import servicio
from routers import categoria  # importa tu router
from routers import cotizacion
from database import Base, engine
from routers import auth  # importa tu router
from routers import auth, servicio, cotizacion, clientes, categoria, usuarios

import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)


# Habilitar CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5175",         # <--- AGREGA ESTO
    "http://127.0.0.1:5175",         # <--- Y ESTO TAMBIÉN
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
app.include_router(cotizacion.router, prefix="/cotizacion", tags=["cotizacion"])
app.include_router(auth.router)
app.include_router(usuarios.router)

Base.metadata.create_all(bind=engine)

