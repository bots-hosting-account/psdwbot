from discord import Embed

from replit import db

from .items import items
from .basic import EMBED_COLOUR, format


async def leaderboard(channel, users):
  message = await channel.send("Loading leaderboard...")
  b_prefix = db.prefix("B")

  user_and_bals = [
    (user, int(db[f"B{user.id}"])) for user in users if f"B{user.id}" in b_prefix
  ]
  e = get_leaderboard_embed(user_and_bals, "Leaderboard")
  e.set_footer(text="To see the leaderboard based on net worth, use `+netrich`. To see the global leaderboard, use `+rich g`.")
  await message.edit("", embed=e)


async def net_worth_leaderboard(channel, users):
  message = await channel.send("Loading net worth leaderboard...")
  b_prefix = db.prefix("B")

  user_and_bals = []
  for user in users:
    net_worth = 0
    user_in_system = False

    if f"B{user.id}" in b_prefix:
      user_in_system = True
      net_worth += int(db[f"B{user.id}"])

      for inv_entry in db.prefix(f"{user.id}I"):
        item = items[inv_entry.split("I")[1]]
        count_in_inv = int(db[inv_entry])
        item_value = count_in_inv * item.sell_price
        net_worth += item_value

    if net_worth > 0 or user_in_system:
      user_and_bals.append((user, net_worth))

  e = get_leaderboard_embed(user_and_bals, "Net Worth Leaderboard")
  e.set_footer(text="To see the leaderboard based on money only, use `+rich`. To see the global net worth leaderboard, use `+netrich g`.")
  await message.edit("", embed=e)


def get_leaderboard_embed(user_and_bals, leaderboard_title):
  #Sort by balances
  user_and_bals.sort(key=lambda u_b: u_b[1], reverse=True)
  
  str_lb = "\n".join(
    f"**{format(bal)}** — {user.name}" for user, bal in user_and_bals
  )

  e = Embed(title=leaderboard_title, description=str_lb, color=EMBED_COLOUR)
  return e
