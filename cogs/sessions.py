#---------------------------------
# Discord Bot
# cogs/sessions.py
#
# @ start date          03 11 2022
# @ last update         06 11 2022
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
            'https://open.spotify.com/playlist/37i9dQZF1DZ06evO2YcT04?si=b935ac263b7447a5'
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
            'https://open.spotify.com/playlist/37i9dQZF1DXb3BV2Rig4yV?si=f84c6493761d459f'
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
            'https://www.youtube.com/watch?v=kJQP7kiw5Fk'
        )

        await ctx.send(f'**`{ctx.author}`**: Queued \'Despacito\'!')

    @commands.before_invoke(record_usage)
    @commands.command(name='ruizinho', help = 'Queues \'Ruizinho da Penacova\'.')
    async def ruizinho(self, ctx: commands.Context):
        '''
        Queues song 'Vida de Teso' by Ruizinho da Penacova.
        '''
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://open.spotify.com/track/0rMoGHo974tZkjpqnzG1pl?si=a4f2b6e874614c1b'
        )

        await ctx.send(f'**`{ctx.author}`**: Queued \'Ruizinho da Penacova\'!')

    @commands.before_invoke(record_usage)
    @commands.command(name='bicho', help = 'Queues \'O bicho\'.')
    async def ruizinho(self, ctx: commands.Context):
        '''
        Queues song 'O bicho' by Iran Costa.
        '''
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://www.youtube.com/watch?v=Ma8AEbLmJn0'
        )

        await ctx.send(f'**`{ctx.author}`**: Queued \'Iran Costa - O bicho\'!')

    @commands.before_invoke(record_usage)
    @commands.command(name='champions',aliases=['uefa'], help = 'Queues \'UEFA Champions League Anthem\'.')
    async def champions(self, ctx: commands.Context):
        '''
        Queues song Champions League Anthem.
        '''
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://www.youtube.com/watch?v=3LyGVsdYSDI'
        )

        await ctx.send(f'**`{ctx.author}`**: Queued \'UEFA Champions League Anthem\'!')

    @commands.before_invoke(record_usage)
    @commands.command(name='oliverbenji', aliases=['oliver', 'benji'], help = 'Queues PT Intro/Outro of \'Oliver e Benji\'.')
    async def oliver(self, ctx: commands.Context):
        '''
        Queues Intro and Outro of 'Oliver e Benji' (PT).
        '''
        # Oliver e Benji 1ª Abertura - Portugal
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://www.youtube.com/watch?v=hAShEnz1glk'
        )

        # Captain Tsubasa Road to 2002 Portuguese Ending #2
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://www.youtube.com/watch?v=KzP1MntXTF0'
        )

        await ctx.send(f'**`{ctx.author}`**: Queued \'Oliver e Benji\'!')


    @commands.command(name='worldwide', aliases=['pitbull'], help = 'Queues \'Mr. WorldWide - Mr. 305\'.')
    async def worldwide(self, ctx: commands.Context):
        '''
        Queues Spotify playlist: 'The True Pitbull'.
        '''
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://open.spotify.com/playlist/4rSQgiTkx0ihUKPwq8WBbF?si=b9e70d846d4844e8'
        )

        await ctx.send(f'**`{ctx.author}`**: Queued \'The True Pitbull\'!')

    @commands.command(name='djjajao', aliases=['jajao', 'dj'], help = 'Queues \'Orbital Mix - Best Of\' by DJ Jajao.')
    async def djjajao(self, ctx: commands.Context):
        '''
        Queues SoundCloud playlist: 'Orbital Mix - Best Of'.
        '''
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://soundcloud.com/erasojajao/sets/orbital-mix-best-of-1'
        )

        await ctx.send(f'**`{ctx.author}`**: Queued \'Orbital Mix - Best Of\' by DJ Jajao!')

#---------------------------------
# Setup
#---------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Jams(bot))
