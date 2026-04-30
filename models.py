from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Coche(Base):
    __tablename__ = "coches"

    id = Column(Integer, primary_key=True, index=True)
    #No agregamos el cliente_id como clave foránea, ya que no hemos definido una tabla de clientes en este ejemplo
    cliente_id = Column(Integer, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, nullable=True)
    matricula = Column(String, unique=True, index=True)