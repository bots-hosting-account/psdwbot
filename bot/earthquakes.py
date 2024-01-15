import discord
import urllib.request

url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.csv"

def get_lines():
  page = urllib.request.urlopen(url)
  charset = page.headers.get_content_charset()
  return page.read().decode(charset).split("\n")

def get_earthquake_data(line):
  date = line[:10]
  time = line[11:19]
  info = line[line.index('"') + 1:line.rindex('"')]
  mag = line.split(",")[4]
  return(f"{time} {date} — magnitude {mag}, {info}")

def get_n_earthquakes(n):
  lines = get_lines()
  data = []
  for i in range(n):
    line = lines[i + 1]
    data.append(get_earthquake_data(line))
  return data

def get_max_earthquakes():
  lines = get_lines()
  data = []
  total_len = 0
  i = 0
  while total_len <= 2000:
    line = lines[i + 1]
    dt = get_earthquake_data(line)
    data.append(dt)
    total_len += len(dt) + 1
    i += 1
  if total_len > 2000:
    data.pop()
  return data


async def send_message(cmd_parts, message):
  if len(cmd_parts) >= 2 and cmd_parts[1].isdigit():
    n_quakes = int(cmd_parts[1]) or 5
    quakes_str = "\n".join(get_n_earthquakes(n_quakes))
  else:
    quakes_str = "\n".join(get_max_earthquakes())
  
  try:
    await message.channel.send(quakes_str)
  
  except discord.errors.HTTPException:
    excess = len(quakes_str) - 2000
    character_s = "character" if excess == 1 else "characters"
    await message.channel.send(f"Message was {excess} {character_s} too long. Please request fewer earthquakes, the maximum is usually around 30.")
  
  except Exception as e:
    await message.channel.send("An error occured. Please try again or request fewer earthquakes.")
    raise e
