#---------------------------------
# Discord Bot
# cogs/general.py
#
# @ start date          01 11 2022
# @ last update         07 11 2022
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
from discord.ext import commands
from utils import record_usage

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

#---------------------------------
# Setup
#---------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))