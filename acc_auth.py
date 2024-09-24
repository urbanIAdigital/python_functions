import requests
import json
import urllib.parse
import save_data
import get_token
import constants
import os

access_token = get_token.get_access_token(constants.client_id, constants.client_secret)

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}
# hub_id = "b.36666791-130f-4c46-ab3a-f7369f5c7c81"

def get_project_id_by_name(project_name):

    current_directory = os.path.dirname(os.path.abspath(__file__))

    json_file_path = os.path.join(current_directory, 'projects_data.json')
    try:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo 'projects_data.json' en {current_directory}")
        return None
    except json.JSONDecodeError:
        print("Error: El archivo 'projects_data.json' no contiene un JSON válido")
        return None
    for project in json_data['data']:
        if project['attributes']['name'] == project_name:
            return project['id']
    return None

def get_projects_hub():

    url = "https://developer.api.autodesk.com/project/v1/hubs"

    response = requests.get(url, headers=headers)
    projects = response.json()
    print(f" hubs en ACC {projects["data"][0]["id"]}")
    return projects["data"][0]["id"]

def simplify_json(json_data):

    data_list = json_data['data']

    simplified_data = []
    
    for item in data_list:
        simplified_item = {
            'name': item['attributes']['name'],
            'id': item['id'],
            'type': item['type']
        }
        simplified_data.append(simplified_item)
    simplified_json = {'data': simplified_data}
    
    return simplified_json


def get_projects_list():
    hub_id = get_projects_hub()
    projects_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects"

    response2 = requests.get(projects_url, headers=headers)

    projects_data = response2.json()
    print(f"numero de projectos en ACC {len(projects_data["data"])}")
    save_data.save_projects_data(projects_data, "projects_data", "json")
    
    return projects_data

# project_id = "b.07de680e-32d8-4411-acaa-3ab60c0b1a02"
folder_id = "urn:adsk.wipprod:fs.folder:co.acSfkHVVRUubjgp_Tb0WGA"

def get_folders_list():
    hub_id = get_projects_hub()
    project_id = get_project_id_by_name(constants.project_name)
    print(project_id)
    folder_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
    response = requests.get(folder_url, headers=headers)
    if response.status_code == 200:
        folders_data = response.json()
        save_data.save_projects_data(folders_data, "folders_data", "json")
        return folders_data
    else:
        print(f"Error: {response.status_code} - {response.text}")
# get_folders_list()
   
def get_content_folder():
    project_id = get_project_id_by_name(constants.project_name)
    contents_url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents"
    response = requests.get(contents_url, headers=headers)
    contents = response.json()["data"]
    save_data.save_projects_data(contents, "contents", "json")
    return contents

get_content_folder()

    

item_id = "urn:adsk.wipprod:dm.lineage:7Vmj1aF7RniLgiwv357NRw"

def get_item_details():
    project_id = get_project_id_by_name(constants.project_name)
    tip_url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/items/{item_id}/tip"
    response = requests.get(tip_url, headers=headers)
    tip_data = response.json()["data"]
    print(json.dumps(response.json(), indent=2))
    version_id = tip_data["id"]
    encoded_version_id = urllib.parse.quote(version_id, safe="")

    print(f"Version ID: {encoded_version_id}")
    version_url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/versions/{encoded_version_id}"
    response = requests.get(version_url, headers=headers)

    if response.status_code != 200:
        print(
            f"Error al obtener los detalles de la versión. Código de estado: {response.status_code}"
        )
        print(response.text)
    else:
        version_data = response.json()["data"]
        if "relationships" in version_data and "storage" in version_data["relationships"]:
            download_url = version_data["relationships"]["storage"]["meta"]["link"]["href"]
            file_response = requests.get(download_url, headers=headers)
            if file_response.status_code == 200:
                filename = "ConsultaSeven_20240910.geojson"
                with open(filename, "wb") as file:
                    file.write(file_response.content)
                print(f"Archivo '{filename}' descargado con éxito.")
            else:
                print(
                    f"Error al descargar el archivo. Código de estado: {file_response.status_code}"
                )
                print(file_response.text)
        else:
            print("No se pudo encontrar el enlace de descarga en los datos de la versión.")
            print(version_data)

