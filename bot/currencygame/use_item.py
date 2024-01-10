from discord import Embed

from math import floor, sqrt
from random import random, randint, choice

from .items import items, Holidays, holiday
from .basic import (
  EMBED_COLOUR,
  commit_to_database,
  ensure,
  add_money, format,
  get_item_id, get_item_count, add_item, remove_item, user_has_item
)


async def use_item(cmd_parts, message):
  if len(cmd_parts) < 2:
    await message.reply("Usage: `+use item_id` or `+use item_id amount`")
    return

  uid = message.author.id
  ensure(uid)

  item_id = get_item_id("".join(cmd_parts[1:]))
  last_was_value = False

  if item_id is None:
    item_id = get_item_id("".join(cmd_parts[1:-1]))
    last_was_value = True

  if item_id is None:
    e = Embed(description="No such item exists.", color=EMBED_COLOUR)
    await message.reply(embed=e)
    return
  elif not user_has_item(uid, item_id):
    use_item = items[item_id]
    e = Embed(description=f"You do not have a {use_item} in your inventory.", color=EMBED_COLOUR)
    await message.reply(embed=e)
    return

  item_count_in_inv = None
  if last_was_value and len(cmd_parts) >= 3:
    if cmd_parts[-1].lower() in ("max", "all", "maximum"):
      uid = message.author.id
      item_count_in_inv = get_item_count(uid, item_id)
      requested_amount = item_count_in_inv
    elif cmd_parts[-1].isdigit():
      requested_amount = int(cmd_parts[-1])
      if requested_amount == 0:
        use_item = items[item_id]
        e = Embed(description=f"You cannot use 0x {use_item}, you must use at least one.", color=EMBED_COLOUR)
        await message.reply(embed=e)
        return
    else:
      await message.reply(f"Cannot use {cmd_parts[-1]}x {items[item_id]}. Please provide a valid amount of items (or none at all).")
      return
  else:
    requested_amount = 1

  if item_count_in_inv is None:
    uid = message.author.id
    item_count_in_inv = get_item_count(uid, item_id)

  if item_count_in_inv < requested_amount:
    use_item = items[item_id]
    e = Embed(description=f"You cannot use {requested_amount:,}x {use_item}, you only have {item_count_in_inv:,}.", color=EMBED_COLOUR)
    await message.reply(embed=e)
  elif item_id == "gift":
    await use_gift_box(message, uid, requested_amount)
  elif item_id == "newplayerpack":
    await use_new_player_pack(message, uid, requested_amount)
  elif item_id == "pumpkin":
    await use_pumpkin(message, uid, requested_amount)
  else:
    e = Embed(description="That cannot be used.", color=EMBED_COLOUR)
    await message.reply(embed=e)


async def use_gift_box(message, uid, requested_amount):
  item_id = "gift"
  used_item = items[item_id]

  e = Embed(description=f"Opening {requested_amount:,}x {used_item}...", color=EMBED_COLOUR)
  new_message = await message.reply(embed=e)

  embed_text = f"You opened {requested_amount:,}x {used_item} and found:"

  item_ids = tuple(items.keys())
  number_of_items = 0
  for _ in range(requested_amount):
    number_of_items += 9 - floor(sqrt(randint(1, 50)) * 1.2)

  found = tuple(choice(item_ids) for _ in range(number_of_items))
  found_dict = {}

  for found_name in set(found):
    found_dict[found_name] = found.count(found_name)

  sorted_keys = sorted(found_dict.keys(), key=lambda k: found_dict[k], reverse=True)

  for item_name in sorted_keys:
    found_item = items[item_name]
    amount = found_dict[item_name]
    embed_text += "\n" + "\u200b " * 3 + f"• {amount:,}x {found_item}"
    add_item(uid, found_item, amount)

  remove_item(uid, used_item, requested_amount)

  empty_box = items["box"]
  embed_text += f"\nYou also gained {requested_amount:,}x {empty_box}."
  add_item(uid, empty_box, requested_amount)
  
  commit_to_database()
  
  e = Embed(description=embed_text, color=EMBED_COLOUR)
  await new_message.edit(embed=e)


async def use_new_player_pack(message, uid, requested_amount):
  item_id = "newplayerpack"
  used_item = items[item_id]

  e = Embed(description=f"Opening {requested_amount:,}x {used_item}...", color=EMBED_COLOUR)
  new_message = await message.reply(embed=e)

  embed_text = f"You opened {requested_amount:,}x {used_item} and found:"

  found_item_ids = ("shovel", "rod", "rifle")

  for item_id in found_item_ids:
    found_item = items[item_id]
    embed_text += "\n" + "\u200b " * 3 + f"• {requested_amount}x {found_item}"
    add_item(uid, found_item, requested_amount)

  remove_item(uid, used_item, requested_amount)

  gained_money = 350 * requested_amount
  embed_text += f"\nYou also gained {format(gained_money)}."
  add_money(uid, gained_money)
  
  commit_to_database()
  
  e = Embed(description=embed_text, color=EMBED_COLOUR)
  await new_message.edit(embed=e)


async def use_pumpkin(message, uid, requested_amount):
  gained_money = 0
  for i in range(requested_amount):
    gained_money += 550 - floor(sqrt(random() * 160000))

  if holiday == Holidays.HALLOWEEN:
    gained_money *= randint(3, 7)

  s = "" if requested_amount == 1 else "s"
  embed_text = f"You went trick-or-treating {requested_amount:,} time{s} and found {format(gained_money)}."
  add_money(uid, gained_money)
  dropped_pumpkins = randint(0, requested_amount)
  if dropped_pumpkins > 0:
    pumpkin = items["pumpkin"]
    embed_text += f" Unfortunately, you dropped {dropped_pumpkins:,}x {pumpkin}."
    add_item(uid, pumpkin, -dropped_pumpkins)
  
  commit_to_database()
  
  e = Embed(description=embed_text, color=EMBED_COLOUR)
  await message.reply(embed=e)
