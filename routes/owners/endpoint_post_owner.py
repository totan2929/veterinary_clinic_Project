import sys
import os
import json

# Configure system path to allow relative imports from nested routes folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from database.db_connection import execute_write_operation_returning_id, execute_single_query
from utils.functions import (
    clear_screen, pause, validate_doc_type, validate_doc_number,
    validate_person_name, validate_phone, validate_email, validate_status
)


def check_duplicate_doc(doc_number: str) -> None:
    """
    Validates that no owner exists with the same document number.

    Parameters:
        doc_number (str): Document number to check against the database.
    """
    sql = "SELECT owner_id FROM owners WHERE doc_number = %s"
    row = execute_single_query(sql, (doc_number,))
    if row:
        raise ValueError(f"Ya existe un propietario con el documento {doc_number}.")


def create_owner() -> None:
    """
    Executes the POST flow to insert a new owner record into the database.
    Prompts for required fields including address and birth_date, validates user inputs,
    performs the INSERT operation, and outputs standardized JSON.
    """
    clear_screen()
    try:
        # 1. Input capture and validation
        doc_type = validate_doc_type(input("Tipo de Documento (CC, CE, TI, PASAPORTE): "))
        doc_number = validate_doc_number(input("Número de Documento: "))
        
        # Check for duplicate document before attempting insertion
        check_duplicate_doc(doc_number)

        first_name = validate_person_name(input("Nombres: "))
        last_name = validate_person_name(input("Apellidos: "))
        
        # Capture birth_date (Format: YYYY-MM-DD)
        birth_date = input("Fecha de Nacimiento (YYYY-MM-DD): ").strip()
        if not birth_date:
            raise ValueError("La fecha de nacimiento es obligatoria.")

        # Capture address input
        address = input("Dirección de Residencia: ").strip()

        phone = validate_phone(input("Teléfono (10 dígitos): "))
        email = validate_email(input("Correo Electrónico: "))
        status = validate_status(input("Estado (Active/Inactive): "))

        # 2. Database write operation including address and birth_date
        sql = """
            INSERT INTO owners (doc_type, doc_number, first_name, last_name, birth_date, address, phone, email, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (doc_type, doc_number, first_name, last_name, birth_date, address, phone, email, status)
        affected_rows, new_id = execute_write_operation_returning_id(sql, params)

        if not new_id:
            raise RuntimeError("Fallo al obtener el ID generado.")

        # 3. Standardized JSON response (HTTP 201 Created)
        response = {
            "status": 201,
            "message": "Propietario creado exitosamente",
            "data": {
                "owner_id": new_id,
                "doc_type": doc_type,
                "doc_number": doc_number,
                "first_name": first_name,
                "last_name": last_name,
                "birth_date": birth_date,
                "address": address,
                "phone": phone,
                "email": email,
                "status": status
            }
        }
        print(json.dumps(response, indent=2, ensure_ascii=False, default=str))

    except ValueError as validation_err:
        # Handle data validation errors (HTTP 400)
        error_response = {
            "status": 400,
            "error": "ValidationFailed",
            "detail": str(validation_err)
        }
        print(json.dumps(error_response, indent=2, ensure_ascii=False))

    except Exception as general_err:
        # Handle database connection or runtime errors (HTTP 500)
        error_response = {
            "status": 500,
            "error": "InternalError",
            "detail": str(general_err)
        }
        print(json.dumps(error_response, indent=2, ensure_ascii=False))

    finally:
        pause()


# Execute main function when running script directly
if __name__ == "__main__":
    create_owner()