from discord.ext import commands
from typing import Optional
from discord import Member
from discord.ext.commands.errors import MemberNotFound

description = {"slap": "Шлепает по щеке",
               "echo": "Повторяет сообщение"}


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slap")
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}")

    @slap_member.error
    async def slap_error(self, ctx, exc):
        if isinstance(exc, MemberNotFound):
            await ctx.send("Я не могу найти такого пользователя")

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
