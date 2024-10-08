import pandas as pd
import json


def excel_to_json(file_path, output_json_path):
    # Cargar el archivo Excel en un DataFrame de pandas
    df = pd.read_excel(file_path)

    # Convertir el DataFrame a JSON
    json_data = df.to_json(orient="records", force_ascii=False)

    # Guardar el JSON en la ruta especificada
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(json.loads(json_data), json_file, ensure_ascii=False, indent=4)

    print(f"Archivo JSON guardado en: {output_json_path}")


# Ejemplo de uso
file_path = "C:/Users/juan.carrasquilla/OneDrive - EDU/Descargas/IE_Base_20240930.xlsx"
output_json_path = "C:/Users/juan.carrasquilla/Documents/repos/contrato-interadministrativo/src/constants/data_resp.json"

excel_to_json(file_path, output_json_path)
