from discord.ext import commands
from data.parser import master
from typing import Optional
import discord

description = {"pic": "Выдает рандомное фото рандомной(или выбранной) категории с сайта anime.reactor.cc.",
               "show": "Показывает возможные для выбора категории",
               "Lornorge": ": Пингует Лорнхорна жижареференсом."}


class Hentai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description=description["pic"], brief=": Рандомная аниме пикча.")
    async def pic(self, ctx, *, category: Optional[str] = None):
        if ctx.channel.is_nsfw():
            if category == "show":
                value = master.sorted_categories
                embed = discord.Embed(colour=discord.Colour.blue())
                fields = [("Hentai", value["Hentai"], True),
                          ("Anime", value["Anime"], True),
                          ("Art", value["Art"], True)]
                for name, value, inline in fields:
                    embed.add_field(name=name, value="\n".join(value), inline=inline)
                embed.set_image(url="https://cdn.discordapp.com/attachments/786965436667133993/790977574062260224/ffe264d032fc05e798def5e2bf762efd.png")
                await ctx.send(embed=embed)
            else:
                async with ctx.channel.typing():
                    if category is not None:
                        try:
                            category = master.check_name(category)
                        except master.CategoryNameError:
                            await ctx.send("Некорректная категория")
                            return

                    else:
                        category = "/tag/Anime+Ero"
                    pic_url, post_url = master.purse_func(category)
                    embed = discord.Embed(color=0xff9900, description=post_url)
                    embed.set_image(url=pic_url)
                    await ctx.channel.send(embed=embed)
        else:
            await ctx.send("Здесь такое не позволено")

    @pic.error
    async def on_command_error(self, ctx, ex):
        print(ex)
        await ctx.send("Не выдумывай")

    '''@commands.command(description=description["show"], brief=": Категории.")
    async def show(self, ctx):
        value = get_title()
        embed = discord.Embed(colour=discord.Colour.blue())
        for i in value:
            embed.add_field(name=i, value=", ".join(value[i]))
        embed.set_image(url="https://p4.wallpaperbetter.com/wallpaper/590/589/279/anime-girl-wide-screen-wallpaper"
                            "-preview.jpg")
        await ctx.send(embed=embed)'''

    #  @commands.command(brief=description["Lornorge"])
    #  async def Lornorge(self, ctx, *args):
        #  await ctx.send(ctx.guild.get_member(USERS["Lornorge"]).mention + " " + " ".join(args), file=discord.File(os.path.join(IMAGES_DIR, "Lornorge.png")))

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("hentai")


def setup(bot):
    bot.add_cog(Hentai(bot))
