import asyncio

from sqlalchemy import text

from database import engine, Base
from models import Coche, Color, Marca


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        columns = await conn.execute(text("PRAGMA table_info(coches)"))
        column_names = {row[1] for row in columns}

        if "marca_id" not in column_names:
            await conn.execute(text("ALTER TABLE coches ADD COLUMN marca_id INTEGER"))

        if "marca" in column_names:
            await conn.execute(
                text(
                    """
                    INSERT OR IGNORE INTO marcas (nombre)
                    SELECT DISTINCT marca
                    FROM coches
                    WHERE marca IS NOT NULL AND marca != ''
                    """
                )
            )
            await conn.execute(
                text(
                    """
                    UPDATE coches
                    SET marca_id = (
                        SELECT marcas.id
                        FROM marcas
                        WHERE marcas.nombre = coches.marca
                    )
                    WHERE marca_id IS NULL
                    """
                )
            )


asyncio.run(init_db())
