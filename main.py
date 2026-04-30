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




""""
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