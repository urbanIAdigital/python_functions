import requests

def get_access_token(client_id, client_secret):
    url = 'https://developer.api.autodesk.com/authentication/v2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': 'data:read data:write bucket:read bucket:create viewables:read account:read'
    }
    response = requests.post(url, headers=headers, data=data)
    token_info = response.json()
    access_token = token_info['access_token']
    return access_token
