#---------------------------------
# Discord Bot
# utils/music/song.py
#
# @ start date          02 11 2022
# @ last update         08 11 2022
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
import discord
from discord.ext import commands

import asyncio
from functools import partial
from youtube_dl import YoutubeDL

from constants import YDL_OPTIONS, FFMPEG_OPTIONS

#---------------------------------
# Constants
#---------------------------------
N_LIMIT_ATTEMPTS = 3

#---------------------------------
# Song
#---------------------------------
class Song:
    def __init__(self, source, data, requester):
        self.source = source
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(
        cls,
        ctx: commands.Context,
        search: str,
        *,
        loop: asyncio.BaseEventLoop = None
    ):
        loop = loop or asyncio.get_event_loop()

        n_attempts = 0
        while n_attempts < N_LIMIT_ATTEMPTS:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                to_run = partial(ydl.extract_info, url = search, download = False)
            data = await loop.run_in_executor(None, to_run)

            if data: break
            else: n_attempts += 1

            await asyncio.sleep(5)
        
        if 'entries' in data:
            data = data['entries'][0]

        await ctx.send(f'Added {data["title"]} to the Queue.', delete_after = 15)
        return {
            'webpage_url': data['webpage_url'],
            'requester': ctx.author,
            'title': data['title'],
            'upload_date': data['upload_date'],
            'artist': data['uploader'],
            'duration': data['duration'],
            'thumbnail': data['thumbnail'],
            'views': data['view_count'],
        }

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        n_attempts = 0
        while n_attempts < N_LIMIT_ATTEMPTS:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                to_run = partial(ydl.extract_info, url = data['webpage_url'], download = False)
            data = await loop.run_in_executor(None, to_run)

            if data: break
            else: n_attempts += 1

            await asyncio.sleep(5)

        source = await discord.FFmpegOpusAudio.from_probe(data['url'], **FFMPEG_OPTIONS) # TODO: requires more testing
        return cls(source = source, data = data, requester = requester)