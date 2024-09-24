import requests
import base64
import time
import get_token
import constants
import json
import save_data

# Asumiendo que ya tienes el token de acceso
access_token = get_token.get_access_token(constants.client_id, constants.client_secret)

# Información del item que proporcionaste
item_id = "urn:adsk.wipprod:dm.lineage:-za1GgKuTMePbDjBEn8LOQ"
project_id = "b.07de680e-32d8-4411-acaa-3ab60c0b1a02"

def encode_urn(urn):
    return base64.urlsafe_b64encode(urn.encode()).decode().rstrip("=")

def get_latest_version(project_id, item_id):
    url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/items/{item_id}/tip"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['id']
    else:
        print(f"Error obteniendo la última versión: {response.status_code}, {response.text}")
        return None

def start_translation(urn):
    url = "https://developer.api.autodesk.com/modelderivative/v2/designdata/job"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": {"urn": urn},
        "output": {
            "formats": [{"type": "svf", "views": ["2d", "3d"]}]
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def check_translation(urn):
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/manifest"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_metadata(urn):
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_properties(urn, guid):
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata/{guid}/properties"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def extract_specific_properties(properties):
    specific_props = {}
    if 'data' in properties and 'collection' in properties['data']:
        for item in properties['data']['collection']:
            if item['name'] == 'Identity Data':
                for prop in item['properties']:
                    specific_props[prop['name']] = prop['value']
            elif item['name'] == 'Graphics':
                for prop in item['properties']:
                    specific_props[prop['name']] = prop['value']
    return specific_props

def main():
    latest_version = get_latest_version(project_id, item_id)
    if not latest_version:
        return

    urn = encode_urn(latest_version)
    print(f"URN codificado: {urn}")

    translation = start_translation(urn)
    print("Conversión iniciada:", translation)

    while True:
        status = check_translation(urn)
        print("Estado de la conversión:", status['status'])
        if status['status'] == 'success':
            break
        elif status['status'] == 'failed':
            print("La conversión falló.")
            return
        time.sleep(10)

    metadata = get_metadata(urn)
    if 'data' not in metadata or not metadata['data']:
        print("No se encontraron metadatos.")
        return

    for obj in metadata['data']['metadata']:
        if obj['name'] == '{3D}':  # Buscamos específicamente la vista 3D
            properties = get_properties(urn, obj['guid'])
            save_data.save_projects_data(properties, "model_properties", "json")
            specific_props = extract_specific_properties(properties)
            print("\nPropiedades específicas de la vista 3D:")
            for key, value in specific_props.items():
                print(f"{key}: {value}")
            break
    else:
        print("No se encontró la vista 3D en los metadatos.")

if __name__ == "__main__":
    main()