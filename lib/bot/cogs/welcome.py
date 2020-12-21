from discord.ext import commands
import discord


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        #  db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        embed = discord.Embed(title="Присоединился новый член!",
                              description=f"Приветствуем {member.mention} на нашем сервере.\n\n"
                                          "Советую тебе прописать `+help` для ознакомления с возможностями нашего бота",
                              colour=discord.Colour.red())
        embed.set_author(name=self.bot.guild.name, icon_url=self.bot.guild.icon_url)
        embed.set_image(
            url="https://media1.tenor.com/images/de33002aaf0aad1d9ddd0065c169f2ec/tenor.gif?itemid=18556640")
        embed.set_thumbnail(url=member.avatar_url)
        await self.bot.get_channel(786965436667133993).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")


def setup(bot):
    bot.add_cog(Welcome(bot))
