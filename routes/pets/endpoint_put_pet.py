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

def update_pet_completely():
    clear_screen()
    try:
        # 1. Buscar la mascota actual
        pet_id_input = input("Digite el ID de la mascota a actualizar por completo: ")
        if not pet_id_input.isdigit():
            raise ValueError("El ID debe ser numérico.")
        pet_id = int(pet_id_input)
        
        pet = get_pet_by_id(pet_id)
        if not pet:
            raise ValueError("No se encontró ninguna mascota con ese ID.")

        clear_screen()
        print(f"--- ACTUALIZACIÓN COMPLETA (PUT): {pet['name'].upper()} ---")
        print("Instrucción: Si deseas mantener el dato actual [mostrado entre corchetes], simplemente presiona ENTER.\n")

        # --- Funciones Auxiliares para el PUT ---
        def get_new_val(prompt, current, validator):
            val = input(f"{prompt} [{current}]: ").strip()
            if val == "":
                return current # Si presiona Enter, conserva el original
            return validator(val) # Si escribe algo, lo valida

        def get_new_bool(prompt, current_int):
            current_str = "S" if current_int == 1 else "N"
            val = input(f"{prompt} [{current_str}]: ").strip()
            if val == "":
                return current_int
            return validate_boolean_yn(val)
        # ----------------------------------------

        # 2. Captura de datos con opción de omitir
        name = get_new_val("Nombre", pet['name'], validate_pet_name)
        species = get_new_val("Especie (perro/gato/ave/reptil/roedor/otro)", pet['species'], validate_pet_species)
        breed = get_new_val("Raza", pet['breed'], validate_pet_breed)
        gender = get_new_val("Género (macho/hembra)", pet['gender'], validate_pet_gender)
        birth_date = get_new_val("Fecha de Nacimiento", pet['estimated_birth_date'], validate_birth_date)
        weight_kg = get_new_val("Peso en KG", pet['weight_kg'], validate_weight_kg)
        color = get_new_val("Color", pet['color'], validate_pet_color)
        coat = get_new_val("Pelaje", pet['coat'], validate_pet_coat)
        
        has_chip = get_new_bool("¿Tiene Chip? (S/N)", pet['has_chip'])
        
        # Lógica especial para el número de chip
        if has_chip == 1:
            current_chip = pet['chip_number'] if pet['chip_number'] else ""
            chip_input = input(f"Número de Chip [{current_chip}]: ").strip()
            if chip_input == "":
                if current_chip != "":
                    chip_number = current_chip
                else:
                    # Dijo que sí tiene chip pero no escribió nada y antes no tenía
                    chip_number = validate_chip_number("", 1) 
            else:
                chip_number = validate_chip_number(chip_input, 1)
        else:
            chip_number = None

        is_neutered = get_new_bool("¿Está esterilizado? (S/N)", pet['is_neutered'])
        is_alive = get_new_bool("¿Sigue con vida? (S/N)", pet['is_alive'])

        # 3. Inserción de todos los campos (PUT reemplaza todo)
        sql = """
            UPDATE pets SET 
                name = %s, species = %s, breed = %s, gender = %s, 
                estimated_birth_date = %s, weight_kg = %s, color = %s, 
                coat = %s, has_chip = %s, chip_number = %s, 
                is_neutered = %s, is_alive = %s
            WHERE pet_id = %s
        """
        params = (
            name, species, breed, gender, birth_date, weight_kg, 
            color, coat, has_chip, chip_number, is_neutered, is_alive, pet_id
        )
        affected_rows = execute_write_operation(sql, params)

        # 4. Salida JSON
        response = {
            "status": "success",
            "message": "Registro de mascota reemplazado por completo (PUT).",
            "affected_rows": affected_rows
        }
        print(json.dumps(response, indent=2, ensure_ascii=False))

    except ValueError as err:
        print(f"Error de Validación: {err}")
    except Exception as err:
        print(f"Error Interno: {err}")
    finally:
        pause()

if __name__ == "__main__":
    update_pet_completely()
    