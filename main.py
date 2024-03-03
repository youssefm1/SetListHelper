from ast import dump
from flask import Flask, redirect, request, session, url_for, render_template
import requests
import base64
import os
from itertools import groupby, combinations
import pdb
import streamlit as st

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify API credentials
CLIENT_ID = 'abc'
CLIENT_SECRET = 'abc'
REDIRECT_URI = 'http://localhost:5000/callback'  # Update with your redirect URI

# Spotify API endpoints
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    # Redirect to Spotify authorization
    return redirect(f'{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=user-read-private user-read-email')

@app.route('/callback')
def callback():
    # Handle Spotify callback and get access token
    code = request.args.get('code')
    auth = (CLIENT_ID, CLIENT_SECRET)
    token_data = requests.post(SPOTIFY_TOKEN_URL, data={'code': code, 'redirect_uri': REDIRECT_URI, 'grant_type': 'authorization_code'}, auth=auth).json()

    # Store token in session (in production, consider using a secure session management solution)
    session['token'] = token_data['access_token']

    return "Authentication successful! You can now make requests to the Spotify API.     " + str(session['token'])

@app.route('/get_profile')
def get_profile():
    # Example endpoint to get the user's profile information
    headers = {'Authorization': f'Bearer {session["token"]}'}
    profile_data = requests.get(f'{SPOTIFY_API_BASE_URL}me', headers=headers).json()

    return profile_data


@app.route('/audio-features/<playlist_id>')
def audio_features(playlist_id):
    if 'token' not in session:
        return redirect(url_for('index'))
    headers = {'Authorization': f'Bearer {session["token"]}'}

    playlist_response = requests.get(f'{SPOTIFY_API_BASE_URL}playlists/{playlist_id}?fields=tracks.items(track(name,id))', headers=headers).json()
    #array to hold song
    tracks = playlist_response["tracks"]["items"]
    track_ids = [item["track"]["id"] for item in playlist_response["tracks"]["items"]]
    track_param = ','.join(track_ids)
    track_features_response = requests.get(f'{SPOTIFY_API_BASE_URL}audio-features?ids={track_param}', headers=headers).json() # Make a request to the Spotify API to get audio features
    track_features_response = track_features_response["audio_features"]
    track_composite_list = []
    for track in track_features_response:
        single_track_info = []
        track_name_response = requests.get(f'{SPOTIFY_API_BASE_URL}tracks/{track["id"]}', headers=headers).json() # Make a request to the Spotify API to get audio features
        single_track_info = {"name": track_name_response["name"], "key": track["key"], "tempo": round(track["tempo"], 0), "energy": track["energy"]}
        track_composite_list.append(single_track_info)
    return render_template('audio_features.html', result=group_songs(track_composite_list))


def are_keys_compatible(key1, key2):
    return abs(key1 - key2) % 12 in {0, 1, 2, 11}

def are_tempos_compatible(tempo1, tempo2):
    tempo1, tempo2 = max(tempo1, tempo2), min(tempo1, tempo2)
    tempo_dif = tempo1 - tempo2
    if tempo_dif >= 10 and (abs(tempo_dif-tempo2)) >= 10:
        return False
    return True


def group_songs(songs):
    grouped_songs = []

    for song in songs:
        added = False
        for group in grouped_songs:
            if all(are_keys_compatible(song["key"], other_song["key"]) and
                   are_tempos_compatible(song["tempo"], other_song["tempo"])
                   for other_song in group):
                group.append(song)
                added = True
                break

        if not added:
            grouped_songs.append([song])
    grouped_songs = [group for group in grouped_songs if len(group) > 1]

    return grouped_songs



if __name__ == '__main__':
    app.run(debug=True)
