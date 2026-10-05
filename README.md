# 🐾 Sistema de Gestión Veterinaria

Backend para la gestión de una clínica veterinaria, desarrollado como proyecto académico de **Programación V**. El sistema permite administrar propietarios y mascotas mediante operaciones CRUD, utilizando Python y MySQL.

---

## 🎓 Información Académica

* **Materia:** Programación V
* **Institución:** CIAF
* **Entrega:** Trabajo del Corte 1
* **Fecha:** Octubre 2026
* **Autores:**

  * Jonathan Cañola Salazar
  * Jorge Andrés García Mojica

---

## 📝 Descripción del Proyecto

Este proyecto es una implementación backend orientada a la gestión de una clínica veterinaria.

El sistema funciona como una interfaz de línea de comandos (CLI) que simula el comportamiento de una API RESTful, interactuando directamente con una base de datos relacional **MySQL**.

Actualmente permite administrar dos entidades principales:

* **Propietarios (`owners`)**
* **Mascotas (`pets`)**

El proyecto implementa operaciones CRUD para ambas entidades:

* `GET`
* `POST`
* `PUT`
* `PATCH`
* `DELETE`

El desarrollo se enfoca en buenas prácticas de programación, separación de responsabilidades, seguridad en el acceso a datos y validación de información ingresada por el usuario.

---

## 🏗️ Arquitectura del Proyecto

El código está organizado mediante una estructura modular que separa las responsabilidades principales del sistema.

### 📌 Capa de Enrutamiento — `routes/`

Contiene los scripts encargados de ejecutar las operaciones correspondientes a los métodos HTTP:

* `GET`
* `POST`
* `PUT`
* `PATCH`
* `DELETE`

Estos scripts interactúan con el usuario y generan respuestas estructuradas.

### 📌 Capa de Acceso a Datos — `database/`

El archivo:

```text
database/db_connection.py
```

centraliza la conexión con MySQL y las operaciones relacionadas con la base de datos.

También se encarga del control de transacciones mediante:

* `COMMIT`
* `ROLLBACK`

### 📌 Capa de Utilidades — `utils/`

El archivo:

```text
utils/functions.py
```

contiene funciones auxiliares para:

* Validación de datos.
* Expresiones regulares.
* Conversión y mapeo de información.
* Funciones utilizadas por los diferentes endpoints.

---

## 🛡️ Seguridad y Buenas Prácticas

El proyecto implementa diferentes medidas de seguridad y buenas prácticas.

### 1. Prevención de Inyección SQL

Las consultas utilizan parámetros preparados mediante `%s` en lugar de concatenar directamente los valores proporcionados por el usuario.

Ejemplo:

```python
cursor.execute(
    "SELECT * FROM owners WHERE document = %s",
    (document,)
)
```

Esto ayuda a prevenir ataques de **inyección SQL (CWE-89)**.

### 2. Protección de Credenciales

Las credenciales de conexión a MySQL se almacenan en un archivo `.env`.

Este archivo debe estar incluido en `.gitignore` para evitar que las credenciales sean subidas al repositorio.

### 3. Manejo de Errores

Las operaciones de acceso a datos utilizan bloques `try-except` para manejar errores y evitar mostrar información interna de la aplicación o de la base de datos al usuario.

### 4. Validación de Entradas

El proyecto utiliza validaciones mediante expresiones regulares para comprobar información como:

* Documentos.
* Correos electrónicos.
* Nombres.
* Números telefónicos.

### 5. Seguridad en Operaciones Destructivas

Las operaciones `DELETE` requieren una confirmación adicional antes de ejecutarse.

Esto ayuda a evitar eliminaciones accidentales.

---

## 🗄️ Base de Datos

La aplicación utiliza **MySQL** como sistema gestor de bases de datos.

### Crear la base de datos

```sql
CREATE DATABASE IF NOT EXISTS veterinary_clinic_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE veterinary_clinic_db;
```

Las tablas principales utilizadas por el sistema son:

* `owners`
* `pets`

> Los scripts de creación de las tablas se encuentran en el proyecto y deben ejecutarse antes de utilizar los endpoints.

---

## 👤 Usuario de la Base de Datos

Para la conexión de la aplicación se puede crear un usuario específico con los permisos necesarios:

