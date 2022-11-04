#---------------------------------
# Discord Bot
# utils/music/song.py
#
# @ start date          02 11 2022
# @ last update         03 11 2022
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
# Setup
#---------------------------------
YTDL = YoutubeDL(YDL_OPTIONS) # TODO

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

        to_run = partial(YTDL.extract_info, url = search, download = False)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.send(f'Added {data["title"]} to the Queue.', delete_after = 15)
        # TODO more info about the song,
        # https://github.com/rg3/youtube-dl/blob/master/README.md to get more info
        return {
            'webpage_url': data['webpage_url'],
            'requester': ctx.author,
            'title': data['title']
        }

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(YTDL.extract_info, url = data['webpage_url'], download = False)
        data = await loop.run_in_executor(None, to_run)

        source = await discord.FFmpegOpusAudio.from_probe(data['url'])
        return cls(source = source, data = data, requester = requester)