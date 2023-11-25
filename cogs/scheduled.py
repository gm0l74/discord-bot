#---------------------------------
# Discord Bot
# cogs/scheduled.py
#
# @ start date          03 11 2022
# @ last update         10 11 2022
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
import os, json
from datetime import datetime, time

import discord, spotipy
from discord.ext import commands, tasks

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
    send: Callable
):
    ctx = Object()
    ctx.voice_client = voice_client

    ctx.guild = Object()
    ctx.guild.voice_client = voice_client
    ctx.guild.id = guild_idx

    ctx.channel = Object()
    ctx.channel.id = channel_idx

    ctx.bot = bot
    ctx.cog = bot.get_cog('Music')

    ctx.author = ':robot:'
    ctx.send = ctx.channel.send = send

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

        self.db = json.load(open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                '..', 'birthdays_db.json'
            ), 'r'
        ))

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
            self.birthdays.start()

    def cog_unload(self):
        self.keane.cancel()
        self.birthdays.cancel()

    #---------------------------------------------------------------------------------------------------
    # TASK: Keane
    #---------------------------------------------------------------------------------------------------
    @tasks.loop(time = time(23, 0, 0))
    async def keane(self):
        '''
        Schedule a task to automatically queue the Spotify
        playlist: 'This is Keane' every day at 23:00.
        '''
        async def _keane(guild_idx: str, channel_idx: str):
            try:
                # Connect to the voice channel
                vc = await self.bot.get_channel(channel_idx).connect()
            except:
                # Already connected to a voice channel
                vc = self.bot.get_guild(guild_idx).voice_client

            text = self.bot.get_channel(self.text_channels[guild_idx])
            ctx = mock_ctx(
                self.bot,
                guild_idx, channel_idx, vc,
                lambda m, **kwargs: text.send(m, **kwargs)
            )
            await ctx.cog.play(
                ctx,
                'https://open.spotify.com/track/609vJX1mWBVtteIjcJj9oa?si=4dd8f5287c3f44e2'
            )

        for guild_idx, channel_idx in self.voice_channels.items():
            self.bot.loop.create_task(_keane(
                guild_idx = guild_idx,
                channel_idx = channel_idx
            ))

    @keane.before_loop
    async def before_keane_task(self):
        await self.bot.wait_until_ready()

    #---------------------------------------------------------------------------------------------------
    # TASK: Birthdays
    #---------------------------------------------------------------------------------------------------
    @tasks.loop(time = time(0, 0, 0))
    async def birthdays(self):
        '''
        Schedule a task to automatically wish a happy birthday.
        '''
        async def _birthdays(
            guild_idx: str,
            voice_channel_idx: str,
            text_channel: discord.channel.TextChannel,
            name: str
        ):
            # Send chat message
            msg = await text_channel.send(f'Parabéns **`{name}`**! {":tada:" * 5}{":partying_face:" * 5}')

            # Add emoji reactions to the message
            await msg.add_reaction('\N{PARTY POPPER}')
            await msg.add_reaction('\N{FACE WITH PARTY HORN AND PARTY HAT}')

        now = datetime.now().strftime('%d-%m')
        if now not in self.db:
            return

        name = self.db[now]
        for guild_idx, text_channel_idx in self.text_channels.items():
            text_channel = self.bot.get_channel(text_channel_idx)
            self.bot.loop.create_task(_birthdays(
                guild_idx,
                self.voice_channels[guild_idx],
                text_channel,
                name
            ))

    @birthdays.before_loop
    async def before_birthdays_task(self):
        await self.bot.wait_until_ready()

#---------------------------------
# Setup
#---------------------------------
async def setup(bot: commands.Bot, spotify: spotipy.Spotify):
    await bot.add_cog(Scheduled(bot, spotify))
