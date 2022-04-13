from random import Random
import discord
from discord.ext import commands

from cogs.game import Game


class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.games = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("DONE")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        print(msg.content)
        if msg.content.replace("!", "").startswith(f"<@{self.bot.user.id}>"):
            splitted = msg.content.split("|")  # we split by |
            if len(splitted) < 2:
                await msg.reply("Not enough arguments given")
                return

            request_type = splitted[1].lower().strip()
            try:
                if request_type == "get":
                    await self._get(msg, *splitted[2:])
                    return
                if request_type == "start":
                    await self._start(msg, *splitted[2:])
                    return
                if request_type == "play":
                    await self._play(msg, *splitted[2:])
            except TypeError as e:
                await msg.reply(f"Invalid format received: {e.args}")

    async def _get(self, msg: discord.Message, game_id):
        if game_id is None:
            await msg.reply("No game id given")
            return
        try:
            game_id = int(game_id)
        except ValueError:
            await msg.reply("Game id isn't an int")
            return
        game = self._find_game(game_id)
        if game is None:
            await msg.reply("Currently no game with that id")
            return
        await msg.reply(game.format())

    async def _start(self, msg: discord.Message, enemy_id):
        if enemy_id is None:
            await msg.reply("No enemy player given")
            return
        try:
            enemy_id = int(enemy_id.replace("<", "").replace(
                ">", "").replace("!", "").replace("@", ""))
        except ValueError:
            await msg.reply("Invalid user id given")
            return
        new_game = Game(self._find_random_id(), msg.author.id, enemy_id)
        self.games.append(new_game)
        await msg.reply(new_game.format())

    async def _play(self, msg: discord.Message, game_id, move_from, move_to):
        if game_id is None:
            await msg.reply("No game id given")
            return
        if move_from is None:
            await msg.reply("No move from given")
            return
        if move_to is None:
            await msg.reply("No move to given")
            return
        try:
            game_id = int(game_id)
        except ValueError:
            await msg.reply("Game id isn't an int")
            return
        game = self._find_game(game_id)
        if game is None:
            await msg.reply("No game with that id going on right now")
            return
        valid, reason = game.move(msg.author.id, move_from, move_to)
        if not valid:
            await msg.reply(reason)
            return
        await msg.reply("Move accepted")

    def _find_game(self, game_id) -> Game:
        res = [x for x in self.games if x.id == game_id]
        if len(res) > 0:
            return res[0]
        return None

    def _find_random_id(self):
        # finds a random free id
        rand = Random()
        while True:
            r = rand.randint(111, 999)
            taken_ids = [x.id for x in self.games]
            if r not in taken_ids:
                return r


def setup(bot: commands.Bot):
    bot.add_cog(Main(bot))
