from discord.ext import commands
from typing import Optional
from discord import Member
from discord.ext.commands.errors import MemberNotFound
import discord

description = {"slap": "Шлепает по щеке",
               "echo": "Повторяет сообщение"}


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slap")
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "без причины"):
        await ctx.send(f"{ctx.author.display_name} ударил по щеке {member.mention} {reason}")

    @slap_member.error
    async def slap_error(self, ctx, exc):
        if isinstance(exc, MemberNotFound):
            await ctx.send("Я не могу найти такого пользователя")

    @commands.command(name="F", aliased=["respect"])
    async def F_command(self, ctx, *args):
        name = " ".join(args)
        if len(name) > 0:
            embed = discord.Embed(title="Сообщение о респекте", colour=discord.Colour.red())
            embed.add_field(name=ctx.message.author.name, value=f"Pays respect to {name}")
        else:
            embed = discord.Embed(title=f"Сообщение о респекте", colour=discord.Colour.red())
            embed.add_field(name=ctx.message.author.name, value="Pays respect")
        embed.set_author(name=self.bot.guild.name, icon_url=self.bot.guild.icon_url)
        embed.set_thumbnail(url="https://media1.tenor.com/images/5543cf0b34a0f3c3b7b22d335ee1c330/tenor.gif?itemid=16463488")
        embed.set_image(url="https://images4.fanpop.com/image/photos/22100000/The-letter-the-alphabet-22187359-2560-2560.jpg")
        await ctx.send(embed=embed)

    @commands.command(name="echo")
    async def echo(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("other")


def setup(bot):
    bot.add_cog(Other(bot))
