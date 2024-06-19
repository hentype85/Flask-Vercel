import os
import json


def lst_users_data():
    json_folder = "./data"
    lst_users = []
    # verificar si el directorio existe
    if not os.path.exists(json_folder):
        print(f"Directory {json_folder} does not exist")
        return lst_users

    # iterar sobre cada archivo en la carpeta
    for archivo in os.listdir(json_folder):
        if archivo.endswith(".json"):
            ruta_archivo = os.path.join(json_folder, archivo)

            try:
                # abrir y cargar el contenido del archivo JSON
                with open(ruta_archivo, 'r') as f:
                    datos_json = json.load(f)
                    lst_users.append(datos_json)
            except json.JSONDecodeError as e:
                print(f"Error loading JSON file {ruta_archivo}: {str(e)}")
            except OSError as e:
                print(f"Error opening file {ruta_archivo}: {str(e)}")

    return lst_users
