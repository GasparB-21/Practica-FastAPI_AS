# Practica FastAPI con SQLAlchemy Async

Este proyecto es una API desarrollada con FastAPI y SQLAlchemy asincrono. La practica trabaja con coches y aplica relaciones entre tablas siguiendo el tutorial de relaciones:

- Una marca puede tener muchos coches: relacion 1:N.
- Un coche pertenece a una sola marca.
- Un coche puede tener varios colores y un color puede estar asociado a varios coches: relacion N:N.

La base de datos usada es SQLite mediante `aiosqlite`, y el archivo de base de datos se guarda como `test.db`.

## Estructura principal

- `main.py`: contiene la aplicacion FastAPI, los esquemas de Pydantic y los endpoints.
- `models.py`: contiene los modelos SQLAlchemy `Marca`, `Coche`, `Color` y la tabla intermedia `coche_color`.
- `database.py`: configura la conexion asincrona con SQLite.
- `dependencies.py`: define la dependencia `get_db` para obtener sesiones de base de datos.
- `init_db.py`: crea las tablas necesarias en la base de datos.

## Instalacion y ejecucion

Para ejecutar el proyecto es necesario tener instalado FastAPI, Uvicorn, SQLAlchemy y el driver asíncrono de SQLite aiosqlite.

Desde la carpeta del proyecto, ejecuta los siguientes comandos.

Primero instala FastAPI y Uvicorn:

```bash
pip install fastapi uvicorn
```

Instala SQLAlchemy y el driver asincrono de SQLite:

```bash
pip install sqlalchemy aiosqlite
```

Crea o actualiza las tablas de la base de datos:

```bash
python init_db.py
```

Arranca el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

Cuando el servidor este en marcha, la API estara disponible en:

```text
http://127.0.0.1:8000
```

Tambien puedes abrir la documentacion interactiva de FastAPI en:

```text
http://127.0.0.1:8000/docs
```

## Endpoints disponibles

### Marcas

Crear una marca:

```http
POST /marcas/
```

Ejemplo de JSON:

```json
{
  "nombre": "Toyota"
}
```

Listar marcas:

```http
GET /marcas/
```

### Coches

Crear un coche dentro de una marca:

```http
POST /marcas/{marca_id}/coches/
```

Ejemplo de JSON:

```json
{
  "cliente_id": 1,
  "modelo": "Corolla",
  "matricula": "1234ABC"
}
```

Listar todos los coches con su marca y colores:

```http
GET /coches/
```

Obtener un coche por ID:

```http
GET /coches/{coche_id}
```

Actualizar un coche:

```http
PUT /coches/{coche_id}
```

Ejemplo de JSON:

```json
{
  "cliente_id": 1,
  "modelo": "Civic",
  "matricula": "5678DEF",
  "marca_id": 2
}
```

Eliminar un coche:

```http
DELETE /coches/{coche_id}
```

### Colores

Crear un color:

```http
POST /colores/
```

Ejemplo de JSON:

```json
{
  "nombre": "Rojo"
}
```

Listar colores:

```http
GET /colores/
```

Asignar un color a un coche:

```http
POST /coches/{coche_id}/colores/{color_id}
```

Este endpoint crea la relacion N:N entre un coche y un color usando la tabla intermedia `coche_color`.

## Flujo recomendado para probar

1. Crear una marca con `POST /marcas/`.
2. Crear un coche asociado a esa marca con `POST /marcas/{marca_id}/coches/`.
3. Crear un color con `POST /colores/`.
4. Asignar el color al coche con `POST /coches/{coche_id}/colores/{color_id}`.
5. Consultar `GET /coches/` para ver el coche con su marca y sus colores.
