import json
import os
import pandas as pd


def simplify_json(json_data):
    # Extraer la lista de datos del JSON
    data_list = json_data["data"]

    # Crear una lista para almacenar los datos simplificados
    simplified_data = []

    for item in data_list:
        simplified_item = {
            "name": item["attributes"]["name"],
            "id": item["id"],
            "type": item["type"],
            "latitude": "",	
            "longitude": "",	
        }
        simplified_data.append(simplified_item)

    # Crear el nuevo JSON simplificado
    simplified_json = {"data": simplified_data}

    return pd.DataFrame(simplified_json)


# Obtener la ruta del directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta completa al archivo JSON
json_file_path = os.path.join(current_directory, "projects_data.json")

# Leer el archivo JSON
try:
    with open(json_file_path, "r") as file:
        json_data = json.load(file)
except FileNotFoundError:
    print(
        f"Error: No se pudo encontrar el archivo 'projects_data.json' en {current_directory}"
    )
    exit(1)
except json.JSONDecodeError:
    print("Error: El archivo 'projects_data.json' no contiene un JSON válido")
    exit(1)

# Llamar a la función y obtener el JSON simplificado
simplified_json = simplify_json(json_data)

print(simplified_json.head)
# Opcionalmente, guardar el JSON simplificado en un nuevo archivo
output_file_path = os.path.join(current_directory, "simplified_projects_data.json")
with open(output_file_path, "w") as file:
    json.dump(simplified_json, file, indent=2)

print(f"\nEl JSON simplificado se ha guardado en: {output_file_path}")
