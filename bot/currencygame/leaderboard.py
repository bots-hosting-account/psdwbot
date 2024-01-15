from discord import Embed

from connect_database import connection

from .items import items
from .basic import EMBED_COLOUR, format


async def leaderboard(client, channel, users):
  message = await channel.send("Loading leaderboard...")
  
  with connection.cursor() as cursor:
    balances = tuple(cursor.execute("SELECT id, balance FROM balances"))
  user_ids_to_search = tuple(user.id for user in users)
  user_rows = list(row for row in balances if row[0] in user_ids_to_search)
  
  e = get_leaderboard_embed(client, user_rows, "Leaderboard")
  e.set_footer(text="To see the leaderboard based on net worth, use `+netrich`. To see the global leaderboard, use `+rich g`.")
  await message.edit("", embed=e)


async def net_worth_leaderboard(client, channel, users):
  message = await channel.send("Loading net worth leaderboard...")
  
  with connection.cursor() as cursor:
    balances = tuple(cursor.execute("SELECT id, balance FROM balances"))
  user_ids_to_search = tuple(user.id for user in users)
  user_rows = tuple(row for row in balances if row[0] in user_ids_to_search)
  found_user_ids = tuple(row[0] for row in user_rows)

  inventory_query = "SELECT userid, item, amount FROM inventory WHERE userid in ("
  inventory_query += ", ".join(f"'{int(uid)}'" for uid in found_user_ids)
  inventory_query += ")"
  with connection.cursor() as cursor:
    items = tuple(cursor.execute(inventory_query))
  item_index = 0

  user_net_worths = []
  for (uid, balance) in user_rows:
    net_worth = balance
    
    while item_index < len(items) and items[item_index][0] == uid:
      _, item_id, amount = items[item_index]
      net_worth += items[item_id].sell_price * amount
      item_index += 1
    
    user_net_worths.append((uid, net_worth))
  
  e = get_leaderboard_embed(client, user_net_worths, "Net Worth Leaderboard")
  e.set_footer(text="To see the leaderboard based on money only, use `+rich`. To see the global net worth leaderboard, use `+netrich g`.")
  await message.edit("", embed=e)


def get_leaderboard_embed(client, user_money_list, leaderboard_title):
  user_money_list.sort(key=lambda _, money: money, reverse=True)
  
  str_lb = "\n".join(
    f"**{format(money)}** — {client.get_user(uid).name}" for uid, money in user_money_list
  )
  
  e = Embed(title=leaderboard_title, description=str_lb, color=EMBED_COLOUR)
  return e
