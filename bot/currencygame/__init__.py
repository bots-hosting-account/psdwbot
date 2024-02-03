import discord
from discord import Embed

from random import random, randint, choice
from math import floor

from connect_database import connection

from .items import (
  holiday,
  items, shop_items,
  dig_rewards, fish_rewards, hunt_rewards
)
from .basic import (
  EMBED_COLOUR,
  commit_to_database,
  ensure, parse_uid,
  get_money, add_money, set_money, format,
  get_item_id, add_item, user_has_item, get_item_count
)
from .paginate_embed import paginate_embed

from .buy_sell import buy, sell
from .leaderboard import leaderboard, net_worth_leaderboard
from .search import search
from .use_item import use_item

#################################### beg

async def beg(message):
  uid = message.author.id
  ensure(uid)

  if randint(1, 4) > 1:
    gained_money = randint(10, 500)
    add_money(uid, gained_money)
    commit_to_database()
    reward_str = format(gained_money)
  else:
    reward_str = choice(("a slap to the face", "the side-eye"))
  
  await message.reply(f"You begged and somebody gave you {reward_str}.")

#################################### gamble

async def gamble(cmd_parts, message):
  if len(cmd_parts) < 2:
    await message.reply(f"You have to specify an amount to {cmd_parts[0]}.")
    return
  
  uid = message.author.id
  amount_to_bet = cmd_parts[1]
  
  if amount_to_bet.isdigit():
    at_stake = int(amount_to_bet)
    player_money = get_money(message.author.id)
    if at_stake > player_money:
      await message.reply(f"You can't bet {format(at_stake)}, you only have {format(player_money)}.")
  
  elif amount_to_bet in ("max", "all", "maximum"):
    at_stake = get_money(message.author.id)
  
  else:
    await message.reply(f"'{amount_to_bet}' is not a valid amount.")
    return
  
  payout, amount_won = get_payout_and_money(uid, at_stake)
  add_money(uid, amount_won)
  commit_to_database()
  money = format(abs(amount_won))
  if payout <= 2:
    await message.reply(f"Your lucky numbers didn't appear today and you lost {money}!")
  elif payout <= 4:
    await message.reply(f"You won a small prize of {money}.")
  elif payout <= 6:
    await message.reply(f"You won a modest prize of {money}.")
  else:
    await message.reply(f"You hit the jackpot and won {money}!")

def get_payout_and_money(uid, amt):
  ensure(uid)
  payout = randint(0, 7)
  won = 0
  if payout <= 2:
    #Lose
    won = -100
  elif payout <= 4:
    #Small payout
    won = randint(1, 30)
  elif payout <= 6:
    #Medium payout
    won = randint(31, 75)
  else:
    #Large payout
    won = randint(76, 100)
  amt = round(won / 100 * amt)
  return payout, amt

#################################### balance

async def balance(message, cmd_parts, client, net_worth=False):
  if len(cmd_parts) > 1:
    given_name = " ".join(cmd_parts[1:])
    uid = parse_uid(message.guild, given_name)
    gave_valid_uid = (uid is not None)
  else:
    uid = message.author.id
    gave_valid_uid = True

  if gave_valid_uid:
    money = get_money(uid)
    if net_worth:
      with connection.cursor() as cursor:
        items = cursor.execute("SELECT item, amount FROM inventory WHERE userid = :id", id=str(uid))
        for (item_id, amount) in items:
          money += items[item_id].sell_price * amount
    
    if uid == message.author.id:
      msg = f"You have {format(money)}."
    else:
      msg = client.get_user(uid).name + f" has {format(money)}."
  else:
    msg = f"The user '{given_name}' does not exist or is not in this server."
  await message.reply(msg)

#################################### shop, items

async def shop(message, client):
  e = Embed(title="Shop", color=EMBED_COLOUR)
  
  fields = []
  for item_id in shop_items:
    item = items[item_id]
    name = f"{item} — ֏{item.buy_price:,}"
    value = f"ID: `{item.id}`"
    fields.append((name, value))

  await paginate_embed(client, message, e, fields, False)

async def view_items(message, client):
  e = Embed(title="All Items", color=EMBED_COLOUR)

  sorted_items = sorted(((item_id, items[item_id].name) for item_id in items), key=lambda id_name: id_name[1])

  fields = []
  for item_id, _item_name in sorted_items:
    name = str(items[item_id])
    value = f"ID: `{item_id}`"
    fields.append((name, value))

  await paginate_embed(client, message, e, fields, False)

#################################### event_message

async def event_message(message):
  if holiday is None:
    description = "There is currently no active event."
  else:
    description = f"The current event is **{holiday}** (active {holiday.get_active()}).\n\nEffects:"
    for effect in holiday.effects:
      description += "\n* " + effect
  
  embed = Embed(title="Event", description=description, color=EMBED_COLOUR)
  await message.reply(embed=embed)

#################################### inventory

async def inventory(cmd_parts, message, client):
  gave_uid = len(cmd_parts) > 1
  if gave_uid:
    given_user = " ".join(cmd_parts[1:])
    uid = parse_uid(message.guild, given_user)
    if uid is None:
      await message.reply(f"The user '{cmd_parts[1]}' does not exist or is not in this server.")
      return
  else:
    uid = message.author.id
  
  await _send_inventory_message(uid, message, client)

async def _send_inventory_message(uid, message, client):
  username = discord.utils.get(client.users, id=uid).name
  inv = get_inv_data(uid)
  e = Embed(title=username + "'s Inventory", color=EMBED_COLOUR)

  if len(inv) == 0:
    owner_name = "your" if uid == message.author.id else (username + "'s")
    e.add_field(name="Nothing is here", value=f"There is nothing in {owner_name} inventory.", inline=False)
    await message.reply(embed=e)
  else:
    inv.sort(key=lambda item_and_amount: item_and_amount[0].name)
    fields = []
    for item, amount in inv:
      name = f"{item} — {amount:,}"
      value = f"ID: `{item.id}`"
      fields.append((name, value))

  await paginate_embed(client, message, e, fields, False)

