# Documentación de la API

## Descripción General
Esta API proporciona endpoints para gestionar usuarios, usuarios administradores, usuarios clientes, visitantes, empleados y habitaciones. Está construida utilizando Flask, Flask-CORS y Flask-SQLAlchemy.

## Configuración
La aplicación está configurada para usar PostgreSQL como la base de datos. La URL de la base de datos se toma de una variable de entorno `DATABASE_URL` o por defecto a una cadena de conexión especificada.

## CORS
CORS está habilitado para todas las rutas.

## Endpoints

### General

#### `GET /`
Devuelve un mensaje indicando que la API está en funcionamiento.

**Respuesta**
- `200 OK`: "API is running"

### Usuarios

#### `GET /users`
Obtiene todos los usuarios.

**Respuesta**
- `200 OK`: Lista de usuarios

#### `GET /users/<dni>`
Obtiene un usuario por DNI.

**Parámetros**
- `dni` (string): El DNI del usuario.

**Respuesta**
- `200 OK`: Objeto usuario
- `404 Not Found`: {"error": "User not found"}

#### `POST /users`
Crea un nuevo usuario.

**Solicitud**
- `application/json`:
  ```json
  {
    "dni": "string",
    "nombre": "string",
    "apellido": "string",
    "gmail": "string",
    "password": "string",
    "foto": "string",
    "politicas": "boolean",
    "isAdmin": "boolean",
    "isCliente": "boolean"
  }
  ```

**Respuesta**
- `201 Created`: Objeto usuario creado

#### `PUT /users/<dni>`
Actualiza un usuario existente por DNI.

**Parámetros**
- `dni` (string): El DNI del usuario.

**Solicitud**
- `application/json` (actualización parcial permitida):
  ```json
  {
    "nombre": "string",
    "apellido": "string",
    "gmail": "string",
    "password": "string",
    "foto": "string",
    "politicas": "boolean",
    "isAdmin": "boolean",
    "isCliente": "boolean"
  }
  ```

**Respuesta**
- `200 OK`: Objeto usuario actualizado
- `404 Not Found`: {"error": "User not found"}

#### `DELETE /users/<dni>`
Elimina un usuario por DNI.

**Parámetros**
- `dni` (string): El DNI del usuario.

**Respuesta**
- `200 OK`: {"message": "User deleted"}
- `404 Not Found`: {"error": "User not found"}

### Usuarios Administradores

#### `POST /admin_users`
Crea un nuevo usuario administrador.

**Solicitud**
- `application/json`:
  ```json
  {
    "dni": "string",
    "codadmin": "string"
  }
  ```

**Respuesta**
- `201 Created`: Objeto usuario administrador creado

#### `GET /admin_users/<dni>`
Obtiene un usuario administrador por DNI.

**Parámetros**
- `dni` (string): El DNI del usuario administrador.

**Respuesta**
- `200 OK`: Objeto usuario administrador
- `404 Not Found`: {"error": "Admin user not found"}

#### `PUT /admin_users/<dni>`
Actualiza un usuario administrador existente por DNI.

**Parámetros**
- `dni` (string): El DNI del usuario administrador.

**Solicitud**
- `application/json` (actualización parcial permitida):
  ```json
  {
    "codadmin": "string"
  }
  ```

**Respuesta**
- `200 OK`: Objeto usuario administrador actualizado
- `404 Not Found`: {"error": "Admin user not found"}

#### `POST /admin_users/verify`
Verifica un usuario administrador por DNI y código de administrador.

**Solicitud**
- `application/json`:
  ```json
  {
    "dni": "string",
    "codAdmin": "string"
  }
  ```

**Respuesta**
- `200 OK`: {"message": "Admin code verified"}
- `400 Bad Request`: {"error": "Invalid admin code"}

### Usuarios Clientes

#### `POST /cliente_users`
Crea un nuevo usuario cliente.

**Solicitud**
- `application/json`:
  ```json
  {
    "dni": "string"
  }
  ```

**Respuesta**
- `201 Created`: Objeto usuario cliente creado

#### `GET /cliente_users/<dni>`
Obtiene un usuario cliente por DNI.

**Parámetros**
- `dni` (string): El DNI del usuario cliente.

**Respuesta**
- `200 OK`: Objeto usuario cliente
- `404 Not Found`: {"error": "Cliente user not found"}

### Visitantes

#### `POST /visitors`
Crea un nuevo visitante.

**Solicitud**
- `application/json`:
  ```json
  {
    "dni": "string",
    "nombre": "string",
    "apellido": "string",
    "edad": "integer",
    "foto": "string",
    "dni_cliente": "string"
  }
  ```

**Respuesta**
- `201 Created`: Objeto visitante creado

#### `GET /visitors/<dni>`
Obtiene un visitante por DNI.

