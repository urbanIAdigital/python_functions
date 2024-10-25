import aspose.tasks as tasks
import csv
import os

# Ruta de la carpeta que contiene los archivos .mpp
ruta_carpeta = "C:/Users/juan.carrasquilla/Documents/repos/acc_functions/mppFolder"
ruta_salida_csv = "C:/Users/juan.carrasquilla/Documents/repos/acc_functions/csv_files2"

# Asegúrate de que la carpeta de salida exista, si no, créala
if not os.path.exists(ruta_salida_csv):
    os.makedirs(ruta_salida_csv)

# Función para inspeccionar todos los atributos de una tarea
def ver_atributos_tarea(tarea):
    print(f"Inspectando atributos de la tarea: {tarea.name}")
    
    # Imprimir todas las propiedades estándar de la tarea
    for atributo in dir(tarea):
        if not atributo.startswith("__") and not callable(getattr(tarea, atributo)):
            valor = getattr(tarea, atributo)
            print(f"{atributo}: {valor}")
    
    # Imprimir los campos personalizados (extended_attributes)
    print("Campos personalizados:")
    for atributo in tarea.extended_attributes:
        print(f"{atributo.attribute_definition.field_name}: {atributo.value}")

# Función recursiva para recorrer tareas y subtareas
def recorrer_tareas(tarea, nivel, escritor_csv):
    # Llama a la función para inspeccionar los atributos de la tarea (opcional)
    # ver_atributos_tarea(tarea)

    # Obtener los datos de la tarea
    nombre_tarea = tarea.name
    codigo_bim = obtener_valor_campo_personalizado(tarea, "Text2")  # Usar "Text2" como Código BIM
    unidad = obtener_valor_campo_personalizado(tarea, "UNITS")
    cantidad_ejecutada = tarea.actual_work  # Cantidad ejecutada
    cantidad_programada = tarea.work  # Cantidad programada
    porcentaje_completado = tarea.percent_complete  # % Completado
    comienzo_real = tarea.actual_start  # Comienzo real
    fin_real = tarea.actual_finish  # Fin real
    duracion_real = tarea.duration  # Duración real
    porcentaje_financiero_ejecutado = tarea.cost  # % Financiero ejecutado
    desviacion = tarea.cost_variance  # Desviación

    # Nuevas columnas
    porcentaje_programado = tarea.percent_work_complete  # % Programado
    variacion_finalizacion = tarea.finish_variance  # Variación de finalización
    costo_previsto = tarea.cost  # Costo previsto (puedes ajustar según lo necesites)
    costo_real = tarea.actual_cost  # Costo real

    # Escribir la fila correspondiente en el CSV con el nivel de indentación
    escritor_csv.writerow([
        f"{'  ' * nivel}{nombre_tarea}",
        codigo_bim if codigo_bim else "",  # Verificar si el campo existe
        unidad if unidad else "",  # Verificar si el campo existe
        cantidad_ejecutada,
        cantidad_programada,
        porcentaje_completado,
        comienzo_real,
        fin_real,
        duracion_real,
        porcentaje_financiero_ejecutado,
        desviacion,
        porcentaje_programado,  # Columna adicional
        variacion_finalizacion,  # Columna adicional
        costo_previsto,  # Columna adicional
        costo_real  # Columna adicional
    ])

    # Recorrer las subtareas
    for subtarea in tarea.children:
        recorrer_tareas(subtarea, nivel + 1, escritor_csv)

# Función para obtener el valor de un campo personalizado (modificada para buscar Text2)
def obtener_valor_campo_personalizado(tarea, nombre_campo):
    for atributo in tarea.extended_attributes:
        if atributo.attribute_definition.field_name == nombre_campo:
            return atributo.value
    return None  # Retorna None si no se encuentra el campo

# Función para convertir un archivo .mpp a .csv
def convertir_mpp_a_csv(ruta_mpp, ruta_csv):
    # Cargar el archivo .mpp
    project = tasks.Project(ruta_mpp)

    # Crear y abrir el archivo CSV en modo escritura
    with open(ruta_csv, mode="w", newline="", encoding="utf-8") as archivo_csv:
        # Inicializar el writer para CSV
        escritor_csv = csv.writer(archivo_csv)

        # Escribir la cabecera del CSV
        escritor_csv.writerow([
            "Tarea", 
            "Código BIM", 
            "Unidad", 
            "Cantidad Ejecutada", 
            "Cantidad Programada", 
            "% Completado", 
            "Comienzo Real", 
            "Fin Real", 
            "Duración Real", 
            "% Financiero Ejecutado", 
            "Desviación (%)",
            "% Programado",  # Nueva columna
            "Variación de Finalización",  # Nueva columna
            "Costo Previsto",  # Nueva columna
            "Costo Real"  # Nueva columna
        ])

        # Recorrer todas las tareas principales y sus subtareas
        for task in project.root_task.children:
            recorrer_tareas(task, 0, escritor_csv)  # Nivel 0 para las tareas principales

# Recorrer todos los archivos .mpp en la carpeta
for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith(".mpp"):
        ruta_mpp = os.path.join(ruta_carpeta, archivo)
        # Generar una ruta para el archivo CSV de salida, cambiando la extensión de .mpp a .csv
        nombre_archivo_csv = os.path.splitext(archivo)[0] + ".csv"
        ruta_csv = os.path.join(ruta_salida_csv, nombre_archivo_csv)

        # Llamar a la función de conversión para cada archivo .mpp
        convertir_mpp_a_csv(ruta_mpp, ruta_csv)

print(
    f"Todos los archivos .mpp en {ruta_carpeta} han sido convertidos a CSV y guardados en {ruta_salida_csv}"
)
