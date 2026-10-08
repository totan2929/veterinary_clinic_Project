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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.db_connection import execute_multiple_query, execute_single_query
from utils.functions import clear_screen, pause, validate_doc_number

def get_pets_by_owner():
    clear_screen()
    try:
        # En vez de buscar por ID de mascota, buscamos todas las mascotas de un dueño. 
        # Es mucho más útil en la vida real.
        doc_input = input("Digite el Número de Documento del Propietario para ver sus mascotas: ")
        doc_number = validate_doc_number(doc_input)

        owner = execute_single_query("SELECT owner_id, first_name FROM owners WHERE doc_number = %s", (doc_number,))
        if not owner:
            raise ValueError("Propietario no encontrado.")

        sql = "SELECT * FROM pets WHERE owner_id = %s"
        pets = execute_multiple_query(sql, (owner['owner_id'],))

        response = {
            "code-status": 200,
            "status": "success",
            "owner": owner['first_name'],
            "total_pets": len(pets),
            "data": pets
        }
        print(json.dumps(response, indent=2, ensure_ascii=False, default=str))

    except ValueError as validation_err:
        print(f"Error de Validación: {validation_err}")
    except Exception as general_err:
        print(f"Error Interno: {general_err}")
    finally:
        pause()

if __name__ == "__main__":
    get_pets_by_owner()
