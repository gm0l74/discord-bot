#---------------------------------
# Discord Bot
# utils/utils.py
#
# @ start date          01 11 2022
# @ last update         03 11 2022
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
from discord.ext import commands

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#---------------------------------
# Library initializers
#---------------------------------
def setup_spotify(client: str, secret: str):
    return spotipy.Spotify(
        auth_manager = SpotifyClientCredentials(
            client_id = client,
            client_secret = secret
        )
    )

#---------------------------------
# Soundcloud
#---------------------------------
async def soundcloud_playlist(search: str):
    # TODO
    # <articles> inside <section class="tracklist">
    # get its 'href'
    # combine with https://soundcloud.com{href}
    # force refresh to see more articles
    pass

#---------------------------------
# Spotify
#---------------------------------
async def spotify_album(spotify: spotipy.Spotify, code: str):
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

async def spotify_playlist(spotify: spotipy.Spotify, code: str):
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

async def handle_playlist_request(spotify: spotipy.Spotify, search: str):
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
    else:
        return search

#---------------------------------
# Logging
#---------------------------------
async def record_usage(_cog: commands.Cog, ctx: commands.Context):
    print(ctx.author, 'used', ctx.command, 'at', ctx.message.created_at)