import requests
import get_token
import constants

def set_webhook():
    try:
        access_token = get_token.get_access_token(constants.client_id, constants.client_secret)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        url = "https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks"

        payload = {
            "callbackUrl": "https://eor0n13bztpnupm.m.pipedream.net",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.acSfkHVVRUubjgp_Tb0WGA"
            }
        }

        response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP no exitosos

        print(f"Código de estado: {response.status_code}")
        print("Respuesta JSON:")
        print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")