**Parámetros**
- `dni` (string): El DNI del visitante.

**Respuesta**
- `200 OK`: Objeto visitante
- `404 Not Found`: {"error": "Visitor not found"}

#### `GET /visitors/client/<dni_cliente>`
Obtiene visitantes para un cliente específico por DNI del cliente.

**Parámetros**
- `dni_cliente` (string): El DNI del cliente.

**Respuesta**
- `200 OK`: Lista de visitantes
- `404 Not Found`: {"error": "No visitors found"}

#### `PUT /visitors/<dni>`
Actualiza un visitante existente por DNI.

**Parámetros**
- `dni` (string): El DNI del visitante.

**Solicitud**
- `application/json` (actualización parcial permitida):
  ```json
  {
    "nombre": "string",
    "apellido": "string",
    "edad": "integer",
    "foto": "string",
    "dni_cliente": "string"
  }
  ```

**Respuesta**
- `200 OK`: Objeto visitante actualizado
- `404 Not Found`: {"error": "Visitor not found"}

#### `DELETE /visitors/<dni>`
Elimina un visitante por DNI.

**Parámetros**
- `dni` (string): El DNI del visitante.

**Respuesta**
- `200 OK`: {"message": "Visitor deleted"}
- `404 Not Found`: {"error": "Visitor not found"}

### Empleados

#### `POST /empleados`
Crea un nuevo empleado.

**Solicitud**
- `application/json`:
  ```json
  {
    "codigo_empleado": "string",
    "nombre": "string",
    "apellido": "string",
    "dni": "string",
    "email": "string",
    "foto": "string",
    "cargo": "string"
  }
  ```

**Respuesta**
- `201 Created`: Objeto empleado creado

#### `GET /empleados`
Obtiene todos los empleados.

**Respuesta**
- `200 OK`: Lista de empleados

#### `GET /empleados/<codigo_empleado>`
Obtiene un empleado por código de empleado.

**Parámetros**
- `codigo_empleado` (string): El código del empleado.

**Respuesta**
- `200 OK`: Objeto empleado
- `404 Not Found`: {"error": "Empleado not found"}

#### `PUT /empleados/<codigo_empleado>`
Actualiza un empleado existente por código de empleado.

**Parámetros**
- `codigo_empleado` (string): El código del empleado.

**Solicitud**
- `application/json` (actualización parcial permitida):
  ```json
  {
    "nombre": "string",
    "apellido": "string",
    "dni": "string",
    "email": "string",
    "foto": "string",
    "cargo": "string"
  }
  ```

**Respuesta**
- `200 OK`: Objeto empleado actualizado
- `404 Not Found`: {"error": "Empleado not found"}

#### `DELETE /empleados/<codigo_empleado>`
Elimina un empleado por código de empleado.

**Parámetros**
- `codigo_empleado` (string): El código del empleado.

**Respuesta**
- `200 OK`: {"message": "Empleado deleted"}
- `404 Not Found`: {"error": "Empleado not found"}

### Cuartos

#### `POST /cuartos`
Crea un nuevo cuarto.

**Solicitud**
- `application/json`:
  ```json
  {
    "codigo_cuarto": "string",
    "nro_cuarto": "integer",
    "piso": "integer",
    "costo": "float"
  }
  ```

**Respuesta**
- `201 Created`: Objeto cuarto creado

#### `GET /cuartos/<codigo_cuarto>`
Obtiene un cuarto por código de cuarto.

**Parámetros**
- `codigo_cuarto` (string): El código del cuarto.

**Respuesta**
- `200 OK`: Objeto cuarto
- `404 Not Found`: {"error": "Cuarto not found"}

#### `PUT /cuartos/<codigo_cuarto>`
Actualiza un cuarto existente por código de cuarto.

**Parámetros**
- `codigo_cuarto` (string): El código del cuarto.

**Solicitud**
- `application/json` (actualización parcial permitida):
  ```json
  {
    "nro_cuarto": "integer",
    "piso": "integer",
    "costo": "float"
  }
  ```

**Respuesta**
- `200 OK`: Ob

jeto cuarto actualizado
- `404 Not Found`: {"error": "Cuarto not found"}

#### `DELETE /cuartos/<codigo_cuarto>`
Elimina un cuarto por código de cuarto.

**Parámetros**
- `codigo_cuarto` (string): El código del cuarto.

**Respuesta**
- `200 OK`: {"message": "Cuarto deleted"}
- `404 Not Found`: {"error": "Cuarto not found"}

## Ejecutando la Aplicación
Para ejecutar la aplicación, configure la variable de entorno `DATABASE_URL` y ejecute el script:
```sh
export DATABASE_URL="your_database_url"
python app.py
```

La API estará disponible en `http://0.0.0.0:5000/` por defecto.