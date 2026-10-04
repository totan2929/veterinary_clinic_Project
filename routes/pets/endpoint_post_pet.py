import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.db_connection import execute_write_operation_returning_id, execute_single_query
from utils.functions import (
    clear_screen, pause, validate_doc_number, validate_pet_name, 
    validate_pet_species, validate_weight_kg, validate_boolean_yn, validate_chip_number
)

def create_pet():
    clear_screen()
    try:
        # 1. Vincular al propietario
        doc_input = input("Documento del Propietario (Dueño): ")
        doc_number = validate_doc_number(doc_input)
        
        owner = execute_single_query("SELECT owner_id FROM owners WHERE doc_number = %s", (doc_number,))
        if not owner:
            raise ValueError("El propietario no existe. Debe registrarlo primero.")
        owner_id = owner['owner_id']

        # 2. Captura de datos de la mascota usando TUS 5 FUNCIONES NUEVAS
        name = validate_pet_name(input("Nombre de la mascota: "))
        species = validate_pet_species(input("Especie (perro/gato/ave/reptil/roedor/otro): "))
        weight_kg = validate_weight_kg(input("Peso en KG (Ej: 12.5): "))
        
        has_chip_input = validate_boolean_yn(input("¿Tiene Chip? (S/N): "))
        chip_number = None
        if has_chip_input == 1:
            chip_number = validate_chip_number(input("Número de Chip: "), has_chip_input)

        is_neutered = validate_boolean_yn(input("¿Está esterilizado? (S/N): "))
        is_alive = 1 # Por defecto al crear una mascota, asumimos que está viva

        # 3. Inserción
        sql = """
            INSERT INTO pets (owner_id, name, species, weight_kg, has_chip, chip_number, is_neutered, is_alive)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (owner_id, name, species, weight_kg, has_chip_input, chip_number, is_neutered, is_alive)
        affected_rows, new_pet_id = execute_write_operation_returning_id(sql, params)

        # 4. Salida
        response = {
            "status": "success",
            "message": "Mascota registrada exitosamente",
            "data": {"pet_id": new_pet_id, "name": name}
        }
        print(json.dumps(response, indent=2, ensure_ascii=False))

    except ValueError as validation_err:
        print(f"Error de Validación: {validation_err}")
    except Exception as general_err:
        print(f"Error Interno: {general_err}")
    finally:
        pause()

if __name__ == "__main__":
    create_pet()