```sql
CREATE USER 'vet_admin'@'localhost'
IDENTIFIED BY 'TuPasswordSegura';
```

Se asignan únicamente los permisos necesarios para las operaciones CRUD:

```sql
GRANT SELECT, INSERT, UPDATE, DELETE
ON veterinary_clinic_db.*
TO 'vet_admin'@'localhost';
```

Aplicar los cambios:

```sql
FLUSH PRIVILEGES;
```

Para verificar los permisos:

```sql
SHOW GRANTS FOR 'vet_admin'@'localhost';
```

---

## 📂 Estructura del Proyecto

```text
veterinary_clinic/
│
├── .env
├── .gitignore
├── database/
│   └── db_connection.py
│
├── routes/
│   ├── owners/
│   │   ├── endpoint_get_owner.py
│   │   ├── endpoint_post_owner.py
│   │   ├── endpoint_put_owner.py
│   │   ├── endpoint_patch_owner.py
│   │   └── endpoint_delete_owner.py
│   │
│   └── pets/
│       ├── endpoint_get_pet.py
│       ├── endpoint_post_pet.py
│       ├── endpoint_put_pet.py
│       ├── endpoint_patch_pet.py
│       └── endpoint_delete_pet.py
│
└── utils/
    └── functions.py
```

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd veterinary_clinic
```

---

### 2. Crear el entorno virtual

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

### 3. Instalar las dependencias

```bash
pip install mysql-connector-python python-dotenv
```

---

### 4. Configurar las variables de entorno

Crear un archivo llamado:

```text
.env
```

en la raíz del proyecto.

Ejemplo:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=veterinary_clinic_db
DB_USER=vet_admin
DB_PASSWORD=TU_PASSWORD
DB_CHARSET=utf8mb4
```

**Importante:** no subir el archivo `.env` a GitHub.

El archivo `.gitignore` debe incluir:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

## ⚙️ Uso del Sistema

Los diferentes endpoints se ejecutan desde la raíz del proyecto mediante Python.

### 👤 Propietarios

| Operación | Comando                                         | Descripción                                   |
| --------- | ----------------------------------------------- | --------------------------------------------- |
| `POST`    | `python routes/owners/endpoint_post_owner.py`   | Registra un propietario validando duplicados. |
| `GET`     | `python routes/owners/endpoint_get_owner.py`    | Consulta información de un propietario.       |
| `PATCH`   | `python routes/owners/endpoint_patch_owner.py`  | Modifica parcialmente la información.         |
| `PUT`     | `python routes/owners/endpoint_put_owner.py`    | Actualiza completamente la información.       |
| `DELETE`  | `python routes/owners/endpoint_delete_owner.py` | Elimina un propietario previa confirmación.   |

### 🐶 Mascotas

| Operación | Comando                                     | Descripción                                            |
| --------- | ------------------------------------------- | ------------------------------------------------------ |
| `POST`    | `python routes/pets/endpoint_post_pet.py`   | Registra una mascota vinculada a un propietario.       |
| `GET`     | `python routes/pets/endpoint_get_pet.py`    | Consulta las mascotas de un propietario.               |
| `PATCH`   | `python routes/pets/endpoint_patch_pet.py`  | Modifica parcialmente la información de una mascota.   |
| `PUT`     | `python routes/pets/endpoint_put_pet.py`    | Actualiza completamente la información de una mascota. |
| `DELETE`  | `python routes/pets/endpoint_delete_pet.py` | Elimina una mascota previa confirmación.               |

---

## 📦 Dependencias

El proyecto utiliza las siguientes dependencias principales:

```text
mysql-connector-python
python-dotenv
```

Para instalarlas:

```bash
pip install mysql-connector-python python-dotenv
```

---

## 🔐 Recomendaciones de Seguridad

Antes de subir el proyecto a GitHub:

1. Verificar que `.env` esté incluido en `.gitignore`.
2. No publicar contraseñas reales.
3. No incluir credenciales directamente en los archivos `.py`.
4. Utilizar un usuario de MySQL específico para la aplicación.
5. Otorgar únicamente los permisos necesarios.
6. Revisar que no existan contraseñas dentro del historial de Git.

---

