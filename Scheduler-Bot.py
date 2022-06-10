import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from modules.Scheduler import Calendar
# This is MY PERSONAL TOKEN for the bot :)
from private.auth import PASSWORD

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='>>')

bot.calendar = Calendar()

def make_day_selector():
  selector = Select(
    min_values=1,
    max_values=1,
    placeholder='Pick Day',
  )

  for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']: 
    selector.add_option(label=day)

  return selector

def make_time_selector():
  selector = Select(
    max_values = 24,
    placeholder='Pick Time',
  )

  for i in range(24):
    start_str = str(i)
    if len(start_str) < 2: start_str = '0' + start_str
    end_str = str(i+1) if i != 23 else '0'
    if len(end_str) < 2: end_str = '0' + end_str
    selector.add_option(
      label=f"{start_str}:00 to {end_str}:00",
      value=i)

  return selector

@bot.command()
async def my_schedule(ctx):
  await ctx.send(
    bot.calendar.usr_sched_as_str(ctx.author)
)

@bot.command()
async def enter_times(ctx):
  select_day = make_day_selector()
  select_time = make_time_selector()
  button = Button(
    label='Clear',
    style=discord.ButtonStyle.green,
  )

  view = View()
  view.add_item(select_day)
  view.add_item(select_time)
  view.add_item(button)

  async def callback_day(interaction):
    select_day.placeholder = select_day.values[0]
    select_time.placeholder = f"Selecting for {select_day.values[0]}"
    button.label = f"Clear {select_day.placeholder}"
    await interaction.response.edit_message(
      content=bot.calendar.get_avail_days(ctx.author),
      view=view
    )
  select_day.callback = callback_day

  async def callback_time(interaction):
    select_time.placeholder = f"Time chosen for {select_day.placeholder}"
    button.label = f"Clear {select_day.placeholder}"
    bot.calendar.update(ctx.author, select_day.placeholder, select_time.values)
    await interaction.response.edit_message(
      content=bot.calendar.get_avail_days(ctx.author),
      view=view
    )
  select_time.callback = callback_time

  async def callback_button(interaction):
    bot.calendar.update(ctx.author, select_day.placeholder, [])
    button.label = f"Cleared {select_day.placeholder}"
    await interaction.response.edit_message(
      content=bot.calendar.get_avail_days(ctx.author),
      view=view)
  button.callback = callback_button

  await ctx.send('Enter Your Availability', view=view)

@bot.command()
async def results(ctx):
  await ctx.send(bot.calendar.find_best())
  
@bot.command()
async def reset(ctx):
  bot.calendar = Calendar()
  await ctx.send('bot is reset')

if __name__ == "__main__":
  bot.run(PASSWORD)