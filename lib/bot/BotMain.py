import discord
from asyncio import sleep
from datetime import datetime
from discord.ext import commands
from glob import glob
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument, CommandOnCooldown, MissingPermissions
from discord.errors import HTTPException, Forbidden

PREFIX = "+"
OWNER_ID = [327062541438287872]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/bot/cogs/*.py")]
IGNORE_EXCEPTIONS = (commands.CommandNotFound, BadArgument)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"  {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(commands.Bot):
    def __init__(self):
        self.PREFIX = PREFIX
        self.guild = None
        self.ready = False
        self.cogs_ready = Ready()
        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_ID,
            intents=discord.Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.bot.cogs.{cog}")
            print(f" {cog} cog loaded")
        print("setup is complete")

    def run(self, version):
        self.version = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read().strip()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print(" bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Не выдумывай")

        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, commands.CommandNotFound):
            await ctx.send("Не выдумывай")
        #  elif any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            #  pass
        elif isinstance(exc, MissingPermissions):
            await ctx.send("У тебя нету права исполнять эту команду!")
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("Добавь пожалуйста нужные аргументы")
        elif isinstance(exc, BadArgument):
            pass
        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"Твоя команда откатывается. Подожди ещё {exc.retry_after:,.0f} секнуд(ы)")
        elif hasattr(exc, "original"):
            if isinstance(exc.original, HTTPException):
                pass
            elif isinstance(exc.original, Forbidden):
                await ctx.send("У меня нет на это разрешения :(")
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(770674670973878332)

            channel = self.get_channel(786965436667133993)
            users = self.guild.members
            online_count = 0
            for member in users:
                status = member.status
                if status.name == "online":
                    online_count += 1
            embed = discord.Embed(title="IsoArizuBot Подключился к серверу!",
                                  description="Теперь он готов выполнять твои команды. :male_sign:",
                                  colour=discord.Colour.blurple(),
                                  timestamp=datetime.utcnow())
            field = [("Всего пользователей", self.guild.member_count, True),
                     ("Онлайн пользователей", online_count, True)]
            '''for name, value, inline in field:
                embed.add_field(name=name, value=value, inline=inline)'''
            embed.set_author(name=self.guild.name, icon_url=self.guild.icon_url)
            embed.set_thumbnail(url=self.get_user(790114584576917535).avatar_url)
            embed.set_image(url="https://media1.tenor.com/images/5f29f4f87dff192c131f4eba38156837/tenor.gif?itemid=18353747")
            embed.set_footer(text="Without further interruption...")

            await channel.send(embed=embed)
            print(" connecting cogs")
            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            print(" connecting finished")
            self.ready = True
            print("bot ready")

        else:
            print("bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
