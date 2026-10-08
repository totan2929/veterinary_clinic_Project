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

from database.db_connection import execute_write_operation_returning_id, execute_single_query
from utils.functions import (
    clear_screen, pause, validate_doc_number, validate_pet_name, 
    validate_pet_species, validate_weight_kg, validate_boolean_yn, validate_chip_number,
    validate_pet_breed, validate_pet_gender, validate_birth_date, validate_pet_color, validate_pet_coat
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

        # 2. Captura de todos los datos obligatorios
        name = validate_pet_name(input("Nombre de la mascota: "))
        species = validate_pet_species(input("Especie (perro/gato/ave/reptil/roedor/otro): "))
        breed = validate_pet_breed(input("Raza: "))
        gender = validate_pet_gender(input("Género (macho/hembra): "))
        birth_date = validate_birth_date(input("Fecha de nac. estimada (AAAA-MM-DD): "))
        weight_kg = validate_weight_kg(input("Peso en KG (Ej: 12.5): "))
        color = validate_pet_color(input("Color: "))
        coat = validate_pet_coat(input("Tipo de pelaje (Ej: Corto, Largo): "))
        
        has_chip_input = validate_boolean_yn(input("¿Tiene Chip? (S/N): "))
        chip_number = None
        if has_chip_input == 1:
            chip_number = validate_chip_number(input("Número de Chip: "), has_chip_input)

        is_neutered = validate_boolean_yn(input("¿Está esterilizado? (S/N): "))
        is_alive = 1 # Por defecto está viva al registrarse

        # 3. Inserción con todos los campos
        sql = """
            INSERT INTO pets (
                owner_id, name, species, breed, gender, estimated_birth_date, 
                weight_kg, color, coat, has_chip, chip_number, is_neutered, is_alive
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            owner_id, name, species, breed, gender, birth_date, 
            weight_kg, color, coat, has_chip_input, chip_number, is_neutered, is_alive
        )
        affected_rows, new_pet_id = execute_write_operation_returning_id(sql, params)

        # 4. Salida
        response = {
            "status": "success",
            "message": "Mascota registrada exitosamente",
            "data": {"pet_id": new_pet_id, "name": name, "  owner_id": owner_id, "species": species, "breed": breed, "gender": gender, "estimated_birth_date": birth_date, "weight_kg": weight_kg, "color": color, "coat": coat, "has_chip": has_chip_input, "chip_number": chip_number, "is_neutered": is_neutered, "is_alive": is_alive}
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