import sys
import os
import json

# Configure system path to allow relative imports from nested routes folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from database.db_connection import execute_write_operation, execute_single_query
from utils.functions import (
    clear_screen,
    pause,
    validate_doc_number,
    validate_person_name,
    validate_phone,
    validate_email,
    validate_status
)


def get_owner_by_doc(doc_number: str) -> dict:
    """
    Fetches a single owner record from the database by document number.

    Parameters:
        doc_number (str): The owner's identification document number.

    Returns:
        dict: The retrieved owner record or None if not found.
    """
    sql = "SELECT * FROM owners WHERE doc_number = %s"
    return execute_single_query(sql, (doc_number,))


def update_owner_field_by_doc(column_name: str, new_value: str, doc_number: str) -> int:
    """
    Dynamically updates a specific column for an owner in the database.

    Parameters:
        column_name (str): The column field to be updated.
        new_value (str): The new validated value.
        doc_number (str): The owner's document number.

    Returns:
        int: Number of affected rows in the database.
    """
    sql = f"UPDATE owners SET {column_name} = %s WHERE doc_number = %s"
    return execute_write_operation(sql, (new_value, doc_number))


def run_patch_owner() -> None:
    """
    Executes the interactive PATCH flow to update a single specific field
    of an owner (Name, Last Name, Phone, Email, or Status).
    """
    clear_screen()
    try:
        # 1. Search for existing owner record
        doc_input = input("Digite el Número de Documento del propietario a actualizar: ")
        doc_number = validate_doc_number(doc_input)
        
        owner = get_owner_by_doc(doc_number)
        if not owner:
            response = {
                "status": 404,
                "error": "NotFound",
                "message": f"No se encontró ningún propietario con el documento '{doc_number}'."
            }
            print(json.dumps(response, indent=2, ensure_ascii=False))
            return

        # 2. Display dynamic field selection menu with current data
        clear_screen()
        print(f"--- ACTUALIZANDO PROPIETARIO: {owner['first_name']} {owner['last_name']} ---")
        print(f"1. Actualizar Nombres            [Dato actual: {owner['first_name']}]")
        print(f"2. Actualizar Apellidos          [Dato actual: {owner['last_name']}]")
        print(f"3. Actualizar Teléfono           [Dato actual: {owner['phone']}]")
        print(f"4. Actualizar Correo Electrónico [Dato actual: {owner['email']}]")
        print(f"5. Actualizar Estado             [Estado actual: {owner['status']}]")
        print("6. Cancelar")
        
        option = input("\nSeleccione el campo a actualizar (1-6): ").strip()
        
        column_to_update = ""
        new_value = None

        # 3. Process selection and validate input per field
        if option == '1':
            new_value = validate_person_name(input("Nuevos Nombres: "))
            column_to_update = "first_name"
        elif option == '2':
            new_value = validate_person_name(input("Nuevos Apellidos: "))
            column_to_update = "last_name"
        elif option == '3':
            new_value = validate_phone(input("Nuevo Teléfono (10 dígitos): "))
            column_to_update = "phone"
        elif option == '4':
            new_value = validate_email(input("Nuevo Correo Electrónico: "))
            column_to_update = "email"
        elif option == '5':
            new_status = validate_status(input("Nuevo Estado (Active/Inactive): "))
            if new_status == owner['status']:
                raise ValueError(f"El propietario ya se encuentra en estado '{new_status}'.")
            new_value = new_status
            column_to_update = "status"
        elif option == '6':
            response = {
                "status": 200,
                "message": "Operación cancelada por el usuario.",
                "data": None
            }
            print(json.dumps(response, indent=2, ensure_ascii=False))
            return
        else:
            raise ValueError("Opción no válida seleccionada del menú.")

        # 4. Execute single field database update
        affected_rows = update_owner_field_by_doc(column_to_update, new_value, doc_number)

        # 5. Fetch updated record to return in JSON response
        updated_owner = get_owner_by_doc(doc_number)

        response = {
            "status": 200,
            "message": f"Campo '{column_to_update}' actualizado correctamente.",
            "affected_rows": affected_rows,
            "data": updated_owner
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
        # Handle database or unexpected runtime errors (HTTP 500)
        error_response = {
            "status": 500,
            "error": "InternalError",
            "detail": str(general_err)
        }
        print(json.dumps(error_response, indent=2, ensure_ascii=False))

    finally:
        # Pause execution to allow viewing output before exit
        pause()


# Execute main function when running script directly
if __name__ == "__main__":
    run_patch_owner()