"""
Ajuste de la ruta del sistema (sys.path):
Calcula dinámicamente la ruta absoluta de la raíz del proyecto (subiendo dos niveles 
desde la ubicación actual de este script) y la inyecta en el entorno de Python.
Esto garantiza que los módulos hermanos ('database' y 'utils') puedan ser importados 
correctamente, independientemente de la carpeta desde la cual el usuario ejecute el archivo.
"""

import sys
import os
import json

# Configure system path to allow relative imports from nested routes folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from database.db_connection import execute_write_operation, execute_single_query
from utils.functions import clear_screen, pause, validate_doc_number, confirm_action_yn


def delete_owner() -> None:
    """
    Executes the DELETE flow for an owner record given their document number.
    """
    clear_screen()
    try:
        # 1. Search for existing owner record
        doc_input = input("Digite el Número de Documento del propietario a eliminar: ")
        doc_number = validate_doc_number(doc_input)

        sql_check = "SELECT owner_id, first_name, last_name FROM owners WHERE doc_number = %s"
        owner = execute_single_query(sql_check, (doc_number,))

        if not owner:
            response = {
                "status": 404,
                "error": "NotFound",
                "message": f"No se encontró ningún propietario con el documento '{doc_number}'."
            }
            print(json.dumps(response, indent=2, ensure_ascii=False))
            return

        # 2. Interactive confirmation prompt
        owner_full_name = f"{owner['first_name']} {owner['last_name']}"
        if not confirm_action_yn(f"¿Está seguro que desea eliminar a {owner_full_name}?"):
            response = {
                "status": 200,
                "message": "Operación cancelada por el usuario.",
                "data": None
            }
            print(json.dumps(response, indent=2, ensure_ascii=False))
            return

        # 3. Perform database DELETE operation
        sql_delete = "DELETE FROM owners WHERE doc_number = %s"
        affected_rows = execute_write_operation(sql_delete, (doc_number,))

        # 4. Standardized JSON output
        response = {
            "status": 200,
            "message": f"Propietario '{owner_full_name}' eliminado correctamente.",
            "affected_rows": affected_rows
        }
        print(json.dumps(response, indent=2, ensure_ascii=False))

    except ValueError as validation_err:
        # Handle validation errors (HTTP 400)
        error_response = {
            "status": 400,
            "error": "ValidationFailed",
            "detail": str(validation_err)
        }
        print(json.dumps(error_response, indent=2, ensure_ascii=False))

    except Exception as general_err:
        # Handle runtime or foreign key constraint errors (HTTP 500)
        error_response = {
            "status": 500,
            "error": "InternalError",
            "detail": f"Error interno (Posible restricción por mascotas o citas asociadas): {general_err}"
        }
        print(json.dumps(error_response, indent=2, ensure_ascii=False))

    finally:
        pause()


if __name__ == "__main__":
    delete_owner()