from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from pydantic import BaseModel

# URL de la base de datos
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/test1"

# Configuración de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Definición del modelo (tabla) 'items'
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


# Crear la tabla en la base de datos (esto es opcional si ya la tienes creada)
Base.metadata.create_all(bind=engine)


# Modelo de Pydantic para la respuesta
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True


# Crear la instancia de FastAPI
app = FastAPI()


# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Evento de inicio para conectar a la base de datos
@app.on_event("startup")
async def startup():
    pass  # No es necesario conectar explícitamente usando databases en este caso


# Evento de apagado para desconectar la base de datos
@app.on_event("shutdown")
async def shutdown():
    pass  # No es necesario desconectar explícitamente en este caso


# Ruta para obtener los elementos de la tabla 'items'
@app.get("/items/", response_model=List[ItemResponse])
async def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items
