from pydoc import describe
import discord
from discord.ext import commands
from matplotlib.pyplot import title


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Game of Amazons",
            description="10x10 field, cool game, [basically read the wiki](https://en.m.wikipedia.org/wiki/Game_of_the_Amazons)"
        )
        embed.add_field(name="start", value="Starts the game")
        embed.add_field(name="get", value="Gets a game's status")
        embed.add_field(name="play", value="Moves a piece")
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
