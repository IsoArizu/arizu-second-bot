from discord.ext import commands
import random

description = {"roll": "Выдает рандомное число от 1 до 100"}


class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx):
        num = random.randrange(1, 101)
        await ctx.send(f"{ctx.message.author.name} получает ролл {num}")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("gamble")


def setup(bot):
    bot.add_cog(Gamble(bot))
