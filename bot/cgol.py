from discord_ui import Button
from asyncio.exceptions import TimeoutError as AETimeoutError
from discord import Embed
import conway_life

WIDTH = 8
HEIGHT = 6

BOARD_FORMAT_STRING = ("```╔" + "══" * WIDTH + "╗\n" +
                       "║{}║\n" * HEIGHT +
                       "╚" + "══" * WIDTH + "╝```")

def get_rows(board):
  return [board[i * WIDTH:i * WIDTH + WIDTH] for i in range(HEIGHT)]

def format_row(row):
  return "".join("██" if cell else "  " for cell in row)

def format_board(board):
  board_rows = get_rows(board)
  return BOARD_FORMAT_STRING.format(*map(format_row, board_rows))

def encode(board) -> int:
  return sum(2 ** i for i in range(WIDTH * HEIGHT) if board[i])

def decode(encoded: int):
  return [bool(encoded & (2 ** i)) for i in range(WIDTH * HEIGHT)]

async def run(message, client, pos, cgol_msg=None):
  start = decode(pos)
  end = [False] * WIDTH * HEIGHT
  
  conway_life.run(WIDTH, HEIGHT, 0, 1, start, end, None)
  
  end_pos = encode(end)
  board = format_board(end)
  
  embed = Embed(title="Conway's Game of Life", description=board)
  embed.set_footer(text=f"To show the next step, type +cgol {end_pos}")

  button = Button(custom_id="cgolnext", color="blurple", label="Next step")
  
  if cgol_msg == None:
    cgol_msg = await message.reply(embed=embed, components=[button])
  else:
    await cgol_msg.edit(embed=embed,components=[button])
  
  try:
    clicked = await cgol_msg.wait_for("button", client, by=message.author)
    await clicked.respond(ninja_mode=True)
    await run(message, client, end_pos, cgol_msg)
  except AETimeoutError:
    button.color = "gray"
    button.disabled = True
    await cgol_msg.edit(embed=embed, components=[button])

