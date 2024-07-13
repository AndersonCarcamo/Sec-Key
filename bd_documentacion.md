# Documentación del Backend

## Modelo: User

**Nombre de la tabla:** `users`

| Columna    | Tipo       | Descripción                                      |
|------------|------------|--------------------------------------------------|
| dni        | String(8)  | DNI del usuario, clave primaria                  |
| nombre     | String(50) | Nombre del usuario, no nulo                      |
| apellido   | String(50) | Apellido del usuario, no nulo                    |
| gmail      | String(50) | Gmail del usuario, no nulo y único               |
| password   | String(255)| Contraseña del usuario, no nulo                  |
| foto       | String(255)| URL de la foto del usuario, no nulo              |
| politicas  | Boolean    | Aceptación de políticas, no nulo                 |
| isadmin    | Boolean    | Indicador de si es administrador, por defecto `False` |
| iscliente  | Boolean    | Indicador de si es cliente, por defecto `False`  |

**Métodos:**

```python
def as_dict(self):
    return {
        'dni': self.dni,
        'nombre': self.nombre,
        'apellido': self.apellido,
        'gmail': self.gmail,
        'password': self.password,
        'foto': self.foto,
        'politicas': self.politicas,
        'isadmin': self.isadmin,
        'iscliente': self.iscliente
    }
```

## Modelo: AdminUser

**Nombre de la tabla:** `admin_users`

| Columna    | Tipo       | Descripción                                      |
|------------|------------|--------------------------------------------------|
| dni        | String(8)  | DNI del usuario, clave foránea de `users.dni`    |
| codadmin   | String(8)  | Código de administrador, no nulo y único         |

**Relaciones:**
- Relación uno a uno con la tabla `users`

**Métodos:**

```python
def as_dict(self):
    return {
        'dni': self.dni,
        'codadmin': self.codadmin
    }
```

## Modelo: ClienteUser

**Nombre de la tabla:** `cliente_users`

| Columna    | Tipo       | Descripción                                      |
|------------|------------|--------------------------------------------------|
| dni        | String(8)  | DNI del usuario, clave foránea de `users.dni`    |

**Métodos:**

```python
def as_dict(self):
    return {col.name: getattr(self, col.name) for col in self.__table__.columns}
```

## Modelo: Visitor

**Nombre de la tabla:** `visitors`

| Columna    | Tipo       | Descripción                                      |
|------------|------------|--------------------------------------------------|
| dni        | String(8)  | DNI del visitante, clave primaria                |
| nombre     | String(50) | Nombre del visitante, no nulo                    |
| apellido   | String(50) | Apellido del visitante, no nulo                  |
| edad       | Integer    | Edad del visitante, no nulo                      |
| foto       | String(255)| URL de la foto del visitante, no nulo            |
| dni_cliente| String(8)  | DNI del cliente asociado, clave foránea de `cliente_users.dni` |

**Métodos:**

```python
def as_dict(self):
    return {col.name: getattr(self, col.name) for col in self.__table__.columns}
```

## Modelo: Empleado

**Nombre de la tabla:** `empleados`

| Columna          | Tipo       | Descripción                                      |
|------------------|------------|--------------------------------------------------|
| codigo_empleado  | String(8)  | Código del empleado, clave primaria              |
| nombre           | String(50) | Nombre del empleado, no nulo                     |
| apellido         | String(50) | Apellido del empleado, no nulo                   |
| dni              | String(8)  | DNI del empleado, único y no nulo                |
| email            | String(50) | Email del empleado, único y no nulo              |
| foto             | String(255)| URL de la foto del empleado, no nulo             |
| cargo            | String(50) | Cargo del empleado, no nulo                      |

**Métodos:**

```python
def as_dict(self):
    return {col.name: getattr(self, col.name) for col in self.__table__.columns}
```

## Modelo: Cuarto

**Nombre de la tabla:** `cuartos`

| Columna      | Tipo          | Descripción                                      |
|--------------|---------------|--------------------------------------------------|
| codigo_cuarto| String(4)     | Código del cuarto, clave primaria                |
| nro_cuarto   | String(1)     | Número del cuarto, no nulo                       |
| piso         | Integer       | Piso del cuarto, no nulo                         |
| costo        | Numeric(10, 2)| Costo del cuarto, no nulo                        |

**Métodos:**

```python
def as_dict(self):
    return {col.name: getattr(self, col.name) for col in self.__table__.columns}
```

## Modelo: ClienteCuarto

**Nombre de la tabla:** `cliente_cuartos`

| Columna       | Tipo       | Descripción                                      |
|---------------|------------|--------------------------------------------------|
| dni_cliente   | String(8)  | DNI del cliente, clave foránea de `cliente_users.dni` |
| codigo_cuarto | String(4)  | Código del cuarto, clave foránea de `cuartos.codigo_cuarto` |

**Métodos:**

```python
def as_dict(self):
    return {col.name: getattr(self, col.name) for col in self.__table__.columns}
```

## Modelo: CuartoEmpleado

**Nombre de la tabla:** `cuartos_empleados`

| Columna         | Tipo       | Descripción                                      |
|-----------------|------------|--------------------------------------------------|
| codigo_cuarto   | String(4)  | Código del cuarto, clave foránea de `cuartos.codigo_cuarto` |
| codigo_empleado | String(8)  | Código del empleado, clave foránea de `empleados.codigo_empleado` |

**Métodos:**

```python
def as_dict(self):
    return {col.name: getattr(self, col.name) for col in self.__table__.columns}
```