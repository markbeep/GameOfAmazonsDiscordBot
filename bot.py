import discord
from discord.ext import commands
from util.file import create_files
from util.json import get_config
import os

create_files()
config = get_config()

bot = commands.Bot(command_prefix=config.prefixes)

print("Loading main extension:\t", end="", flush=True)
bot.load_extension("cogs.main")
print("DONE")


print("Logging in:\t", end="", flush=True)
bot.run(config.token)
