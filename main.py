#---------------------------------
# Discord Bot
# main.py
#
# @ start date          01 11 2022
# @ last update         06 11 2022
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
import os, asyncio, discord
from datetime import datetime
from discord.ext import commands

from dotenv import load_dotenv

# cogs
import cogs.music as music
import cogs.general as general
import cogs.sessions as sessions
import cogs.scheduled as scheduled

from utils import setup_spotify

#---------------------------------
# Setup
#---------------------------------
load_dotenv()

# - Discord
TOKEN = os.getenv('DISCORD_TOKEN')

# - Spotify
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_SECRET = os.getenv('SPOTIFY_SECRET')

try:
    spotify = setup_spotify(SPOTIFY_CLIENT_ID, SPOTIFY_SECRET)
except:
    spotify = None

#---------------------------------
# Client [BOT]
#---------------------------------
class Client(commands.Bot):
    async def on_command_error(self, ctx, error):
        await super().on_command_error(ctx, error)

        os.makedirs('./logs', exist_ok = True)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open('./logs/errors.log', 'a+') as f:
            f.write(f'[{now}] {error}\n')

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')

        # List all servers that are connected to the bot
        for guild in self.guilds:
            print(f'{self.user} connected to {guild.name}(id: {guild.id})')

#---------------------------------
# Execute
#---------------------------------
bot = Client(
    intents = discord.Intents.all(),
    command_prefix = '!'
)

def init_configs(bot: commands.Bot):
    loop = asyncio.get_event_loop()
    tasks = [
        music.setup(bot, spotify),
        scheduled.setup(bot, spotify),
        sessions.setup(bot),
        general.setup(bot),
    ]
    loop.run_until_complete(asyncio.wait(tasks))

init_configs(bot)
bot.run(TOKEN)