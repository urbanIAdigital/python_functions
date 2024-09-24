import json
def save_projects_data(projects_data, file_name, file_type="json"):
    """
    Guarda la respuesta JSON en un archivo.

    :param projects_data: Diccionario con los datos del proyecto.
    :param file_name: Nombre del archivo sin la extensión.
    :param file_type: Tipo de archivo a guardar ('json' o 'txt').
    """
    if file_type == "json":
        file_path = f"{file_name}.json"
        with open(file_path, "w") as file:
            json.dump(projects_data, file, indent=4)
    elif file_type == "txt":
        file_path = f"{file_name}.txt"
        with open(file_path, "w") as file:
            file.write(json.dumps(projects_data, indent=4))
    else:
        raise ValueError("Tipo de archivo no soportado. Usa 'json' o 'txt'.")

    print(f"Archivo guardado en: {file_path}")
