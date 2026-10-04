import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.db_connection import execute_write_operation, execute_single_query
from utils.functions import (
    clear_screen, pause, validate_doc_number, validate_person_name, 
    validate_phone, validate_email, validate_status
)

def replace_owner():
    clear_screen()
    try:
        doc_input = input("Digite el Número de Documento del propietario a reemplazar (PUT): ")
        doc_number = validate_doc_number(doc_input)

        owner = execute_single_query("SELECT owner_id FROM owners WHERE doc_number = %s", (doc_number,))
        if not owner:
            raise ValueError("El propietario no existe.")

        print("\n--- INGRESE LOS NUEVOS DATOS COMPLETOS ---")
        first_name = validate_person_name(input("Nuevos Nombres: "))
        last_name = validate_person_name(input("Nuevos Apellidos: "))
        phone = validate_phone(input("Nuevo Teléfono: "))
        email = validate_email(input("Nuevo Correo: "))
        status = validate_status(input("Nuevo Estado (Active/Inactive): "))

        sql = """
            UPDATE owners 
            SET first_name = %s, last_name = %s, phone = %s, email = %s, status = %s
            WHERE doc_number = %s
        """
        params = (first_name, last_name, phone, email, status, doc_number)
        affected_rows = execute_write_operation(sql, params)

        response = {
            "status": "success",
            "message": "Datos del propietario reemplazados completamente.",
            "affected_rows": affected_rows
        }
        print(json.dumps(response, indent=2, ensure_ascii=False))

    except ValueError as validation_err:
        print(f"Error de Validación: {validation_err}")
    except Exception as general_err:
        print(f"Error Interno: {general_err}")
    finally:
        pause()

if __name__ == "__main__":
    replace_owner()
