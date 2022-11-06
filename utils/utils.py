#---------------------------------
# Discord Bot
# utils/utils.py
#
# @ start date          01 11 2022
# @ last update         05 11 2022
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
import requests, re
from bs4 import BeautifulSoup
from discord.ext import commands

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from typing import Union, List

#---------------------------------
# Library initializers
#---------------------------------
def setup_spotify(client: str, secret: str) -> spotipy.Spotify:
    return spotipy.Spotify(
        auth_manager = SpotifyClientCredentials(
            client_id = client,
            client_secret = secret
        )
    )

#---------------------------------
# Soundcloud
#---------------------------------
def soundcloud_playlist(url: str) -> List[str]:
    '''
    Returns a list of all the songs in the playlist.
    '''
    html = requests.get(url)
    if html.status_code != 200:
        raise ValueError('Couldn\'t retrieve that soundcloud playlist.')
    
    # Parse the response to find all 'script' tags
    soup = BeautifulSoup(html.text, 'html.parser')
    scripts = soup.find_all('script')

    # Locate and extract playlist info from the scripts
    data_json_pattern = re.compile(r"\"tracks\":\[(.*?)\],\".*\":")
    song_idx_pattern = re.compile(r"\"id\":(.*?),\"kind\":\"track\"")
    
    for script in scripts:
        m = re.search(data_json_pattern, str(script))
        if m:
            break
        
    if not m:
        raise ValueError('Couldn\'t find the playlist info.')
    
    # Extract the id of each song
    songs_idx = re.findall(song_idx_pattern, m.group(1))

    # Convert the song_idx into a streamable url for that song
    track_urls = []
    for idx in songs_idx:
        track_urls.append(f'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{idx}')

    return track_urls

#---------------------------------
# Spotify
#---------------------------------
async def spotify_album(spotify: spotipy.Spotify, code: str) -> List[str]:
    '''
    Returns a list of all the song names in a Spotify album.
    '''
    results = spotify.album_tracks(code, limit = 69)
    info = results['items']

    while results['next']:
        results = spotify.next(results)
        info.extend(results['items'])

    track_names = []

    for track_info in info:
        track_names.append(
            f'{track_info["name"]} - {",".join(x["name"] for x in track_info["artists"])}'
        )
    
    return track_names

async def spotify_playlist(spotify: spotipy.Spotify, code: str) -> List[str]:
    '''
    Returns a list of all the song names in a Spotify playlist.
    '''
    results = spotify.playlist_items(
        code,
        limit = 69,
        additional_types = ['track']
    )
    info = results['items']

    while results['next']:
        results = spotify.next(results)
        info.extend(results['items'])

    track_names = []

    for track_info in info:
        track_names.append(
            f'{track_info["track"]["name"]} - {",".join(x["name"] for x in track_info["track"]["artists"])}'
        )
    
    return track_names

async def handle_playlist_request(spotify: spotipy.Spotify, search: str) -> Union[List[str], str]:
    # Spotify Playlist
    if 'https://open.spotify.com/playlist' in search:
        code = search.split('/')[-1].split('?')[0]
        
        urls = await spotify_playlist(spotify, code)
        return urls

    # Spotify Album
    elif 'https://open.spotify.com/album' in search:
        code = search.split('/')[-1].split('?')[0]
        
        urls = await spotify_album(spotify, code)
        return urls

    # Soundcloud Playlist (aka set)
    elif re.match(r'https://soundcloud.com/(.*)/sets/(.*)', search):
        urls = soundcloud_playlist(search)
        return urls
    
    else:
        return search

#---------------------------------
# Logging
#---------------------------------
async def record_usage(_cog: commands.Cog, ctx: commands.Context):
    '''
    Log usage of a command.

    Simply add this function to a decorator, like so:
    ```py
    @commands.before_invoke(record_usage)
    @commands.command()
    async def cmd(self, ctx: commands.Context):
        pass
    ```
    '''
    print(ctx.author, 'used', ctx.command, 'at', ctx.message.created_at)