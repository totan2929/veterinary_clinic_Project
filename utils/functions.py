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

# --- VALIDATORS (PETS) ---

def validate_pet_species(species):
    """1. Valida que la especie sea permitida y la mapea al inglés para la BD."""
    species_map = {
        "perro": "dog",
        "gato": "cat",
        "ave": "bird",
        "reptil": "reptile",
        "roedor": "rodent",
        "otro": "other"
    }
    candidate = str(species).strip().lower()
    if candidate not in species_map:
        raise ValueError(f"Especie inválida. Opciones: {', '.join(species_map.keys())}")
    return species_map[candidate]

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
        return None
    pattern = r"^[A-Za-z0-9]{9,15}$"
    candidate = str(chip).strip()
    if not re.fullmatch(pattern, candidate):
        raise ValueError("Chip inválido. Debe ser alfanumérico entre 9 y 15 caracteres.")
    return candidate

def validate_pet_gender(gender):
    """Valida el género y lo mapea al inglés para la BD."""
    gender_map = {
        "macho": "male",
        "hembra": "female"
    }
    candidate = str(gender).strip().lower()
    if candidate not in gender_map:
        raise ValueError(f"Género inválido. Opciones: {', '.join(gender_map.keys())}")
    return gender_map[candidate]

def validate_pet_breed(breed):
    """Valida la raza (alfanumérico, 2-60 caracteres)."""
    pattern = r"^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ ]{2,60}$"
    candidate = str(breed).strip()
    if not re.fullmatch(pattern, candidate):
        raise ValueError("Raza inválida. Use letras o números (2-60 caracteres).")
    return candidate

def validate_pet_color(color):
    """Valida el color de la mascota (permite letras, espacios y guiones)."""
    pattern = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ \-]{2,50}$"
    candidate = str(color).strip()
    if not re.fullmatch(pattern, candidate):
        raise ValueError("Color inválido. Use letras y guiones (2-50 caracteres).")
    return candidate

def validate_pet_coat(coat):
    """Valida el tipo de pelaje."""
    pattern = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,50}$"
    candidate = str(coat).strip()
    if not re.fullmatch(pattern, candidate):
        raise ValueError("Pelaje inválido. Solo use letras (2-50 caracteres).")
    return candidate

def validate_birth_date(date_str):
    """Valida que la fecha tenga el formato AAAA-MM-DD y no sea futura."""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    candidate = str(date_str).strip()
    if not re.fullmatch(pattern, candidate):
        raise ValueError(
            "El dato ingresado no tiene la estructura requerida. "
            "La fecha debe cumplir el formato estricto AAAA-MM-DD (ej: 1994-06-15)."
        )
    try:
        parsed_date = datetime.strptime(candidate, "%Y-%m-%d").date()
        if parsed_date > datetime.now().date():
            raise ValueError(
                "El dato ingresado no tiene la estructura requerida. "
                "La fecha de nacimiento no puede ser futura."
            )
        return candidate
    except ValueError as err:
        raise ValueError(f"Día o mes no válido en el calendario real: {err}")

def confirm_action_yn(prompt):
    """Pide confirmación de seguridad (Sí/No) al usuario antes de acciones destructivas."""
    while True:
        response = input(f"{prompt} (S/N): ").strip().upper()
        if response in ('S', 'SI', 'Y', 'YES'):
            return True
        elif response in ('N', 'NO'):
            return False
        print("Entrada inválida. Por favor, ingrese 'S' para Sí o 'N' para No.")