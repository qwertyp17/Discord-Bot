import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
import math
import json

def get_prefix(client, message):
  with open ("prefixes.json", "r") as f:
    prefixes = json.load(f)
  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = "k.", case_insensitive = True)
client.remove_command("help")

@client.event
async def on_guild_join(guild):
  with open ("prefixes.json", "r") as f:
    prefixes = json.load(f)

  prefixes[str(guild.id)] = "k."

@client.event #Sends message when bot is online
async def on_ready():
  print("Bot is online")
  await client.change_presence(activity = discord.Game("k.help"))

@client.event
async def on_member_remove(ctx, member):
  await ctx.send(f"{member} has left the server")

@client.command(  ) #Sends help
async def help(ctx):
  embed = discord.Embed(
    title = "Help/Commands",
    colour = (discord.Colour.blurple())
  )
  embed.set_author(name = "K™‡-Œ 18°#9497", icon_url = "https://cdn.discordapp.com/attachments/750164860351807592/751193627455389706/rocket.jpg")
  embed.set_footer(text = "Contact the developer if you require extra support")

  embed.add_field(name = "__**Info**__", value = "**stats** - Information about the bot", inline = False)

  embed.add_field(name = "__**Utility**__:", value = "**rolecheck** - Tells you every user with the supplied role\n**clear [amount]** - Deletes an amount of messages\n**flood [amount] [message]** - Floods the server with a message a number of times", inline = False)

  embed.add_field(name = "__**Fun**__", value = "**flipcoin** - Flips a 2 sided coin\n**rolldie** - Rolls a 6 faced die\n**8ball** - Ask a question and it will answer with the truth", inline = False)

  embed.add_field(name = "__**Misc:**__", value = "Coming Soon", inline = False)

  embed.add_field(name = "__**Support Server:**__", value = "[Link](https://discord.gg/wcVSzpx)", inline = False)

  embed.add_field(name = "__**Invite to Server:**__", value = "[Invite Link](https://discord.com/api/oauth2/authorize?client_id=750408729786318919&permissions=3157216&scope=bot)", inline = False)



  # embed.add_field(name = "__**Top.gg:**__", value = "https://top.gg/bot/750408729786318919", inline = False)


  await ctx.send(embed = embed)

@client.command(aliases = ["coinflip", "flip coin", "coin flip", "flip"]) #Flips coin (50/50 chance)
async def flipcoin(ctx):
  sides = ["heads", "tails"]
  await ctx.send(f"The result is **{random.choice(sides)}**")

@client.command(aliases = ["roll die", "roll", "die roll", "rolldice", "diceroll", "dice roll", "roll dice"]) #Rolls 6 sided die
async def rolldie(ctx):
  await ctx.send(f"The result is **{random.randint(1, 6)}**")

@client.command(aliases = ["info"]) #Info about the bot
async def stats(ctx):
  embed = discord.Embed(
    title = "Information on K™‡-Œ 18°",
    description = "",
    colour = discord.Colour.blue()
  )
  embed.set_author(name = "K18°#9497", icon_url = "https://cdn.discordapp.com/attachments/750164860351807592/751193627455389706/rocket.jpg")
  embed.add_field(name = "Creation Date", value = "September 1, 2020", inline = False)
  embed.add_field(name = "Number of Servers in Use", value = len(client.guilds), inline = False)
  ping = (round(client.latency * 1000))
  embed.add_field(name = "Latency/Ping", value = (f"{ping} ms"))
  await ctx.send(embed = embed)

@client.command(aliases = ["role", "checkrole"])
async def rolecheck(ctx,* ,role: discord.Role):
    userList = [member.name for member in role.members]
    try:
        msg = "\n".join(userList)
        length = len(userList)
        await ctx.send(f"`{length} members have the role:`\n\n{msg}")
    except discord.ext.commands.errors.MissingRequiredArgument:
        await ctx.send("Please provide a role name")
    except discord.ext.commands.errors.BadArgument:
        await ctx.send("Please provide a member name")

