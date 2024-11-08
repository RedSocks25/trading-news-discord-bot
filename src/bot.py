import discord
from discord.ext import commands

from config import env_variables


class PowellBotClient(commands.Bot):

  def __init__(self, command_prefix: str, **options):
    super().__init__(command_prefix=command_prefix, **options)
  
  async def on_ready(self):
    print(f'Logged on as {self.user}!')


# Bot settings and initialization
intents = discord.Intents.default()
intents.messages = True

bot = PowellBotClient(command_prefix='!', intents=intents)


# Bot commands
@bot.command(name='hello')
async def hello_command(ctx):
  await ctx.send(f'Hello! How are you {ctx.author.mention}?')


# Bot execution
bot.run(env_variables['BOT_TOKEN'])