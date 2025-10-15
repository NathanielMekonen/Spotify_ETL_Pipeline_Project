import os
import requests
from dotenv import load_dotenv
import base64
import json
import authentication_code as ac

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
auth_code = os.getenv('AUTH_CODE')

# Encode the Client ID and Client Secret
auth_string = client_id + ':' + client_secret
auth_bytes = auth_string.encode('utf-8')
auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

# Make a POST request to get the refresh token and store it in .env
token_url = 'https://accounts.spotify.com/api/token'
token_headers = {
    'Authorization' : f'Basic {auth_base64}',
    'Content-Type' : 'application/x-www-form-urlencoded'
}
token_data = {
    'grant_type' : 'authorization_code',
    'code' : auth_code,
    'redirect_uri' : ac.redirect_uri
}
result = requests.post(token_url, headers=token_headers, data=token_data)
json_result = json.loads(result.content)
print(json_result['refresh_token'])