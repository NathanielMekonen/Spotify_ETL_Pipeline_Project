import os
import base64
from datetime import time
import time
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
refresh_token = os.getenv('REFRESH_TOKEN')
db_username = os.getenv('USERNAME')
db_password = os.getenv('PASSWORD')
db_host = os.getenv('HOST')
db_port = os.getenv('PORT')
db_name = os.getenv('DATABASE')

spotify_token_url = 'https://accounts.spotify.com/api/token'
spofity_recently_played_url = 'https://api.spotify.com/v1/me/player/recently-played'
spotify_artist_url = 'https://api.spotify.com/v1/artists/'

def get_new_token():
    """Request a new Spotify access token using the refresh token."""
    auth_string = os.getenv('CLIENT_ID') + ':' + os.getenv('CLIENT_SECRET')
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    headers = {
        'Authorization' : f'Basic {auth_base64}',
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token,
        'client_id' : client_id
    }
    result = requests.post(spotify_token_url, headers=headers, data=data)
    json_result = result.json()
    access_token = json_result['access_token']
    if not access_token:
        raise RuntimeError("Failed to retrieve the access token")
    return access_token


def get_auth_header(access_token):
    """Return the authorization header dictionary."""
    return {'Authorization' : f'Bearer {access_token}'}


def extract_recently_played_tracks(access_token):
    """Extract recently played tracks for the past 12 hours."""
    timestamp_ms_12hrsago = int((time.time() - 12 * 60 * 60) * 1000)
    params = {
        'limit' : '50',
        'after' : timestamp_ms_12hrsago
    }
    headers = get_auth_header(access_token)
    result = requests.get(spofity_recently_played_url, params=params, headers=headers)
    json_result = result.json()
    print(f'Successfully extracted your last {len(json_result['items'])} played tracks!')
    return json_result


def extract_artist_image(artist_id, access_token):
    """Extract artist image URL for given artist id."""
    url = f'{spotify_artist_url}{artist_id}'
    headers = get_auth_header(access_token)
    result = requests.get(url, headers=headers)
    json_result = result.json()
    return json_result['images'][0]['url']


def get_artist_image(df, access_token):
    """Map artist ids to the artist image URLs."""
    artist_ids = df['artist_id'].unique()
    artist_image_map = {}
    for x in artist_ids:
        try:
            artist_image_map[x] = extract_artist_image(x, access_token)
        except:
            artist_image_map[x] = None
    return artist_image_map


def transform(data, access_token):
    """Transform raw Spotify data into a cleaned DataFrame."""
    if not data.get('items'):
        print('No data was present in the extract step.')
        return None

    df = pd.json_normalize(data['items'], sep='_')

    # Extract artist names and the first artist ID
    df['artists'] = df['track_artists'].apply(lambda x: ', '.join(artist['name'] for artist in x))
    df['artist_id'] = df['track_artists'].apply(lambda x: [artist['id'] for artist in x][0])

    # Extract album cover URL
    df['track_album_images'] = df['track_album_images'].apply(lambda x: x[0]['url'] if x else None)

    # Create a unique play ID
    df['play_id'] = df['track_id'] + '_' + pd.to_datetime(df['played_at']).dt.strftime('%Y-%m-%d_%H:%M:%S')

    # Convert duration from ms to seconds
    df['track_length_seconds'] = df['track_duration_ms'] / 1000

    # Convert the album release dates to datetimes
    df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'], errors='coerce')

    # Convert played_at to US/Central timezone and format string
    df['played_at'] = pd.to_datetime(df['played_at'], utc=True).dt.tz_convert('US/Central').dt.strftime('%Y-%m-%d %H:%M:%S')

    cleaned_df = df[['play_id', 'track_id', 'track_name', 'track_length_seconds', 'track_popularity', 'played_at', 'context_type', 'track_album_name', 'track_album_images', 'track_album_album_type', 'track_album_release_date', 'artists', 'artist_id']]\
                    .rename(columns={
                        'track_album_name' : 'album', 
                        'track_album_images' : 'album_cover',
                        'track_album_album_type' : 'album_type',
                        'track_album_release_date' : 'album_release_date', 
                    })
    
    # Add artist images
    artist_image_map = get_artist_image(cleaned_df, access_token)
    cleaned_df['artist_image'] = cleaned_df['artist_id'].map(artist_image_map)

    print('Successfully cleaned and transformed the data!')
    return cleaned_df


def load(data):
    """Load data into PostgreSQL database."""
    if data is None or data.empty:
        print('No data was loaded into the database.')
        return
    try:
        engine = create_engine(f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
        data.to_sql('most_recently_played_songs', engine, if_exists='append', index=False)
        print('Successfully loaded the data into the database!')
    except Exception as e:
        print(f'Error during data load: {str(e)}')


def main():
    access_token = get_new_token()
    extracted_data = extract_recently_played_tracks(access_token)
    cleaned_data = transform(extracted_data, access_token)
    load(cleaned_data)


if __name__ == "__main__":
    main()
