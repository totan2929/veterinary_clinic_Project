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
from utils.functions import (
    clear_screen, pause, validate_pet_name, validate_pet_species, 
    validate_pet_breed, validate_pet_gender, validate_birth_date, 
    validate_weight_kg, validate_pet_color, validate_pet_coat, 
    validate_boolean_yn, validate_chip_number
)

def get_pet_by_id(pet_id):
    """Busca a la mascota por su ID."""
    sql = "SELECT * FROM pets WHERE pet_id = %s"
    return execute_single_query(sql, (pet_id,))

def update_pet_field():
    clear_screen()
    try:
        # 1. Buscar la mascota por su ID
        pet_id_input = input("Digite el ID de la mascota a actualizar: ")
        if not pet_id_input.isdigit():
            raise ValueError("El ID de la mascota debe ser un valor numérico.")
        pet_id = int(pet_id_input)
        
        pet = get_pet_by_id(pet_id)
        if not pet:
            raise ValueError("No se encontró ninguna mascota con ese ID en el sistema.")

        # 2. Súper Menú Interactivo CON DATOS ACTUALES
        clear_screen()
        print(f"--- ACTUALIZANDO MASCOTA: {pet['name'].upper()} ---")
        print(f" 1. Nombre             [Actual: {pet['name']}]")
        print(f" 2. Especie            [Actual: {pet['species']}]")
        print(f" 3. Raza               [Actual: {pet['breed']}]")
        print(f" 4. Género             [Actual: {pet['gender']}]")
        print(f" 5. Fecha Nacimiento   [Actual: {pet['estimated_birth_date']}]")
        print(f" 6. Peso (KG)          [Actual: {pet['weight_kg']}]")
        print(f" 7. Color              [Actual: {pet['color']}]")
        print(f" 8. Pelaje             [Actual: {pet['coat']}]")
        print(f" 9. Tiene Chip         [Actual: {'Sí' if pet['has_chip'] else 'No'}]")
        print(f"10. Número de Chip     [Actual: {pet['chip_number']}]")
        print(f"11. Esterilizado       [Actual: {'Sí' if pet['is_neutered'] else 'No'}]")
        print(f"12. Estado Vital       [Actual: {'Viva' if pet['is_alive'] else 'Fallecida'}]")
        print("13. Cancelar")
        
        option = input("\nSeleccione el campo a actualizar (1-13): ").strip()
        
        column_to_update = ""
        new_value = None

        if option == '1':
            new_value = validate_pet_name(input("Nuevo Nombre: "))
            column_to_update = "name"
        elif option == '2':
            new_value = validate_pet_species(input("Nueva Especie (perro/gato/ave/reptil/roedor/otro): "))
            column_to_update = "species"
        elif option == '3':
            new_value = validate_pet_breed(input("Nueva Raza: "))
            column_to_update = "breed"
        elif option == '4':
            new_value = validate_pet_gender(input("Nuevo Género (macho/hembra): "))
            column_to_update = "gender"
        elif option == '5':
            new_value = validate_birth_date(input("Nueva Fecha de Nac. (AAAA-MM-DD): "))
            column_to_update = "estimated_birth_date"
        elif option == '6':
            new_value = validate_weight_kg(input("Nuevo Peso en KG: "))
            column_to_update = "weight_kg"
        elif option == '7':
            new_value = validate_pet_color(input("Nuevo Color: "))
            column_to_update = "color"
        elif option == '8':
            new_value = validate_pet_coat(input("Nuevo Pelaje: "))
            column_to_update = "coat"
        elif option == '9':
            new_value = validate_boolean_yn(input("¿Tiene Chip? (S/N): "))
            column_to_update = "has_chip"
        elif option == '10':
            new_value = validate_chip_number(input("Nuevo Número de Chip (15 dígitos): "), 1)
            column_to_update = "chip_number"
        elif option == '11':
            new_value = validate_boolean_yn(input("¿Está esterilizado? (S/N): "))
            column_to_update = "is_neutered"
        elif option == '12':
            # Bloqueo lógico: Evita actualizar si ya estaba fallecida
            is_alive_input = validate_boolean_yn(input("¿Sigue con vida? (S/N): "))
            if pet['is_alive'] == 0 and is_alive_input == 0:
                raise ValueError("La mascota ya se encuentra registrada como fallecida.")
            new_value = is_alive_input
            column_to_update = "is_alive"
        elif option == '13':
            print("Operación cancelada por el usuario.")
            return
        else:
            raise ValueError("Opción no válida. Seleccione un número del 1 al 13.")

        # 3. Ejecutar Actualización Dinámica
        sql = f"UPDATE pets SET {column_to_update} = %s WHERE pet_id = %s"
        affected_rows = execute_write_operation(sql, (new_value, pet_id))

        # 4. Salida JSON
        response = {
            "status": "success",
            "message": f"El campo '{column_to_update}' se actualizó correctamente.",
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
    update_pet_field()