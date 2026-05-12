# Debajo de todo esta comentada la versión de la práctica 2, antes de aplicar las realaciones.


# Versión de la praáctica 3 (EXTRA) con relaciones entre tablas y manejo de errores.
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from dependencies import get_db
from models import Coche, Color, Marca

app = FastAPI()


class MarcaBase(BaseModel):
    nombre: str


class MarcaCreate(MarcaBase):
    pass


class MarcaResponse(MarcaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ColorBase(BaseModel):
    nombre: str


class ColorCreate(ColorBase):
    pass


class ColorResponse(ColorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CocheBase(BaseModel):
    cliente_id: int
    modelo: str | None = None
    matricula: str


class CocheCreate(CocheBase):
    pass


class CocheUpdate(CocheBase):
    marca_id: int


class CocheResponse(CocheBase):
    id: int
    marca: MarcaResponse
    colores: list[ColorResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


@app.post("/marcas/", response_model=MarcaResponse)
async def create_marca(marca: MarcaCreate, db: AsyncSession = Depends(get_db)):
    db_marca = Marca(**marca.model_dump())

    db.add(db_marca)
    await db.commit()
    await db.refresh(db_marca)

    return db_marca


@app.get("/marcas/", response_model=list[MarcaResponse])
async def list_marcas(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Marca))
    return result.scalars().all()


@app.post("/marcas/{marca_id}/coches/", response_model=CocheResponse)
async def create_coche(
    marca_id: int,
    coche: CocheCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Marca).where(Marca.id == marca_id))
    marca = result.scalar_one_or_none()

    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    db_coche = Coche(**coche.model_dump(), marca_id=marca_id)

    db.add(db_coche)
    await db.commit()

    result = await db.execute(
        select(Coche)
        .where(Coche.id == db_coche.id)
        .options(selectinload(Coche.marca), selectinload(Coche.colores))
    )
    return result.scalar_one()


@app.get("/coches/", response_model=list[CocheResponse])
async def list_coches(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Coche).options(selectinload(Coche.marca), selectinload(Coche.colores))
    )
    return result.scalars().all()


@app.get("/coches/{coche_id}", response_model=CocheResponse)
async def read_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Coche)
        .where(Coche.id == coche_id)
        .options(selectinload(Coche.marca), selectinload(Coche.colores))
    )
    coche = result.scalar_one_or_none()

    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    return coche


@app.put("/coches/{coche_id}", response_model=CocheResponse)
async def update_coche(
    coche_id: int,
    coche: CocheUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Marca).where(Marca.id == coche.marca_id))
    marca = result.scalar_one_or_none()

    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    result = await db.execute(
        select(Coche)
        .where(Coche.id == coche_id)
        .options(selectinload(Coche.marca), selectinload(Coche.colores))
    )
    db_coche = result.scalar_one_or_none()

    if not db_coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    for key, value in coche.model_dump().items():
        setattr(db_coche, key, value)

    await db.commit()

    result = await db.execute(
        select(Coche)
        .where(Coche.id == coche_id)
        .options(selectinload(Coche.marca), selectinload(Coche.colores))
    )
    return result.scalar_one()


@app.delete("/coches/{coche_id}")
async def delete_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = result.scalar_one_or_none()

    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    await db.delete(coche)
    await db.commit()

    return {"mensaje": "Coche eliminado"}


@app.post("/colores/", response_model=ColorResponse)
async def create_color(color: ColorCreate, db: AsyncSession = Depends(get_db)):
    db_color = Color(**color.model_dump())

    db.add(db_color)
    await db.commit()
    await db.refresh(db_color)

    return db_color


@app.get("/colores/", response_model=list[ColorResponse])
async def list_colores(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Color))
    return result.scalars().all()


@app.post("/coches/{coche_id}/colores/{color_id}")
async def asignar_color(
    coche_id: int,
    color_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Coche)
        .where(Coche.id == coche_id)
        .options(selectinload(Coche.colores))
    )
    coche = result.scalar_one_or_none()

    result_color = await db.execute(select(Color).where(Color.id == color_id))
    color = result_color.scalar_one_or_none()

    if not coche or not color:
        raise HTTPException(status_code=404, detail="Coche o color no encontrado")

    if color not in coche.colores:
        coche.colores.append(color)
        await db.commit()

    return {"mensaje": "Color vinculado con exito"}


"""
Version de la practica 2, antes de aplicar relaciones.

En esta version, "marca" era un texto dentro de Coche y todavia no existia
la relacion 1:N Marca-Coche ni la relacion N:N Coche-Color.

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
    db: AsyncSession = Depends(get_db),
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
