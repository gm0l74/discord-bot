#---------------------------------
# Discord Bot
# cogs/scheduled.py
#
# @ start date          03 11 2022
# @ last update         04 11 2022
#---------------------------------

#---------------------------------
# Docs
#---------------------------------
# https://stackoverflow.com/questions/59801751/discordpy-tasks-not-working-as-expected-no-returning
# https://stackoverflow.com/questions/65124909/i-want-to-run-task-everyday-0000-discord-py

#---------------------------------
# Imports
#---------------------------------
import discord, spotipy
from discord.ext import commands, tasks

from utils import spotify_playlist
from utils.music.song import Song

from typing import Callable

#---------------------------------
# Utils
#---------------------------------
class Object(object):
    pass

# Hacky workaround to get around the fact that discord.py
# doesnt provide 'context' to a task.loop
# 
# Manuallly create the context with the necessary fields
def mock_ctx(
    bot: commands.Bot,
    guild_idx: str,
    channel_idx: str,
    voice_client: discord.VoiceClient,
    send_message: Callable
):
    ctx = Object()

    ctx.guild = Object()
    ctx.guild.voice_client = voice_client
    ctx.guild.id = guild_idx

    ctx.channel = Object()
    ctx.channel.id = channel_idx

    ctx.bot = bot
    ctx.cog = bot.get_cog('Music')

    ctx.author = 'auto'

    ctx.send = send_message
    ctx.channel.send = send_message

    return ctx

#---------------------------------
# Scheduled [COG]
#---------------------------------
class Scheduled(commands.Cog):
    '''
    Collection of scheduled tasks.
    
    Attributes:
        bot: commands.Bot
            Bot instance that is executing the commands.
    '''
    __slots__ = ('bot')

    def __init__(self, bot: commands.Bot, spotify: spotipy.Spotify):
        self.bot = bot
        self.spotify = spotify

        self.text_channels = {}
        self.voice_channels = {}

    @commands.Cog.listener()
    async def on_ready(self):
        # Populate the communication channels of the bot
        for guild in self.bot.guilds:
            for channel in guild.voice_channels:
                # Lock the bot to a single voice channel
                # [FIFO]
                self.voice_channels[guild.id] = channel.id
                break
        
            for channel in guild.text_channels:
                # Lock the bot to a single text channel
                # [FIFO]
                self.text_channels[guild.id] = channel.id
                break

        # Start the scheduled tasks
        if not self.keane.is_running():
            self.keane.start()

    def cog_unload(self):
        self.keane.cancel()

    @tasks.loop(hours = 24)
    async def keane(self):
        '''
        Scheduled task to automatically queue the Spotify playlist: 'This is Keane'.
        '''
        # TODO: thread this
        for guild_idx, channel_idx in self.voice_channels.items():
            # Connect to the voice channel of the guild
            vc = self.bot.get_channel(channel_idx)
            try:
                voice = await vc.connect()
            except discord.errors.ClientException:
                pass
            
            ctx = mock_ctx(
                guild_idx = guild_idx,
                channel_idx = channel_idx,
                bot = self.bot,
                voice_client = voice,
                send_message = lambda t, **kwargs: self.bot.get_channel(
                    self.text_channels[guild_idx]
                ).send(t, **kwargs)
            )

            # Load the music controller from the cog: Music
            controller = self.bot.get_cog('Music').get_controller_for(ctx)

            # Add 'This is Keane' spotify playlist to the queue
            queries = await spotify_playlist(
                self.spotify,
                'https://open.spotify.com/playlist/37i9dQZF1DZ06evO2YcT04?si=b935ac263b7447a5'
            )
            if isinstance(queries, str):
                queries = [search]
            
            for search in queries:
                source = await Song.create_source(ctx, search, loop = self.bot.loop)
                await controller.queue.put(source)

    @keane.before_loop
    async def before_keane_task(self):
        # TODO: run at a specific time
        await self.bot.wait_until_ready()

#---------------------------------
# Setup
#---------------------------------
async def setup(bot: commands.Bot, spotify: spotipy.Spotify):
    await bot.add_cog(Scheduled(bot, spotify))