from discord.ext import commands
from util.file import create_files
from util.json import get_config

create_files()
config = get_config()

bot = commands.Bot(command_prefix=config.prefixes)

# removes the help command
bot.remove_command("help")

print("Loading main extension:\t", end="", flush=True)
bot.load_extension("cogs.main")
print("DONE")
print("Loading help extension:\t", end="", flush=True)
bot.load_extension("cogs.help")
print("DONE")


print("Logging in:\t", end="", flush=True)
bot.run(config.token)
