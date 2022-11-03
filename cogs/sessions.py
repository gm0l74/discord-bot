#---------------------------------
# Discord Bot
# cogs/sessions.py
#
# @ start date          03 11 2022
# @ last update         03 11 2022
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
import asyncio

import discord
from discord.ext import commands

from utils import record_usage

#---------------------------------
# Jams [COG]
#---------------------------------
class Jams(commands.Cog):
    '''
    Collection of commands to launch curated sets of playlists
    
    Attributes:
        bot: commands.Bot
            Bot instance that is executing the commands.
    '''
    __slots__ = ('bot')

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.before_invoke(record_usage)
    @commands.command(name='keane', help = 'Queues \'This is Keane\'.')
    async def keane(self, ctx: commands.Context):
        '''
        Queues Spotify playlist: This is Keane.
        '''
        await ctx.invoke(
            self.bot.get_command('play'),
            search = 'https://open.spotify.com/playlist/37i9dQZF1DZ06evO2YcT04?si=b935ac263b7447a5'
        )
        
        await ctx.send(f'**`{ctx.author}`**: Queued \'This is Keane\'!')

    @commands.before_invoke(record_usage)
    @commands.command(name='despacito', help = 'Queues \'Despacito\'.')
    async def despacito(self, ctx: commands.Context):
        '''
        Queues song 'Despacito' by Luis Fonsi.
        '''
        await ctx.invoke(
            self.bot.get_command('play'),
            search = 'https://www.youtube.com/watch?v=kJQP7kiw5Fk'
        )
        
        await ctx.send(f'**`{ctx.author}`**: Queued \'Despacito\'!')

#---------------------------------
# Setup
#---------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Jams(bot))