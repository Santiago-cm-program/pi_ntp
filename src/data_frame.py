import pandas as pd
import requests

# URL de la API
url = "https://playground.mockoon.com/users"

def get_users_data():
    """Consume la API y retorna un DataFrame de usuarios."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        return df
    except requests.exceptions.RequestException as e:
        # En una aplicación real, usarías st.error, pero aquí para un script simple, print es suficiente
        print(f"Error al consumir la API: {e}")
    except ValueError as e:
        print(f"Error al decodificar el JSON: {e}")

    return pd.DataFrame() # Retorna un DataFrame vacío en caso de error