import logging
logging.basicConfig(level=logging.INFO)
from discord import Member, Guild, TextChannel, Message, PermissionOverwrite, Role, \
    CategoryChannel, Reaction, Embed, Color, Activity, Status, ActivityType
from discord.ext.commands import Bot, Context, check_any, CheckFailure
import configparser
import codecs
import sys

CONFIG_FILE = "data/options.ini"
config = configparser.ConfigParser()
config.read_file(codecs.open(CONFIG_FILE, "r", "utf-8"))

TOKEN = config.get("Discord", "BOT_TOKEN")
DISCORD_STATUS_NAME = config.get("Status", "discord_status")
DISCORD_TYPE = config.get("Status", "discord_status_type")
DISCORD_TWITCH = config.get("Status", "discord_twitch_url")
DISCORD_STATUS = config.get("Status", "discord_member_status")
BOT_PREFIX = config.get("Prefix", "command_prefix")

log = logging.getLogger(__name__)
bot = Bot(
    command_prefix=BOT_PREFIX
)

#Start bot
@bot.listen()
async def on_ready():
    # badly implement status lmao
    #str(DISCORD_TYPE.lower())

    if(DISCORD_TYPE == "watching"):
        await bot.change_presence(status=Status(DISCORD_STATUS), activity=Activity(type=ActivityType.watching, name=DISCORD_STATUS_NAME))

    elif(DISCORD_TYPE == "playing"):
        await bot.change_presence(status=Status(DISCORD_STATUS), activity=Game(name=DISCORD_STATUS_NAME))

    elif(DISCORD_TYPE == "listening"):
        await bot.change_presence(status=Status(DISCORD_STATUS), activity=Activity(type=ActivityType.listening, name=DISCORD_STATUS_NAME))

    elif(DISCORD_TYPE == "streaming"):
        await bot.change_presence(status=Status(DISCORD_STATUS), activity=Streaming(name=DISCORD_STATUS_NAME, url=DISCORD_TWITCH))

    log.info(f"Bot is ready: logged in as {bot.user.name} ({bot.user.id})")
    log.info("Checking for Pterodactyl...")
    if(str(sys.argv[1]) == 'ptero'):
        log.info("Pterodactyl Detected!")
    else:
        log.info("Pterodactyl not found.")


#Login

bot.run(TOKEN)