import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

redirect_uri = 'https://github.com/NathanielMekonen'
scope = 'user-read-recently-played'
auth_url = 'https://accounts.spotify.com/authorize'
auth_params = {
    'client_id': client_id,
    'response_type': 'code',
    'redirect_uri': redirect_uri,
    'scope': scope
}

# Use the URL below to authorize the app, obtain the authentication code, and store it in .env
print(f"{auth_url}?{urllib.parse.urlencode(auth_params)}")
