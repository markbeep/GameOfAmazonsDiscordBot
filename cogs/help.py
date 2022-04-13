import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Game of Amazons",
            description="A board game. This bot's main purpose is to allow bots to play another. [Check out the wiki of the game here.](https://en.m.wikipedia.org/wiki/Game_of_the_Amazons)\n"
            "How to play:\n"
            "Using the `start` command you can start a battle against any othert bot (or user). The white player always starts (which is also the player that "
            "initializes the game). The player's take turns using the `play` command to move one of their valid pieces to a new position and shoot an arrow. "
            "After every move, the user ID of the current player is sent along with the current game state, incase you don't keep track of it yourself.\n"
            "If by any chance you want to get the current game state, you can also use the `get` command. *For a more human readable format, use `ama view <match id>`.*"
        )
        embed.add_field(name="‎", value="**Commands:**", inline=False)
        embed.add_field(
            name="⭐start⭐",
            value="Starts a new game with the chosen opponent.\n"
            "**Request Format**: `@Amazons Master | start | enemy_id`\n"
            "- `enemy_id`: The user ID of the bot/player you want to play against. Can be a ping or simply the ID on its own.",
            inline=False
        )
        embed.add_field(
            name="⭐get⭐",
            value="Gets the current game state of a game in a JSON format.\n"
            "The return value is simply a reply to your own message in the following JSON format:\n"
            "`{ 'id': match id, 'board': [[0, ... ,0], ... ,[0, ... ,0]], 'playerWhite': 3123..., 'playerBlack': 3123... }`\n"
            "- `board`: The 10x10 board, where 0 is an empty space, 1 is a white Amazona, 2 is a black Amazona and 3 is an arrow.\n"
            " - `playerWhite` | `playerBlack`: The user IDs for both of the participating players.\n"
            "**Request Format**: `@Amazons Master | get | match_id`\n"
            "- `match_id`: The match ID of a currently ongoing match. Has to be an int.",
            inline=False
        )
        embed.add_field(
            name="⭐play⭐",
            value="Plays a turn and moves a piece and places an arrow.\n"
            "**Request Format**: `@Amazons Master | play | match_id | move_from | move_to | arrow_to`\n"
            "- `match_id`: The match ID of a currently ongoing match. Has to be an int.\n"
            "- `move_from`: The location of the piece you want to move.\n"
            "- `move_to`: The location you want to move the piece. Has to be a legal move.\n"
            "- `arrow_to`: The location you want to shoot the arrow from the new Amazon position.\n"
            "**Note:** *The locations are to be given in a format as follows: `(x,y)` or `[x,y]` or `{x,y}` or `x,y`*",
            inline=False
        )
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
