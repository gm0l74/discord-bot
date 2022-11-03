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
    @commands.command(name='philcollins', aliases=['phil', 'collins'], help = 'Queues \'This is Phil Collins\'.')
    async def philcollins(self, ctx: commands.Context):
        '''
        Queues Spotify playlist: This is Phil Collins.
        '''
        await ctx.invoke(
            self.bot.get_command('play'),
            search = 'https://open.spotify.com/playlist/37i9dQZF1DXb3BV2Rig4yV?si=f84c6493761d459f'
        )
        
        await ctx.send(f'**`{ctx.author}`**: Queued \'This is Phil Collins\'!')

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

    @commands.before_invoke(record_usage)
    @commands.command(name='champions',aliases=['uefa'], help = 'Queues \'UEFA Champions League Anthem\'.')
    async def champions(self, ctx: commands.Context):
        '''
        Queues song Champions League Anthem.
        '''
        await ctx.invoke(
            self.bot.get_command('play'),
            search = 'https://www.youtube.com/watch?v=3LyGVsdYSDI'
        )
        
        await ctx.send(f'**`{ctx.author}`**: Queued \'UEFA Champions League Anthem\'!')

    @commands.before_invoke(record_usage)
    @commands.command(name='oliverbenji', aliases=['oliver', 'benji'], help = 'Queues PT Intro/Outro of \'Oliver e Benji\'.')
    async def oliver(self, ctx: commands.Context):
        '''
        Queues Intro and Outro of Oliver e Benji (PT).
        '''
        # Oliver e Benji 1ª Abertura - Portugal
        await ctx.invoke(
            self.bot.get_command('play'),
            search = 'https://www.youtube.com/watch?v=hAShEnz1glk'
        )

        # Captain Tsubasa Road to 2002 Portuguese Ending #2
        await ctx.invoke(
            self.bot.get_command('play'),
            search = 'https://www.youtube.com/watch?v=KzP1MntXTF0'
        )
        
        await ctx.send(f'**`{ctx.author}`**: Queued \'Oliver e Benji\'!')

#---------------------------------
# Setup
#---------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Jams(bot))