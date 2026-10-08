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

from database.db_connection import execute_write_operation, execute_single_query
# Usamos validate_boolean_yn en lugar de la que nos está dando problemas
from utils.functions import clear_screen, pause, validate_boolean_yn

def delete_pet():
    clear_screen()
    try:
        # 1. Pedir ID y buscar si existe
        pet_id_input = input("Digite el ID de la mascota a eliminar: ")
        if not pet_id_input.isdigit():
            raise ValueError("El ID debe ser numérico.")
        pet_id = int(pet_id_input)
        
        pet = execute_single_query("SELECT name FROM pets WHERE pet_id = %s", (pet_id,))
        if not pet:
            raise ValueError("No se encontró ninguna mascota con ese ID en la base de datos.")
            
        # 2. Confirmación de seguridad
        clear_screen()
        print(f"--- ELIMINACIÓN DE MASCOTA ---")
        print(f"ATENCIÓN: Está a punto de eliminar permanentemente a la mascota '{pet['name'].upper()}'.")
        
        # Validamos con la función que ya existe y funciona (S = 1, N = 0)
        confirm = validate_boolean_yn(input("¿Está absolutamente seguro? (S/N): "))
        
        if confirm == 1:
            # 3. Ejecutar eliminación
            sql = "DELETE FROM pets WHERE pet_id = %s"
            affected_rows = execute_write_operation(sql, (pet_id,))
            
            response = {
                "code-status": 200,
                "status": "success",
                "message": "Registro eliminado exitosamente de la base de datos.",
                "affected_rows": affected_rows
            }
            print(json.dumps(response, indent=2, ensure_ascii=False))
        else:
            print("\nOperación cancelada. El registro no fue modificado.")

    except ValueError as err:
        print(f"Error: {err}")
    except Exception as err:
        print(f"Error Interno: {err}")
    finally:
        pause()

if __name__ == "__main__":
    delete_pet()