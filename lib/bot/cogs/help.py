import discord
import os
from typing import Optional
from discord.utils import get
from discord.ext import commands
from glob import glob

def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []
    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")
    params = " ".join(params)

    return f"```{cmd_and_aliases} {params}```"


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    async def cmd_help(self, ctx, command):
        embed = discord.Embed(title=f"Помощь по команде `{command}`",
                              description=syntax(command),
                              colour=ctx.author.colour)
        embed.add_field(name="Описание команды: ", value=command.help)
        await ctx.send(embed=embed)

    @commands.command(name="help")
    async def show_help(self, ctx, cmd: Optional[str]):
        """Показывает это сообщение."""
        if cmd is None:
            embed = discord.Embed(title="Помощь по командам:",
                                  description="Сейчас я помугу вам разобраться",
                                  colour=discord.Colour.red())
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            embed.add_field(name="Gamble", value="`+roll`: Выдает рандомное число от 1 до 100.\n", inline=False)
            embed.add_field(name="Other", value="`+slap`: Шлепает выбранного пользователя по щеке.\n `+echo`: Повторяет посланное сообщение.\n", inline=False)
            embed.add_field(name="Help", value="`+help`: Показывает это сообщение.\n `+help arg`: Показывает помощь по выбранной команде.\n", inline=False)
            embed.set_thumbnail(url=ctx.bot.get_user(790114584576917535).avatar_url)
            await ctx.send(embed=embed)
        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)
            else:
                await ctx.send("Такой команды не существует")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")


def setup(bot):
    bot.add_cog(Help(bot))
