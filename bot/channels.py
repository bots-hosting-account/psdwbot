import discord
from replit import db

saved_channels = {}


async def save_channel_to_db(cmd_parts, message):
  if len(cmd_parts) < 2 or len(cmd_parts[1]) == 0:
    await message.reply("Error: No save name provided")
    return
  
  save_name = cmd_parts[1]
  saved_channels[save_name] = message.channel
  db.set(f"V{save_name}", message.channel.id)
  
  if not (len(cmd_parts) > 2 and "q" in cmd_parts[2]):
    await message.reply(f"Saved #{message.channel.name} as {save_name}")


async def send_get_channel_message(cmd_parts, message):
  if len(cmd_parts) < 2 or len(cmd_parts[1]) == 0:
    await message.reply("Error: No save name provided")
    return
  
  save_name = cmd_parts[1]
  if save_name in saved_channels:
    channel = saved_channels[save_name]
    await message.reply(f"The channel saved as {save_name} is {format_channel(channel)}")
  else:
    await message.reply(f"No channel is saved as `{save_name}`")


async def send_message_in_saved_channel(cmd_parts, message, format_as_code):
  command = cmd_parts[0]
  space_index = message.content.index(command) + len(command)
  arguments = message.content[space_index + 1:]
  if " " not in arguments:
    await message.reply("Cannot send an empty message")
    return
  elif arguments.startswith(" "):
    await message.reply("Error: No save name provided")
    return
  
  save_name, to_send = arguments.split(" ", 1)
  
  if save_name not in saved_channels:
    await message.reply(f"Error: No channel is saved as `{save_name}`")
    return
  
  if format_as_code:
    to_send = f"```\n{to_send}\n```"
  
  channel = saved_channels[save_name]
  try:
    await channel.send(to_send)
  except discord.errors.Forbidden:
    await message.reply(f"Error: PsdwBot has insufficient permissions to view channel {format_channel(channel)}")


async def send_message_in_channel(cmd_parts, message, client):
  command = cmd_parts[0]
  space_index = message.content.index(command) + len(command)
  arguments = message.content[space_index + 1:]
  if " " not in arguments:
    await message.reply("Cannot send an empty message")
    return
  elif arguments.startswith(" "):
    await message.reply("Error: No save name provided")
    return

  channel_name, to_send = arguments.split(" ", 1)
  
  if channel_name.isdigit():
    channel_id = int(channel_name)
    channel = client.get_channel(channel_id)
  elif channel_name[:2] == "<#" and channel_name[-1] == ">" and channel_name[2:-1].isdigit():
    channel_id = int(channel_name[2:-1])
    channel = client.get_channel(channel_id)
  else:
    if channel_name[0] == "#":
      channel_name = channel_name[1:]
    channel = discord.utils.get(message.guild.channels, name=channel_name)
  
  if channel is None:
    await message.reply(f"Channel {channel_name} not found")
    return
  elif not isinstance(channel, discord.TextChannel):
    channel_type = type(channel).__name__
    channel_type = channel_type[:channel_type.index("Channel")]
    channel_type = channel_type.lower() + " channel"
    await message.reply("Cannot send a message in a " + channel_type)
    return
  
  try:
    await channel.send(to_send)
  except discord.errors.Forbidden:
    await message.channel.send(f"Error: PsdwBot has insufficient permissions to view channel {format_channel(channel)}")


def format_channel(channel):
  return f"#{channel.name} in {channel.guild.name} ({channel.mention})"


def initialise(client):
  global saved_channels
  
  saved = db.prefix("V")
  for save_name in saved:
    channel = client.get_channel(db.get(save_name))
    if channel != None:
      saved_channels[save_name[1:]] = channel
