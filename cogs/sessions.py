#---------------------------------
# Discord Bot
# cogs/sessions.py
#
# @ start date          03 11 2022
# @ last update         08 11 2022
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
    @commands.command(name='keane', help='Queues \'This is Keane\'.')
    async def keane(self, ctx: commands.Context):
        '''
        Queues Spotify playlist: This is Keane.
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'This is Keane\'!')
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://open.spotify.com/playlist/37i9dQZF1DZ06evO2YcT04?si=b935ac263b7447a5'
        )

    @commands.before_invoke(record_usage)
    @commands.command(name='philcollins', aliases=['phil', 'collins'], help='Queues \'This is Phil Collins\'.')
    async def philcollins(self, ctx: commands.Context):
        '''
        Queues Spotify playlist: This is Phil Collins.
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'This is Phil Collins\'!')
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://open.spotify.com/playlist/37i9dQZF1DXb3BV2Rig4yV?si=f84c6493761d459f'
        )

    @commands.before_invoke(record_usage)
    @commands.command(name='despacito', help='Queues \'Despacito\'.')
    async def despacito(self, ctx: commands.Context):
        '''
        Queues song 'Despacito' by Luis Fonsi.
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'Despacito\'!')
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://www.youtube.com/watch?v=kJQP7kiw5Fk'
        )

    @commands.before_invoke(record_usage)
    @commands.command(name='ruizinho', help='Queues \'Ruizinho da Penacova\'.')
    async def ruizinho(self, ctx: commands.Context):
        '''
        Queues song 'Vida de Teso' by Ruizinho da Penacova.
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'Ruizinho da Penacova\'!')
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://open.spotify.com/track/0rMoGHo974tZkjpqnzG1pl?si=a4f2b6e874614c1b'
        )

    @commands.before_invoke(record_usage)
    @commands.command(name='bicho', help='Queues \'O bicho\'.')
    async def bicho(self, ctx: commands.Context):
        '''
        Queues song 'O bicho' by Iran Costa.
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'Iran Costa - O bicho\'!')
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://www.youtube.com/watch?v=Ma8AEbLmJn0'
        )

    @commands.before_invoke(record_usage)
    @commands.command(name='champions',aliases=['uefa'], help='Queues \'UEFA Champions League Anthem\'.')
    async def champions(self, ctx: commands.Context):
        '''
        Queues song Champions League Anthem.
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'UEFA Champions League Anthem\'!')
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://www.youtube.com/watch?v=3LyGVsdYSDI'
        )

    @commands.before_invoke(record_usage)
    @commands.command(name='oliverbenji', aliases=['oliver', 'benji'], help='Queues PT Intro/Outro of \'Oliver e Benji\'.')
    async def oliverbenji(self, ctx: commands.Context):
        '''
        Queues Intro and Outro of 'Oliver e Benji' (PT).
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'Oliver e Benji\'!')

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


    @commands.command(name='worldwide', aliases=['pitbull'], help='Queues \'Mr. WorldWide - Mr. 305\'.')
    async def worldwide(self, ctx: commands.Context):
        '''
        Queues Spotify playlist: 'The True Pitbull'.
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'The True Pitbull\'!')
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://open.spotify.com/playlist/4rSQgiTkx0ihUKPwq8WBbF?si=b9e70d846d4844e8'
        )

    @commands.command(name='djjajao', aliases=['jajao', 'dj'], help='Queues \'Orbital Mix - Best Of\' by DJ Jajao.')
    async def djjajao(self, ctx: commands.Context):
        '''
        Queues SoundCloud playlist: 'Orbital Mix - Best Of'.
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'Orbital Mix - Best Of\' by DJ Jajao!')
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://soundcloud.com/erasojajao/sets/orbital-mix-best-of-1'
        )

    @commands.command(name='coding', help='Queues \'edm-coding\' by GMoita.')
    async def coding(self, ctx: commands.Context):
        '''
        Queues Spotify playlist: 'edm-coding'.
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'edm-coding\' by GMoita!')
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://open.spotify.com/playlist/3k9m8Bnz4XOoA3e7Ximz3k?si=6c781604be994c94'
        )

    @commands.command(name='hanji', help='Queues \'Tom Ching Cheng Hanji\' (10m).')
    async def hanji(self, ctx: commands.Context):
        '''
        Queues 'Tom Ching Cheng Hanji'.
        '''
        await ctx.send(f'**`{ctx.author}`**: Queued \'Tom Ching Cheng Hanji\'!')
        await ctx.invoke(
            self.bot.get_command('play'),
            'https://www.youtube.com/watch?v=qGk4E9ss95s'
        )

#---------------------------------
# Setup
#---------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Jams(bot))
