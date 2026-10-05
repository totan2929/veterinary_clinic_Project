```markdown
# 🐾 Sistema de Gestión Veterinaria (Backend API RESTful)

## 🎓 Información Académica
* **Materia:** Programación V
* **Institución:** CIAF
* **Entrega:** Trabajo del Corte 1
* **Fecha:** Octubre 2026
* **Autores:** 
  * Jonathan Cañola Salazar
  * Jorge Andrés García Mojica

## 📝 Descripción del Proyecto
Este proyecto es una implementación backend orientada a la gestión de una clínica veterinaria. Actúa como una interfaz de línea de comandos (CLI) que simula el comportamiento de una API RESTful, interactuando directamente con una base de datos relacional (MySQL). El sistema permite administrar dos entidades principales de manera transaccional: **Propietarios (`owners`)** y **Mascotas (`pets`)**.

El desarrollo se enfoca en el cumplimiento estricto de buenas prácticas de programación, separación de responsabilidades (arquitectura multicapa), seguridad de acceso a datos y experiencia de usuario en consola.

## 🏗️ Arquitectura y Patrones de Diseño
El código está estructurado en un patrón modular que separa la lógica de negocio, el acceso a datos y las rutas de ejecución:

* **Capa de Enrutamiento (`routes/`):** Contiene los scripts ejecutables que simulan los métodos HTTP (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`). Intercambian datos con el usuario y emiten respuestas en formato JSON estructurado.
* **Capa de Acceso a Datos (`database/db_connection.py`):** Centraliza la conexión a MySQL, implementando el principio *Fail-Fast* y manejando el control de transacciones (ACID) mediante `COMMIT` y `ROLLBACK`[cite: 5].
* **Capa de Utilidades y Reglas de Negocio (`utils/functions.py`):** Aisla las validaciones estrictas (Regex) y mapeos de datos (español a inglés) para mantener los controladores limpios[cite: 16].

## 🛡️ Seguridad y Buenas Prácticas Implementadas
1. **Prevención de Inyección SQL (CWE-89):** Todas las consultas a la base de datos utilizan parámetros preparados (`%s`) en lugar de concatenación de strings[cite: 5].
2. **Protección de Credenciales (CWE-798):** Las variables sensibles de conexión a la base de datos se consumen desde un archivo `.env` externo, el cual está excluido del control de versiones mediante `.gitignore`[cite: 5].
3. **Manejo Seguro de Errores (CWE-209):** Uso de bloques `try-except` para capturar excepciones, enmascarar errores internos del servidor y devolver mensajes JSON amigables sin exponer la estructura de la base de datos[cite: 6, 8, 9].
4. **Validación Estricta de Entradas:** Implementación de expresiones regulares para validar formatos de documentos, correos, nombres y teléfonos antes de cualquier interacción con la base de datos[cite: 16].
5. **Seguridad Transaccional:** Se implementó una confirmación de doble paso (`confirm_action_yn`) para operaciones destructivas (`DELETE`)[cite: 11, 16].

## 🗄️ Scripts SQL de Configuración (Base de Datos y Permisos)
Para la evaluación del sistema, se deben ejecutar las siguientes sentencias en MySQL para preparar el entorno y garantizar que el usuario de la aplicación tenga los privilegios exactos y necesarios.

**1. Creación de la Base de Datos y Tablas (Resumen):**
```sql
CREATE DATABASE IF NOT EXISTS veterinary_clinic_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE veterinary_clinic_db;

-- (Aquí se asume la ejecución de los scripts de creación de tablas 'owners' y 'pets' previamente desarrollados)

```

**2. Creación del Usuario y Asignación de Privilegios:**

```sql
-- Crear el usuario de conexión específico para la aplicación
CREATE USER 'vet_admin'@'localhost' IDENTIFIED BY 'TuPasswordSegura';

-- Otorgar privilegios estrictamente necesarios para el CRUD
GRANT SELECT, INSERT, UPDATE, DELETE ON veterinary_clinic_db.* TO 'vet_admin'@'localhost';

-- Aplicar los cambios
FLUSH PRIVILEGES;

-- Consultar los privilegios asignados (Para captura de pantalla de evidencia)
SHOW GRANTS FOR 'vet_admin'@'localhost';

```

## 📂 Estructura del Directorio

```text
veterinary_clinic/
├── .env                  # Variables de entorno (No subido al repo)
├── .gitignore            # Reglas de exclusión (archivos caché y .env)
├── database/
│   └── db_connection.py  # Motor de conexión y operaciones CRUD
├── routes/
│   ├── owners/           # Módulo de Propietarios
│   │   ├── endpoint_get_owner.py
│   │   ├── endpoint_post_owner.py
│   │   ├── endpoint_put_owner.py
│   │   ├── endpoint_patch_owner.py
│   │   └── endpoint_delete_owner.py
│   └── pets/             # Módulo de Mascotas
│       ├── endpoint_get_pet.py
│       ├── endpoint_post_pet.py
│       ├── endpoint_put_pet.py
│       ├── endpoint_patch_pet.py
│       └── endpoint_delete_pet.py
└── utils/
    └── functions.py      # Validadores, Regex y UI de consola

```

## 🚀 Instalación y Configuración

1. **Clonar el repositorio y acceder a la carpeta:**
```bash
git clone <url-del-repositorio>
cd veterinary_clinic

```


2. **Crear y activar el entorno virtual:**
```bash
# En Linux/Mac:
python3 -m venv .venv
source .venv/bin/activate

```


3. **Instalar dependencias:**
```bash
pip install mysql-connector-python python-dotenv

```


4. **Configurar las variables de entorno:**
Cree un archivo llamado `.env` en la raíz del proyecto y configure sus credenciales basadas en el usuario SQL creado anteriormente:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=veterinary_clinic_db
DB_USER=vet_admin
DB_PASSWORD=VetSecurePass2026*
DB_CHARSET=utf8mb4

```



## ⚙️️ Uso del Sistema (Endpoints)

Para interactuar con el sistema, ejecute cualquiera de los endpoints desde la raíz del proyecto utilizando Python.

| Entidad | Operación | Comando de Ejecución | Descripción |
| --- | --- | --- | --- |
| **Owner** | Crear (`POST`) | `python routes/owners/endpoint_post_owner.py` | Registra dueño validando duplicados. |
| **Owner** | Leer (`GET`) | `python routes/owners/endpoint_get_owner.py` | Consulta datos por documento. |
| **Owner** | Parcial (`PATCH`) | `python routes/owners/endpoint_patch_owner.py` | Modifica un campo específico. |
| **Owner** | Total (`PUT`) | `python routes/owners/endpoint_put_owner.py` | Sobrescribe toda la información. |
| **Owner** | Eliminar (`DELETE`) | `python routes/owners/endpoint_delete_owner.py` | Borra dueño previa confirmación. |
| **Pet** | Crear (`POST`) | `python routes/pets/endpoint_post_pet.py` | Registra mascota vinculada a un dueño. |
| **Pet** | Leer (`GET`) | `python routes/pets/endpoint_get_pet.py` | Lista mascotas de un propietario. |
| **Pet** | Parcial (`PATCH`) | `python routes/pets/endpoint_patch_pet.py` | Supermenú para actualizar 12 campos. |
| **Pet** | Total (`PUT`) | `python routes/pets/endpoint_put_pet.py` | Sobrescribe datos respetando ID. |
| **Pet** | Eliminar (`DELETE`) | `python routes/pets/endpoint_delete_pet.py` | Borra mascota previa confirmación. |

```

```