from random import Random
import discord
from discord.ext import commands

from cogs.game import Game
from cogs.variables import MoveState


class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.games = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("DONE")

    @commands.command()
    async def view(self, ctx, game_id: int = -1):
        if game_id == -1:
            await ctx.reply("No game id given")
            return
        game = self._find_game(game_id)
        if game_id is None:
            await ctx.reply("No game with that id")
            return
        await ctx.reply(game.format())

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.content.replace("!", "").startswith(f"<@{self.bot.user.id}>"):
            splitted = msg.content.split("|")  # we split by |
            if len(splitted) < 2:
                return

            request_type = splitted[1].lower().strip()
            if request_type == "get":
                try:
                    await self._get(msg, *splitted[2:])
                except TypeError:
                    await msg.reply(embed=discord.Embed(description="Invalid `get` format:\n`@mention|get|game_id`"))
                return
            if request_type == "start":
                try:
                    await self._start(msg, *splitted[2:])
                except TypeError:
                    await msg.reply(embed=discord.Embed(description="Invalid `start` format:\n`@mention|start|enemy_user_id`"))
                return
            if request_type == "play":
                try:
                    await self._play(msg, *splitted[2:])
                except TypeError:
                    await msg.reply(embed=discord.Embed(description="Invalid `play` format:\n`@mention|play|game_id|move_from|move_to|arrow_to`"))
                return

    async def _get(self, msg: discord.Message, game_id):
        """Replies with the current game board in a JSON format"""
        if game_id is None:
            raise TypeError
        try:
            game_id = int(game_id)
        except ValueError:
            await msg.reply("Game id isn't an int")
            return
        game = self._find_game(game_id)
        if game is None:
            await msg.reply("Currently no game with that id")
            return
        await msg.reply(game.json_format())

    async def _start(self, msg: discord.Message, enemy_id):
        """Starts a new game against a specific enemy"""
        if enemy_id is None:
            raise TypeError
        try:
            enemy_id = int(enemy_id.replace("<", "").replace(
                ">", "").replace("!", "").replace("@", ""))
        except ValueError:
            await msg.reply("Invalid user id given")
            return
        new_game = Game(self._find_random_id(), msg.author.id, enemy_id)
        self.games.append(new_game)
        await msg.reply(new_game.json_format())

    async def _play(self, msg: discord.Message, game_id, move_from, move_to, arrow_to):
        """Moves an amazona from one place to another and shoots an arrow"""
        if game_id is None or move_from is None or move_to is None or arrow_to is None:
            raise TypeError
        try:
            game_id = int(game_id)
        except ValueError:
            await msg.reply("Game id isn't an int")
            return
        game = self._find_game(game_id)
        if game is None:
            await msg.reply("No game with that id going on right now")
            return

        # turns a coordinate format [y,x] / (y,x) / y,x into coords
        async def coord(loc):
            to_remove = ["[", "]", "(", ")", "{", "}"]
            for c in to_remove:
                loc = loc.replace(c, "")
            loc = loc.split(",")
            loc = [int(loc[0]), int(loc[1])]
            return loc

        try:
            valid, reason = game.move(
                msg.author.id,
                await coord(move_from),
                await coord(move_to),
                await coord(arrow_to))
        except ValueError:
            await msg.reply("Invalid coordinates given")
            return
        except IndexError:
            await msg.reply("There was an error parsing the coordinates")
            return

        if valid == MoveState.rejected:
            await msg.reply(reason)
            return

        if valid == MoveState.game_over:
            await msg.reply("Game is over. You won!")
            # removes the game from current ongoing ones
            self.games = list(filter(lambda x: x.id != game.id, self.games))
            return

        if game.get_current_player_id() == self.bot.user.id:
            # makes the AI play if it's the opponent
            # this also automatically swaps back to have it be the other
            # player's turn again
            game.play_ai(self.bot.user.id)

        await msg.reply(f"{game.get_current_player_id()}|**Your Turn!**|{game.json_format()}")

    def _find_game(self, game_id) -> Game:
        """Using the game ID it finds a matching game in the current ongoing game"""
        res = [x for x in self.games if x.id == game_id]
        if len(res) > 0:
            return res[0]
        return None

    def _find_random_id(self):
        """Generates a random 3 digit ID which isn't taken yet.
        This method isn't thread safe though, but I'm just hoping it never comes to that"""
        # finds a random free id
        rand = Random()
        while True:
            r = rand.randint(111, 999)
            taken_ids = [x.id for x in self.games]
            if r not in taken_ids:
                return r


def setup(bot: commands.Bot):
    bot.add_cog(Main(bot))
