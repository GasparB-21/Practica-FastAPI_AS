from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base


coche_color_association = Table(
    "coche_color",
    Base.metadata,
    Column("coche_id", ForeignKey("coches.id"), primary_key=True),
    Column("color_id", ForeignKey("colores.id"), primary_key=True),
)


class Marca(Base):
    __tablename__ = "marcas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    coches = relationship("Coche", back_populates="marca")


class Coche(Base):
    __tablename__ = "coches"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, index=True)
    modelo = Column(String, nullable=True)
    matricula = Column(String, unique=True, index=True)
    marca_id = Column(Integer, ForeignKey("marcas.id"))

    marca = relationship("Marca", back_populates="coches")
    colores = relationship(
        "Color",
        secondary=coche_color_association,
        back_populates="coches",
    )


class Color(Base):
    __tablename__ = "colores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    coches = relationship(
        "Coche",
        secondary=coche_color_association,
        back_populates="colores",
    )


"""
Version anterior de la practica, antes de aplicar relaciones.

from sqlalchemy import Column, Integer, String

from database import Base


class Coche(Base):
    __tablename__ = "coches"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, nullable=True)
    matricula = Column(String, unique=True, index=True)
"""
