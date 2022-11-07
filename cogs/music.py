#---------------------------------
# Discord Bot
# cogs/music.py
#
# @ start date          02 11 2022
# @ last update         07 11 2022
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
import asyncio

import discord, spotipy, youtube_dl
from discord.ext import commands

from utils import record_usage, handle_playlist_request

from utils.music.song import Song
from utils.music.controller import Controller

#---------------------------------
# Music [COG]
#---------------------------------
class Music(commands.Cog):
    '''
    Collection of commands related to music playback.
    
    Attributes:
        bot: commands.Bot
            Bot instance that is executing the commands.
        spotify: Spotify
            Spotify instance that is used to fetch songs.
    '''
    __slots__ = ('bot', 'spotify', 'controllers')

    def __init__(self, bot: commands.Bot, spotify: spotipy.Spotify):
        self.bot = bot
        self.spotify = spotify

        self.controllers = {}

    def get_controller_for(self, ctx: commands.Context):
        '''
        Create or fetch an existing music controller for the guild.
        '''
        try:
            controller = self.controllers[ctx.guild.id]
        except KeyError:
            controller = Controller(ctx)
            self.controllers[ctx.guild.id] = controller

        return controller

    @commands.before_invoke(record_usage)
    @commands.command(name='play', aliases = ['p'], help='Play a song using spotify or youtube.')
    async def play(self, ctx: commands.Context, *search):
        '''
        Enqueue a song (fetched by YouTube URL or YouTube Search).
        '''
        search = ' '.join(search)
        vc = ctx.voice_client
        if not vc:
            await ctx.invoke(self.connect)

        controller = self.get_controller_for(ctx)

        # Handle Playlists
        queries = await handle_playlist_request(self.spotify, search)
        if isinstance(queries, str):
            queries = [search]
        
        for search in queries:
            # Handle single spotify track
            if 'https://open.spotify.com/track' in search:
                code = search.split('/')[-1].split('?')[0]
                
                info = self.spotify.track(code)
                search = f'{info["name"]} - {",".join(x["name"] for x in info["artists"])}'

            # Handle a possible !stop
            if ctx.guild.id not in self.controllers:
                break

            try:
                source = await Song.create_source(ctx, search, loop = self.bot.loop)
                await controller.queue.put(source)
            except youtube_dl.utils.DownloadError:
                # Convers fetching errors such as 404s and geo-blocked content
                pass

    @commands.before_invoke(record_usage)
    @commands.command(name='shuffle', help='Shuffle the music playlist.')
    async def shuffle(self, ctx: commands.Context):
        '''
        Shuffles all songs in the queue.
        '''
        controller = self.get_controller_for(ctx)
        controller.queue.shuffle()
        await ctx.send(f'**`{ctx.author}`**: Shuffled the playlist!')

    @commands.before_invoke(record_usage)
    @commands.command(name='pause', help='Pause music stream.')
    async def pause(self, ctx: commands.Context):
        '''
        Pause music.
        '''
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send(
                'No music is being played!',
                delete_after = 15
            )
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f'**`{ctx.author}`**: Paused the music!')

    @commands.before_invoke(record_usage)
    @commands.command(name='resume', help='Resume music stream.')
    async def resume(self, ctx: commands.Context):
        '''
        Resume music.
        '''
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(
                'No music is being played!',
                delete_after = 15
            )
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f'**`{ctx.author}`**: Resumed the music!')

    @commands.before_invoke(record_usage)
    @commands.command(name='skip', help='Skip the current music.')
    async def skip(self, ctx: commands.Context):
        '''
        Skip the song.
        '''
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send('No music is being played!', delete_after = 15)

        if not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f'**`{ctx.author}`**: Skipped the song!')

    @commands.before_invoke(record_usage)
    @commands.command(name='stop', help='Stop the entire playlist.')
    async def stop(self, ctx: commands.Context):
        '''
        Stop the entire playlist by destroying the music controller.
        '''
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(
                'No music is being played!',
                delete_after = 15
            )

        await ctx.send(f'**`{ctx.author}`**: Stopped the playlist!')
        await self.disconnect(ctx.guild)

    async def connect(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        '''
        Connect to voice.
        
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to.
        '''
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise AttributeError('Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise ConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise ConnectionError(f'Connecting to channel: <{channel}> timed out.')

        await ctx.send(
            f'Connected to: **{channel}**',
            delete_after = 15
        )

    async def disconnect(self, guild: discord.Guild):
        await guild.voice_client.disconnect()
        del self.controllers[guild.id]

#---------------------------------
# Setup
#---------------------------------
async def setup(bot: commands.Bot, spotify: spotipy.Spotify):
    await bot.add_cog(Music(bot, spotify))