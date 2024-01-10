from discord import Embed

from .items import items, shop_items
from .basic import (
  EMBED_COLOUR,
  commit_to_database,
  get_money, add_money, format,
  get_item_id, get_item_count, add_item, remove_item
)


async def buy(cmd_parts, message):
  if len(cmd_parts) < 2:
    await message.reply("Usage: `+buy item_id` or `+buy item_id amount`")
    return

  item_id = get_item_id("".join(cmd_parts[1:]))
  last_was_value = False

  if item_id is None:
    item_id = get_item_id("".join(cmd_parts[1:-1]))
    last_was_value = True

  if item_id is None:
    await message.reply("No such item exists.")
    return
  elif item_id not in shop_items:
    await message.reply("The requested item is not available to be bought.")
    return

  uid = None
  if last_was_value and len(cmd_parts) >= 3:
    if cmd_parts[-1].lower() in ("max", "all", "maximum"):
      uid = message.author.id
      user_money = get_money(uid)
      item = items[item_id]
      max_buy = max(user_money // item.buy_price, 0)
      amount = max_buy
    elif cmd_parts[-1].isdigit():
      amount = int(cmd_parts[-1])
    else:
      await message.reply(f"Cannot buy {cmd_parts[-1]}x {items[item_id]}. Please provide a valid amount of items (or none at all).")
      return
  else:
    amount = 1

  if uid is None:
    uid = message.author.id
    user_money = get_money(uid)
    item = items[item_id]
    max_buy = max(user_money // item.buy_price, 0)

  if amount <= max_buy:
    total_price = item.buy_price * amount
    fmt_price = format(total_price)
    e = Embed(description=f"{message.author.mention} bought {amount:,}x {item} and paid {fmt_price}", color=EMBED_COLOUR)
    e.set_author(name="Successful purchase", icon_url=message.author.avatar_url)
    e.set_footer(text="Thanks for your purchase!")

    if amount > 0:
      add_money(uid, -total_price)
      add_item(uid, item, amount)
      commit_to_database()
  
  else:
    max_buy = max(user_money // item.buy_price, 0)
    e = Embed(description=f"You cannot buy {amount:,}x {item}, you can only buy {max_buy:,}.", color=EMBED_COLOUR)
    e.set_author(name="Unsuccessful purchase", icon_url=message.author.avatar_url)
    e.set_footer(text="You are too poor")

  await message.reply(embed=e)

async def sell(cmd_parts, message):
  if len(cmd_parts) < 2:
    await message.reply("You have to specify something to sell.")
    return

  item_id = get_item_id("".join(cmd_parts[1:]))
  last_was_value = False

  if item_id is None:
    item_id = get_item_id("".join(cmd_parts[1:-1]))
    last_was_value = True

  if item_id is None:
    await message.reply("No such item exists.")
    return

  item_count = None
  if last_was_value and len(cmd_parts) >= 3:
    if cmd_parts[-1].lower() in ("max", "all", "maximum"):
      uid = message.author.id
      item_count = get_item_count(uid, item_id)
      amount = item_count
    elif cmd_parts[-1].isdigit():
      amount = int(cmd_parts[-1])
    else:
      await message.reply(f"Cannot sell {cmd_parts[-1]}x {items[item_id]}. Please provide a valid amount of items (or none at all).")
      return
  else:
    amount = 1

  item = items[item_id]

  total_profit = item.sell_price * amount

  if item_count is None:
    uid = message.author.id
    item_count = get_item_count(uid, item_id)

  if item_count >= amount:
    fmt_profit = format(total_profit)
    e = Embed(description=f"{message.author.mention} sold {amount:,}x {item} and received {fmt_profit}", color=EMBED_COLOUR)
    e.set_author(name="Successful sale", icon_url=message.author.avatar_url)

    if amount > 0:
      add_money(uid, total_profit)
      remove_item(uid, item, amount)
      commit_to_database()
  
  else:
    e = Embed(description=f"You cannot sell {amount:,}x {item}, you can only sell {item_count:,}.", color=EMBED_COLOUR)
    e.set_author(name="Unsuccessful sale", icon_url=message.author.avatar_url)
    e.set_footer(text="You are too poor")

  await message.reply(embed=e)
