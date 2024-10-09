import aspose.tasks as tasks
import csv

# Ruta del archivo .mpp
ruta_mpp = "C:/Users/juan.carrasquilla/Documents/repos/fastapi/proyect2.mpp"
ruta_csv = "C:/Users/juan.carrasquilla/Documents/repos/fastapi/proyect2.csv"

# Función recursiva para recorrer tareas y subtareas
def recorrer_tareas(tarea, nivel, escritor_csv):
    # Obtener los datos de la tarea
    nombre_tarea = tarea.name
    inicio_tarea = tarea.start
    fin_tarea = tarea.finish

    # Escribir la fila correspondiente en el CSV con el nivel de indentación
    escritor_csv.writerow([f"{'  ' * nivel}{nombre_tarea}", inicio_tarea, fin_tarea])

    # Recorrer las subtareas
    for subtarea in tarea.children:
        recorrer_tareas(subtarea, nivel + 1, escritor_csv)

# Cargar el archivo .mpp
project = tasks.Project(ruta_mpp)

# Crear y abrir el archivo CSV en modo escritura
with open(ruta_csv, mode='w', newline='', encoding='utf-8') as archivo_csv:
    # Inicializar el writer para CSV
    escritor_csv = csv.writer(archivo_csv)

    # Escribir la cabecera del CSV
    escritor_csv.writerow(['Tarea', 'Inicio', 'Fin'])

    # Recorrer todas las tareas principales y sus subtareas
    for task in project.root_task.children:
        recorrer_tareas(task, 0, escritor_csv)  # Nivel 0 para las tareas principales

print(f'Las tareas y subtareas han sido exportadas a {ruta_csv}')