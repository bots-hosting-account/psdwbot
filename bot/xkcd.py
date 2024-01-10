from discord_ui import Button
from asyncio.exceptions import TimeoutError as AETimeoutError
import urllib.request

def has_xkcd_hyphen(s):
  s = s.lower()
  return " ass " in s or "-ass " in s

def xkcd_hyphenate(s):
  s = s.lower().replace("-ass ", " ass ")
  w = s.split(" ass ", 1)
  il = w[0].rfind(" ")
  ir = w[1].find(" ")
  if ir == -1:
    ir = len(w[1])
  return f"{w[0][il + 1:]} ass-{w[1][:ir]}"


def get_random_xkcd():
  random_url = "https://c.xkcd.com/comic/random"
  comic_url = urllib.request.urlopen(random_url).url
  return comic_url

async def get_random_calvin_hobbes(message, client, original_user):
  random_url = "https://www.gocomics.com/random/calvinandhobbes"
  comic_url = urllib.request.urlopen(random_url).url
  button = Button(custom_id="cah", color="blurple", label="Next comic")
  comic_msg = await message.reply(comic_url, components=[button])
  
  try:
    clicked = await comic_msg.wait_for("button", client)
    button.color = "gray"
    button.disabled = True
    await clicked.respond(ninja_mode=True)
    await comic_msg.edit(content=comic_url, components=[button])
    await get_random_calvin_hobbes(comic_msg, client, original_user)
  except AETimeoutError:
    button.color = "gray"
    button.disabled = True
    await comic_msg.edit(content=comic_url, components=[button])

async def get_random_dilbert(message, client, original_user):
  random_url = "https://www.gocomics.com/random/dilbert-classics"
  comic_url = urllib.request.urlopen(random_url).url
  button = Button(custom_id="dilbert", color="blurple", label="Next comic")
  comic_msg = await message.reply(comic_url, components=[button])
  
  try:
    clicked = await comic_msg.wait_for("button", client)
    button.color = "gray"
    button.disabled = True
    await clicked.respond(ninja_mode=True)
    await comic_msg.edit(content=comic_url, components=[button])
    await get_random_dilbert(comic_msg, client, original_user)
  except AETimeoutError:
    button.color = "gray"
    button.disabled = True
    await comic_msg.edit(content=comic_url, components=[button])
