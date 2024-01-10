from discord import Embed
from discord_ui import Button
from asyncio.exceptions import TimeoutError as AETimeoutError

import random

def edge(n):
  return n == 0 or n == 4

async def run(message, client):
  channel = message.channel
  e = Embed(title="Stupid Minesweeper", description="Mine a square to begin.", color=0x000000)
  comp = []
  
  for i in range(5):
    comp.append([])
    for j in range(5):
      pre = random.randint(1, 1000000)
      id = f"{pre}StupidMinesweeper{i}{j}"
      btn = Button("?", custom_id=id, color="blurple")
      comp[i].append(btn)
  
  m = await channel.send(embed=e, components=comp)
  try:
    btn = await m.wait_for("button", client, by=message.author, timeout=20)
    i = int(btn.custom_id[-2])
    j = int(btn.custom_id[-1])
    await mine(i, j, m, btn)
  except AETimeoutError:
    for i in range(5):
      for j in range(5):
        comp[i][j].color = "grey"
        comp[i][j].disabled = True
    await m.edit(embed=e, components=comp)

async def mine(x, y, message, btn):
  cmp = message.components
  
  for i in range(25):
    cmp[i].label = "\U0001f6a9"
    cmp[i].color = "green"
    cmp[i].disabled = True
  
  if edge(x) and edge(y):
    n = "3"
  elif edge(x) or edge(y):
    n = "5"
  else:
    n = "8"
  cmp[x * 5 + y].label = n
  cmp[x * 5 + y].color = "red"
  
  e = Embed(title="Stupid Minesweeper", description="You win!", color=0x000000)
  await message.edit(embed=e, components=cmp)
  await btn.respond(ninja_mode=True)
