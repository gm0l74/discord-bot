#---------------------------------
# Discord Bot
# cogs/general.py
#
# @ start date          01 11 2022
# @ last update         25 11 2023
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
from discord.ext import commands
from utils import record_usage

import sys
sys.path.append("..")
from authorization import is_antispam_allowed

#---------------------------------
# General [COG]
#---------------------------------
class General(commands.Cog):
    @commands.before_invoke(record_usage)
    @commands.command(name='ping', help='Latency test')
    async def ping(self, ctx: commands.Context):
        t = await ctx.send('Pong!')
        ms = (t.created_at - ctx.message.created_at).total_seconds() * 1000
        await t.edit(content = 'Pong! {} ms'.format(int(ms)))

    @commands.before_invoke(record_usage)
    @commands.command(name='spam', help='Beef spam')
    async def spam(self, ctx: commands.Context):
        for _ in range(20):
            await ctx.send('<:residentsleeper:727251287892295770>')

    @commands.before_invoke(record_usage)
    @commands.command(name='antispam', help='Beef anti spam')
    async def antispam(self, ctx: commands.Context):
        if not is_antispam_allowed(ctx):
            await ctx.send(':clown:' * 5)
            return
        
        for _ in range(4):
            await ctx.send('https://tenor.com/bG8Ja.gif')
            await ctx.send('https://tenor.com/bdek9.gif')

    # ----------------------- GIFs -----------------------
    @commands.before_invoke(record_usage)
    @commands.command(name='gay', help='Quem?')
    async def gay(self, ctx: commands.Context):
        await ctx.send('Sim, de facto, o Bacano é gay!')

    @commands.before_invoke(record_usage)
    @commands.command(name='ripbozo', help='Quando?')
    async def ripbozo(self, ctx: commands.Context):
        await ctx.send('https://tenor.com/view/rip-bozo-gif-22294771')

    @commands.before_invoke(record_usage)
    @commands.command(name='jacinto', help='Jacinto Leite')
    async def jacinto(self, ctx: commands.Context):
        await ctx.send('https://tenor.com/view/milk-milk-man-fresh-milk-gif-22164239')

    @commands.before_invoke(record_usage)
    @commands.command(name='lakaka', help='Wild Lakaka')
    async def lakaka(self, ctx: commands.Context):
        await ctx.send('https://tenor.com/view/lakaka-lakaka-meme-lukaku-chelsea-lukaku-chelsea-gif-23708248')

    @commands.before_invoke(record_usage)
    @commands.command(name='gatodron', aliases=['dron'], help='Drone mais são')
    async def gatodron(self, ctx: commands.Context):
        await ctx.send('https://tenor.com/view/jasminevampirecatswing-gif-20689177')

    @commands.before_invoke(record_usage)
    @commands.command(name='prod', aliases=['test'], help='Real men test in prod')
    async def prod(self, ctx: commands.Context):
        await ctx.send('https://cdn.discordapp.com/attachments/222829160161083397/1125165572515168366/IMG_1793.png')

#---------------------------------
# Setup
#---------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
