import discord
from discord.ext import commands
from config import env_variables
from news_scraper import fetch_economic_events
import pytz
from datetime import datetime


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
@bot.command(name='economic_events')
async def economic_events_command(ctx):
  await ctx.send('Fetching economic events...')

  # Fetch economic events
  economic_events = fetch_economic_events()

  # TODO: Move this to a separate file with constants
  # Define impact to emoji mapping
  impact_to_emoji = {
    'High Volatility Expected': '🔴',
    'Moderate Volatility Expected': '🟠',
    'Low Volatility Expected': '🟢'
  }

  # Format economic events into a single message
  events_message = "Economic Events:\n"

  counter: int = 0
  for event in economic_events:
    # TODO: Change name of variable
    emoji = impact_to_emoji.get(event['impact'], '')

    # TODO: Change of variable names and consider moving this to a separate function (line 50 to 59)
    # Parse event time in Eastern Time
    event_time_et = datetime.combine(datetime.now(), datetime.strptime(event['time'], "%H:%M").time())
    eastern = pytz.timezone("America/New_York")
    event_time_et = eastern.localize(event_time_et)  # Localize to Eastern Time

    # Convert to UTC (Discord uses UTC for timestamp calculations)
    event_time_utc = event_time_et.astimezone(pytz.utc)
    
    # Get UNIX timestamp in seconds
    unix_timestamp = int(event_time_utc.timestamp())

    
    events_message += f"<t:{unix_timestamp}:t> - {event['currency']} - {emoji} {event['impact']} - {event['event']}\n"

    counter += 1
    if counter == 5:
      break
  
  # Get the specific channel by ID
  channel_id = 1091731066206830672  # Replace with your channel ID
  channel = bot.get_channel(channel_id)

  # Send economic events as a single message to the specific channel
  if channel:
      await channel.send(events_message)
  else:
      await ctx.send("Could not find the specified channel.")
    
  # Send economic events as a single message
  await ctx.send(events_message)


# Bot execution
bot.run(env_variables['BOT_TOKEN'])