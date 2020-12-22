from datetime import datetime
from typing import Optional
import discord
from discord.ext import commands

description = {"roll": "Выдает рандомное число от 1 до 100"}


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = bot.get_channel(786965436667133993)

    @commands.command(name="kick")
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, targets: commands.Greedy[discord.Member], *, reason: Optional[str] = "Без причины"):
        if not len(targets):
            await ctx.send("Нужно ввести пользователей, которых ты хочешь кикнуть.")
        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position\
                        and not target.guild_permissions.administrator:
                    await target.kick(reason=reason)
                    embed = discord.Embed(title="Кик оповещение",
                                          description=f"Пользователь с именем {target.name} был выгнан из сервера.",
                                          colour=discord.Colour.red(),
                                          timestamp=datetime.utcnow())
                    fields = [("Выгнали", f"{target.name} также известного как {target.display_name}", False),
                              ("Выгнал", f"{ctx.author.display_name}", False),
                              ("Причина", reason, False)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    embed.set_thumbnail(url=target.avatar_url)
                    await self.bot.get_channel(786965436667133993).send(embed=embed)
                else:
                    await ctx.send(f"{target.display_name} не может быть выгнан")

    @commands.command(name="ban")
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, targets: commands.Greedy[discord.Member], *, reason: Optional[str] = "Без причины"):
        if not len(targets):
            await ctx.send("Нужно ввести пользователей, которых ты хочешь кикнуть.")
        else:
            for target in targets:
                await target.ban(reason=reason)
                if ctx.guild.me.top_role.position > target.top_role.position \
                        and not target.guild_permissions.administrator:
                    embed = discord.Embed(title="Бан оповещение",
                                          description=f"Пользователь с именем {target.name} был забанен на сервере.",
                                          colour=discord.Colour.red(),
                                          timestamp=datetime.utcnow())
                    fields = [("Забанили", f"{target.name} также известного как {target.display_name}", False),
                              ("Забанил", f"{ctx.author.display_name}", False),
                              ("Причина", reason, False)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    embed.set_thumbnail(url=target.avatar_url)
                    await self.bot.get_channel(786965436667133993).send(embed=embed)
                else:
                    await ctx.send(f"{target.display_name} не может быть забанен")

    @commands.command(name="erase", aliases=["clear"])
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, limit: Optional[int] = 1):
        if limit > 0:
            with ctx.channel.typing():
                deleted = await ctx.channel.purge(limit=limit+1)
                await ctx.send(f"Удалено {len(deleted):,} сообщений", delete_after=5)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("moderation")


def setup(bot):
    bot.add_cog(Moderation(bot))