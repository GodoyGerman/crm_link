from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.categoria import Categoria
from schemas.categoria import CategoriaCreate, CategoriaSchema
from typing import List

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.post("/", response_model=CategoriaSchema)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = Categoria(nombre=categoria.nombre)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.get("/", response_model=List[CategoriaSchema])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()
