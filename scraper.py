from unittest.main import main
import requests
from dotenv import load_dotenv, find_dotenv
import os
from urllib import parse

AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1/"

def autherise_spotify(cli_id: str, cli_secret: str):

    auth_response = requests.post(AUTH_URL, {
        'grant_type': "client_credentials",
        "client_id": cli_id,
        "client_secret": cli_secret
    })

    auth_response_data = auth_response.json()
    access_token = auth_response_data["access_token"]

    return access_token

def get_artist_id(artist_name: str, token: str):
    

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    token = autherise_spotify(client_id, client_secret)

