from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, ConfigDict

from models import Coche
from dependencies import get_db

app = FastAPI()


class CocheCreate(BaseModel):
    cliente_id: int
    marca: str
    modelo: str | None = None
    matricula: str


class CocheResponse(CocheCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


@app.post("/coches/", response_model=CocheResponse)
async def create_coche(coche: CocheCreate, db: AsyncSession = Depends(get_db)):
    db_coche = Coche(**coche.model_dump())

    db.add(db_coche)
    await db.commit()
    await db.refresh(db_coche)

    return db_coche


@app.get("/coches/{coche_id}", response_model=CocheResponse)
async def read_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = result.scalar_one_or_none()

    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    return coche


@app.get("/coches/", response_model=list[CocheResponse])
async def list_coches(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche))
    return result.scalars().all()


@app.put("/coches/{coche_id}", response_model=CocheResponse)
async def update_coche(
    coche_id: int,
    coche: CocheCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    db_coche = result.scalar_one_or_none()

    if not db_coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    for key, value in coche.model_dump().items():
        setattr(db_coche, key, value)

    await db.commit()
    await db.refresh(db_coche)

    return db_coche


@app.delete("/coches/{coche_id}")
async def delete_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = result.scalar_one_or_none()

    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    await db.delete(coche)
    await db.commit()

    return {"mensaje": "Coche eliminado"}

"""
#Practica 1 - Adapatada a coches
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos
class Coche(BaseModel):
    cliente_id: int
    marca: str
    modelo: str
    matricula: int

#GET
@app.get("/coches")
def get_coches():
    return {"mensaje": "Lista de coches",
            "coches": [
                            {"cliente_id": 1, "marca": "Toyota", "modelo": "Corolla", "matricula": 1234},
                            {"cliente_id": 2, "marca": "Honda", "modelo": "Civic", "matricula": 5678}
                        ]
            }

#POST
@app.post("/coches")
def create_coches(coche: Coche):
    return {"mensaje": "Coche creado exitosamente", 
            "coche": coche
            }

#PUT
@app.put("/coches/{coche_id}")
def update_coches(coche_id: int, coche: Coche):
    return {"mensaje": "Coche actualizado exitosamente", 
            "coche": coche
            }

#DELETE
@app.delete("/coches/{coche_id}")
def delete_coches(coche_id: int):
    return {"mensaje": f"Coche {coche_id} eliminado"}
"""




""""
#Practica 1
# Modelo de datos
class Usuario(BaseModel):
    nombre: str
    apellidos: str
    #fecha_nacimiento: str
    correo_electronico: str
    edad: int
    es_profesor: bool

#GET
@app.get("/usuarios")
def get_usuarios():
    return {"mensaje": "Lista de usuarios",
            "usuarios": [
                            {"nombre": "Juan", "apellidos": "Pérez", "correo_electronico": "juan.perez@example.com", "edad": 30, "es_profesor": False},
                            {"nombre": "María", "apellidos": "Gómez", "correo_electronico": "maria.gomez@example.com", "edad": 25, "es_profesor": True}
                        ]
            }

#POST
@app.post("/usuarios")
def create_usuario(usuario: Usuario):
    return {"mensaje": "Usuario creado exitosamente", 
            "usuario": usuario
            }

#PUT
@app.put("/usuarios/{usuario_id}")
def update_usuario(usuario_id: int, usuario: Usuario):
    return {"mensaje": "Usuario actualizado exitosamente", 
            "usuario": usuario
            }

#DELETE
@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int):
    return {"mensaje": f"Usuario {usuario_id} eliminado"}
"""