# ============================================================================
# FILE: utils/functions.py
# LAYER: 3 - Business Logic and Domain Validators
# ============================================================================
import os
import re
from datetime import datetime

# --- UTILITIES ---
def clear_screen():
    """Limpia la pantalla de la terminal."""
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    """Pausa la ejecución hasta que el usuario presione una tecla."""
    print("\nPresione cualquier tecla para continuar...")
    if os.name == "nt":
        os.system("pause > nul")
    else:
        os.system("read -n 1 -s -r -p ''")
        print()
    clear_screen()

# --- VALIDATORS (OWNERS) ---
def validate_doc_type(doc_type):
    valid_types = ("CC", "CE", "TI", "PASAPORTE", "PASSPORT")
    candidate = str(doc_type).strip().upper()
    if candidate not in valid_types:
        raise ValueError(f"Tipo de documento inválido. Opciones: {', '.join(valid_types)}.")
    return candidate

def validate_doc_number(doc_number):
    pattern = r"^[A-Za-z0-9]{5,20}$"
    candidate = str(doc_number).strip()
    if not re.fullmatch(pattern, candidate):
        raise ValueError("Documento inválido. Debe ser alfanumérico de 5 a 20 caracteres.")
    return candidate

def validate_person_name(name):
    pattern = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,80}$"
    candidate = str(name).strip()
    if not re.fullmatch(pattern, candidate):
        raise ValueError("Nombre inválido. Solo letras y espacios (2 a 80 caracteres).")
    return candidate

def validate_phone(phone):
    pattern = r"^\d{10}$"
    candidate = str(phone).strip()
    if not re.fullmatch(pattern, candidate):
        raise ValueError("Teléfono inválido. Debe contener exactamente 10 dígitos.")
    return candidate

def validate_email(email):
    pattern = r"^(?=.{10,70}$)[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,6}$"
    candidate = str(email).strip().lower()
    if not re.fullmatch(pattern, candidate):
        raise ValueError("Correo electrónico inválido.")
    return candidate

def validate_status(status):
    valid_statuses = ("Active", "Inactive")
    candidate = str(status).strip().capitalize()
    if candidate not in valid_statuses:
        raise ValueError(f"Estado inválido. Opciones: {', '.join(valid_statuses)}.")
    return candidate

# --- 5 NUEVAS FUNCIONES PROPIAS (VALIDATORS PARA PETS) ---

def validate_pet_species(species):
    """1. Valida que la especie sea una de las permitidas en la clínica."""
    valid_species = ("perro", "gato", "ave", "reptil", "roedor", "otro")
    candidate = str(species).strip().lower()
    if candidate not in valid_species:
        raise ValueError(f"Especie inválida. Opciones: {', '.join(valid_species)}")
    return candidate

def validate_weight_kg(weight):
    """2. Valida que el peso sea un número decimal lógico (0.1 a 150.0 kg)."""
    try:
        candidate = float(str(weight).strip())
        if not (0.1 <= candidate <= 150.0):
            raise ValueError("El peso debe estar entre 0.1 y 150.0 kg.")
        return round(candidate, 2)
    except ValueError:
        raise ValueError("El peso debe ser un número decimal válido.")

def validate_boolean_yn(value):
    """3. Convierte una entrada S/N (Sí/No) en 1 o 0 para base de datos."""
    candidate = str(value).strip().upper()
    if candidate == 'S':
        return 1
    elif candidate == 'N':
        return 0
    else:
        raise ValueError("Entrada inválida. Digite 'S' para Sí o 'N' para No.")

def validate_pet_name(name):
    """4. Valida nombres de mascotas, permitiendo números (ej: Max 2)."""
    pattern = r"^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ ]{2,60}$"
    candidate = str(name).strip()
    if not re.fullmatch(pattern, candidate):
        raise ValueError("Nombre de mascota inválido. Use letras o números (2-60 caracteres).")
    return candidate

def validate_chip_number(chip, has_chip):
    """5. Valida el número de chip solo si la mascota tiene uno."""
    if has_chip == 0:
        return None # No tiene chip, devolvemos nulo
    pattern = r"^[A-Za-z0-9]{9,15}$"
    candidate = str(chip).strip()
    if not re.fullmatch(pattern, candidate):
        raise ValueError("Chip inválido. Debe ser alfanumérico entre 9 y 15 caracteres.")
    return candidate
