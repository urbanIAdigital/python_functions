import json
from mpxj import MPXJProject

def mpp_to_json(mpp_file_path, json_file_path):
    # Cargar el archivo .mpp
    project = MPXJProject()
    project.read(mpp_file_path)

    # Extraer la información del proyecto
    project_data = {
        "name": project.get_project_properties().get_name(),
        "start_date": str(project.get_project_properties().get_start_date()),
        "end_date": str(project.get_project_properties().get_finish_date()),
        "tasks": []
    }

    # Extraer información de las tareas
    for task in project.get_tasks():
        task_data = {
            "id": task.get_id(),
            "name": task.get_name(),
            "start_date": str(task.get_start()),
            "end_date": str(task.get_finish()),
            "duration": str(task.get_duration()),
            "percent_complete": task.get_percent_complete()
        }
        project_data["tasks"].append(task_data)

    # Guardar la información en un archivo JSON
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(project_data, json_file, ensure_ascii=False, indent=4)

# Uso de la función
mpp_file_path = "C:/Users/juan.carrasquilla/Documents/repos/fastapi/proyect2.mpp"
output_json_path = "C:/Users/juan.carrasquilla/Documents/repos/fastapi/output.json"
mpp_to_json(mpp_file_path, output_json_path)