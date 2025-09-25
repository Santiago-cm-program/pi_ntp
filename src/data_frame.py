import requests
import pandas as pd

#URL de la Appi
url = "https://playground.mockoon.com/users"

try :
    response = requests.get(url)
    response.raise_for_status()  # Verifica si la solicitud fue exitosa
    data = response.json()  # Asumiendo que la respuesta es JSON
    df = pd.DataFrame(data)
    
    df.to_csv("mockoon_users.csv", index=False)
    print("Datos guardados en 'mockoon_users.csv'")
    

    
except requests.exceptions.HTTPError as http_err:
    print(f"Error HTTP: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Error de conexión: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Error de timeout: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"Error en la solicitud: {req_err}")
except ValueError as json_err:
    print(f"Error al procesar JSON: {json_err}")