from curses import init_pair
import requests
from dotenv import load_dotenv, find_dotenv
import os
from fuzzywuzzy import fuzz
import json
from typing import Tuple
from tqdm import tqdm
import spotipy
from spotipy.oauth2 import SpotifyOAuth

AUTH_URL = "https://accounts.spotify.com/api/token"
SEARCH_API = "https://api.spotify.com/v1/search"

def init_spotipy():
    load_dotenv(find_dotenv())
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp

def get_spotify_artist(artist_name: str, sp: spotipy.Spotify, limit: int = 10):
    artists = sp.search(artist_name, limit=limit, type="artist")["artists"]["items"]
    # Creating similarity score for artist
    for artist in artists:
        artist["sim_score"] = fuzz.ratio(artist["name"].lower(), artist_name.lower())
        artist["id"] = artist["uri"].split(":")[-1]

    if len(artists) < 1:
        return None
    
    # Sorting artists based on how similar the spotify name is to the artist name.
    # Similarity is done in probability.
    # Percentage can be tweaked, but 99% seems like a good assumption
    most_similar = max(artists, key=lambda x: x["sim_score"])
    if most_similar["sim_score"] < 99:
        return None
    else:
        return most_similar

def find_most_popular_track(artist_id: str, sp: spotipy.Spotify, country="DK", number_ranking = 0) -> str:
    tracks = sp.artist_top_tracks(artist_id, country=country)["tracks"]
    if len(tracks) < 1:
        print(artist_id)
        return
    return tracks[number_ranking]["uri"]

if __name__ == "__main__":
    sp = init_spotipy()
    with open("data/artists.json", "r") as f:
        artist_names = json.load(f)

    spotify_artists = []
    not_found = []
    
    print("Finding artists on spotify")
    for name in tqdm(artist_names):
        spotify_artist = get_spotify_artist(name, sp)
        if spotify_artist is None:
            not_found.append(name)
        else:
            spotify_artists.append(spotify_artist)

    with open("data/spotify_artists.json", "w") as f:
        json.dump(spotify_artists, f, indent=2)
    
    with open("data/artists_not_found.json", "w") as f:
        json.dump(not_found, f, indent=2)
    
    with open("data/spotify_artists.json", "r") as f:
        spotify_artists = json.load(f)

    print("Finding most popular tracks")
    tracks = []
    for artist in tqdm(spotify_artists):
        track = find_most_popular_track(artist["id"], sp)
        if track is not None:
            tracks.append(track)

    playlist_id = os.getenv("PLAYLIST_ID")
    print(f"Adding tracks to playlist: {playlist_id}")
    chunk_size = 100
    chunked_list = [tracks[i:i+chunk_size] for i in range(0, len(tracks), chunk_size)]
    for chunk in tqdm(chunked_list):
        sp.playlist_add_items(playlist_id, chunk)
    