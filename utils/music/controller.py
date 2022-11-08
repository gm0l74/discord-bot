#---------------------------------
# Discord Bot
# utils/music/controller.py
#
# @ start date          03 11 2022
# @ last update         08 11 2022
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
from random import shuffle
import asyncio
from async_timeout import timeout

import discord
from discord.ext import commands

from utils.music.song import Song

#---------------------------------
# Constants
#---------------------------------
TIMEOUT = 5 * 60 # in seconds

#---------------------------------
# Playlist
#---------------------------------
class Playlist(asyncio.Queue):
    def shuffle(self):
        shuffle(self._queue)

#---------------------------------
# Controller
#---------------------------------
class Controller:
    __slots__ = (
        'bot',
        'cog',
        'guild',
        'channel',
        'queue',
        'next',
        'np',
        'current'
    )

    def __init__(self, ctx: commands.Context):
        self.bot = ctx.bot
        self.cog = ctx.bot.get_cog('Music')

        self.guild = ctx.guild
        self.channel = ctx.channel

        self.queue = Playlist()
        self.next = asyncio.Event()

        self.np = None
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        '''
        Main player loop.
        '''
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song
                # Cancel the player and disconnect, if it timeouts...
                async with timeout(TIMEOUT):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self.guild)

            if not isinstance(source, Song):
                # Regather to prevent stream expiration and peer connection reset
                try:
                    song = await Song.regather_stream(source, loop = self.bot.loop)
                except Exception as e:
                    await self.channel.send(
                        f'There was an error processing your song.\n```css\n[{e}]\n```'
                    )
                    continue

            self.current = song
            if self.guild.voice_client:
                try:
                    self.guild.voice_client.play(
                        song.source,
                        after = lambda _: self.bot.loop.call_soon_threadsafe(self.next.set)
                    )
                except:
                    continue

            self.np = await self.channel.send(
                f'**Now Playing:** `{song.title}` requested by `{song.requester}`'
            )
            
            await self.next.wait()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass
            except AttributeError:
                # No message has actually been sent
                # It has probably been faked
                pass

    def destroy(self, guild: discord.Guild):
        '''
        Disconnect and cleanup the player.
        '''
        return self.bot.loop.create_task(self.cog.disconnect(guild))