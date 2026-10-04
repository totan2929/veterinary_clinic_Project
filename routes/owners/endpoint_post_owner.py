import sys
import os
import json

# Ajuste de rutas para importar desde directorios padre
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.db_connection import execute_write_operation_returning_id, execute_single_query
from utils.functions import (
    clear_screen, pause, validate_doc_type, validate_doc_number,
    validate_person_name, validate_phone, validate_email, validate_status
)

def check_duplicate_doc(doc_number):
    """Valida que no exista ya un dueño con el mismo número de documento."""
    sql = "SELECT owner_id FROM owners WHERE doc_number = %s"
    row = execute_single_query(sql, (doc_number,))
    if row:
        raise ValueError(f"Ya existe un propietario con el documento {doc_number}.")

def create_owner():
    clear_screen()
    try:
        # 1. Captura y validación de datos
        doc_type = validate_doc_type(input("Tipo de Documento (CC, CE, TI, PASAPORTE): "))
        doc_number = validate_doc_number(input("Número de Documento: "))
        
        # Validar duplicados antes de insertar (Idempotencia lógica)
        check_duplicate_doc(doc_number)

        first_name = validate_person_name(input("Nombres: "))
        last_name = validate_person_name(input("Apellidos: "))
        phone = validate_phone(input("Teléfono (10 dígitos): "))
        email = validate_email(input("Correo Electrónico: "))
        status = validate_status(input("Estado (Active/Inactive): "))

        # 2. Operación de base de datos
        sql = """
            INSERT INTO owners (doc_type, doc_number, first_name, last_name, phone, email, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (doc_type, doc_number, first_name, last_name, phone, email, status)
        affected_rows, new_id = execute_write_operation_returning_id(sql, params)

        if not new_id:
            raise RuntimeError("Fallo al obtener el ID generado.")

        # 3. Salida JSON
        response = {
            "status": "success",
            "message": "Propietario creado exitosamente",
            "data": {
                "owner_id": new_id,
                "doc_number": doc_number
            }
        }
        print(json.dumps(response, indent=2, ensure_ascii=False))

    except ValueError as validation_err:
        print(f"Error de Validación: {validation_err}")
    except Exception as general_err:
        print(f"Error Interno: {general_err}")
    finally:
        pause()

if __name__ == "__main__":
    create_owner()