def get_inv_data(uid):
  with connection.cursor() as cursor:
    item_rows = tuple(cursor.execute("SELECT item, amount FROM inventory WHERE userid = :id", id=str(uid)))
  return [(item_rows[item_id], amount) for item_id, amount in item_rows]

#################################### dig, hunt, fish

async def dig(message):
  uid = message.author.id
  ensure(uid)

  if user_has_item(uid, "shovel"):
    reward = items[choice(dig_rewards)]
    embed_text = f"You dug and brought back 1x {reward}."
    add_item(uid, reward)
    commit_to_database()
  else:
    embed_text = "You do not have a shovel."

  e = Embed(description=embed_text, color=EMBED_COLOUR)
  await message.reply(embed=e)

async def fish(message):
  uid = message.author.id
  ensure(uid)

  if user_has_item(uid, "rod"):
    reward_id = choice(fish_rewards)
    if reward_id is None:
      embed_text = "You must have gone fishing in [Lake Disappointment](https://en.wikipedia.org/wiki/Kumpupintil_Lake), you brought back nothing!"
    else:
      reward = items[reward_id]
      embed_text = f"You fished and brought back 1x {reward}."
      add_item(uid, reward)
      commit_to_database()
  else:
    embed_text = "You do not have a fishing rod."

  e = Embed(description=embed_text, color=EMBED_COLOUR)
  await message.reply(embed=e)

async def hunt(message):
  uid = message.author.id
  ensure(uid)

  if user_has_item(uid, "rifle"):
    reward_id = choice(hunt_rewards)
    if reward_id is None:
      embed_text = "You failed to kill anything while hunting!"
    else:
      reward = items[reward_id]
      embed_text = f"You hunted successfully and brought back 1x {reward}."
      add_item(uid, reward)
      commit_to_database()
  else:
    embed_text = "You do not have a hunting rifle."

  e = Embed(description=embed_text, color=EMBED_COLOUR)
  await message.reply(embed=e)

#################################### view_item

async def view_item(cmd_parts, message):
  if len(cmd_parts) < 2:
    await message.reply("Usage: `+item item_id`")
    return

  uid = message.author.id
  ensure(uid)

  item_id = get_item_id("".join(cmd_parts[1:]))

  if item_id is None:
    e = Embed(description="No such item exists.", color=EMBED_COLOUR)
    await message.reply(embed=e)
    return

  item = items[item_id]

  count_in_inv = get_item_count(uid, item_id)

  embed_text = "> " + item.description

  e = Embed(title=str(item), description=embed_text, color=EMBED_COLOUR)

  e.add_field(name="", value=f"ID: `{item.id}`", inline=False)

  embed_text = f"You own **{count_in_inv:,}**"
  if count_in_inv > 0:
    total_worth = item.sell_price * count_in_inv
    embed_text += f" (worth {format(total_worth)} in total)"
  embed_text += "."

  e.add_field(name="", value=embed_text, inline=False)

  embed_text = "**Additional Information**\n"
  if item_id in shop_items:
    embed_text += "\u200b " * 3 + f"• Can be bought for {format(item.buy_price)}\n"
  embed_text += "\u200b " * 3 + f"• Can be sold for {format(item.sell_price)}"
  if item.can_be_used:
    embed_text += "\n" + "\u200b " * 3 + "• Can be `+use`d"

  e.add_field(name="", value=embed_text, inline=False)

  await message.reply(embed=e)

#################################### rob

async def rob(cmd_parts, message):
  if len(cmd_parts) < 2:
    await message.reply("Usage: `+rob user`")
    return

  robber_uid = message.author.id
  ensure(robber_uid)

  if get_money(robber_uid) < 500:
    await message.reply(f"You must have at least {format(500)} to rob somebody.")
    return

  target = " ".join(cmd_parts[1:])
  target_uid = parse_uid(message.guild, target)
  if target_uid is None:
    await message.reply(f"The user '{target}' does not exist or is not in this server.")
    return

  target_name = message.guild.get_member(target_uid).name
  if get_money(target_uid) > 0:
    target_has_dagger = user_has_item(target_uid, "dagger")
    if target_has_dagger and randint(1, 3) == 1:
      await message.reply(f"You saw {target_name}'s dagger and thought twice about your planned robbery!")
      return

    target_money = get_money(target_uid)
    if randint(1, 8) > 3:
      if target_has_dagger and randint(1, 2) == 1:
        dropped = randint(1, 500)
        add_money(robber_uid, -dropped)
        commit_to_database()
        await message.reply(f"You got pricked by {target_name}'s dagger and dropped {format(dropped)}!")
        return

      luck = randint(1, 15)
      if luck < 2:
        percent = (1 - random()) * 100
      elif luck < 5:
        percent = (1 - random()) * 50
      elif luck < 8:
        percent = (1 - random()) * 20
      else:
        percent = (1 - random()) * 8
      stolen = floor(percent * 0.01 * target_money)
      add_money(robber_uid, stolen)
      add_money(target_uid, -stolen)
      await message.reply(f"You successfully robbed {target_name} and stole {format(stolen)} ({round(percent, 1)}%)!")
    
    else:
      await message.reply(f"You were caught while attempting to rob {target_name} and paid a fine of {format(500)}!")
      add_money(robber_uid, -500)
    
    commit_to_database()
  
  else:
    await message.reply(f"{target_name} does not have any money!")
