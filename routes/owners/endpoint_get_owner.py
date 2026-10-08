import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.db_connection import execute_single_query
from utils.functions import clear_screen, pause, validate_doc_number

def get_owner():
    clear_screen()
    try:
        # 1. Captura de datos
        doc_input = input("Digite el Número de Documento a consultar: ")
        doc_number = validate_doc_number(doc_input)

        # 2. Consulta a base de datos
        sql = "SELECT * FROM owners WHERE doc_number = %s"
        owner = execute_single_query(sql, (doc_number,))

        # 3. Salida JSON
        if not owner:
            print(json.dumps({"status": "error", "message": "Propietario no encontrado."}, indent=2))
            return

        response = {
            "code-status": 200,
            "status": "success",
            "data": owner
        }
        print(json.dumps(response, indent=2, ensure_ascii=False, default=str))

    except ValueError as validation_err:
        print(f"Error de Validación: {validation_err}")
    except Exception as general_err:
        print(f"Error Interno: {general_err}")
    finally:
        pause()

if __name__ == "__main__":
    get_owner()