@client.command(aliases = ["check user" , "user check", "usercheck"])
async def checkuser(ctx, member: discord.Member):
  try:
    if discord.Member in discord.Guild:
      await ctx.send(f"{discord.Member} is in {discord.Guild}")
    elif discord.Member not in discord.Guild:
      await ctx.send(f"{discord.Member} is not in {discord.Guild}")
  except discord.ext.commands.errors.MissingRequiredArgument:
    await ctx.send("Please provide a member name")
  except discord.ext.commands.errors.BadArgument:
    await ctx.send("Please provide a member name")

@client.command(aliases = ["f"])
async def flood(ctx, amount = 0, *, bruh: str):
  message = bruh
  if amount == 0:
    await ctx.send("Try again with: **flood [message] [amount]**   ")
  if bruh == "":
    await ctx.send("Try again with: **flood [message] [amount]**   ")
  if "@" in bruh:
    await ctx.send("Do not try to mention someone with this command!")
  else:
    for i in range(amount):
     await ctx.send(message)

@client.command(aliases = ["c"])
async def clear(ctx, amount = 1):
  # if discord.Message.author != discord.Permissions.manage_messages:
  #   await ctx.send("You don't have permission to do this!")
  if amount == 1:
    await ctx.channel.send("Try again with the number of messages (greater than 1)")
  else:
    await ctx.channel.purge(limit = amount + 1)

@client.command(aliases = ["8ball", "eightball"])
async def _8ball(ctx, self):
  answers = [
    "It is certain","It is decidedly so", "Without a doubt", "Yes", "No", "Very doubtful", "https://i.imgflip.com/34yx3j.png", "https://i.redd.it/m4h9tq9474841.png","Definitely not", "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/1c549136-46a2-48b3-8a76-8a4f6e02d7d1/dden5ov-79e83b4d-788b-4394-8131-97643053c299.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvMWM1NDkxMzYtNDZhMi00OGIzLThhNzYtOGE0ZjZlMDJkN2QxXC9kZGVuNW92LTc5ZTgzYjRkLTc4OGItNDM5NC04MTMxLTk3NjQzMDUzYzI5OS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.jRO3qOavot-efIDgU1iploT-1mrTWs0UiNC5XHFq420"
  ]
  try:
    await ctx.send(random.choice(answers))
  except discord.ext.commands.errors.MissingRequiredArgument:
    await ctx.send("Provide a question")

@client.command()
async def rate(ctx, *,thing: str):
  await ctx.send(f"{thing}: {random.randint(1, 100)}/100")

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command(aliases = ["pic"])
async def picture(ctx):
  await ctx.send("https://cdn.discordapp.com/attachments/748571137973288980/814691906692055060/blt.jpg")


# @client.command(aliases = ["case"])
# async def casechange(ctx, case: str, *, message: str):
#   case2 = case.lower
#   if case2 = "upper":
#     convertedmessage = message.upper
#     await ctx.send(f"{convertedmessage}")

#   elif case.lower = ("lower"):
#     convertedmessage = message.lower
#     await ctx.send(convertedmessage)

# @client.command()
# async def serverinfo(ctx):
#   embed = discord.Embed(
#     title = "",
#     description = "",
#     colour = discord.Colour.blue()
#   )
#   embed.set_author(name = "", icon_url = "")
#   embed.add_field(name = "Creation Date", value = discord.Guild.created_at, inline = False)
#   embed.add_field(name = "Owner", value = discord.Guild.owner, inline = False)
#   embed.add_field(name = "Members", value = discord.Guild.member_count, inline = False)
#   # embed.add_field(name = "Text Channels", value = len(discord.Guild.text_channels), inline = False )
#   # embed.add_field(name = "Voice Channels", value = len(discord.Guild.voice_channels), inline = False )
#   # embed.add_field(name = "Roles", value = len(discord.Guild.roles), inline = False )
#   embed.add_field(name = "Region", value = discord.Guild.region, inline = False)
#   # embed.add_field(name = "Emojis", value = len(discord.Guild.emojis), inline = False )
#   await ctx.send(embed = embed)
# @client.command()
# async def gif(ctx, word = str):

client.run("token")
