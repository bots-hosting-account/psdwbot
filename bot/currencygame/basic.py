import discord

from replit import db

from .items import items, Holidays, holiday

#################################### Embed-related

if holiday == Holidays.HALLOWEEN:
  EMBED_COLOUR = 0xff7700
else:
  EMBED_COLOUR = 0x242424

#################################### Database-related

def commit_to_database():
  pass

#################################### UID-related

def ensure(uid):
  b_uid = "B" + str(uid)
  if b_uid not in db:
    db[b_uid] = "0"
    db[str(uid) + "Inewplayerpack"] = 1

def parse_uid(guild, string):
  if string.isdigit():
    return int(string)

  elif string[:2] == "<@" and string[-1] == ">" and string[2:-1].isdigit():
    return int(string[2:-1])

  elif string[:3] == "\\<@" and string[-1] == ">" and string[3:-1].isdigit():
    return int(string[3:-1])

  elif "#" in string:
    name, discriminator = string.split("#", 1)
    user = discord.utils.get(
      guild.members, name=name, discriminator=discriminator
    )
    return user.id if user else None

  else:
    user = discord.utils.get(guild.members, name=string)
    if user:
      return user.id
    else:
      return None

#################################### Money-related

def uid_has_money(uid):
  return "B" + str(uid) in db

def get_money(uid):
  if uid_has_money(uid):
    return int(db["B" + str(uid)])
  else:
    return 0

def add_money(uid, amt):
  ensure(uid)
  db["B" + str(uid)] = str(get_money(uid) + amt)

def set_money(uid, amt):
  ensure(uid)
  db["B" + str(uid)] = str(amt)

def format(amt):
  return f"֏{amt:,}"

#################################### Item-related

def get_item_id(string):
  if string in items:
    return string
  else:
    string = string.replace("_", "").lower()
    for item_id in items:
      item_name = items[item_id].name.replace(" ", "").lower()
      if string == item_name:
        return item_id
    return None

def user_has_item(uid, item_id):
  item_key = f"{uid}I{item_id}"
  return item_key in db

def add_item(uid, item, amount=1):
  itemuser_id = f"{uid}I{item.id}"
  if itemuser_id not in db:
    db[itemuser_id] = str(amount)
  else:
    old_amt = int(db[itemuser_id])
    db[itemuser_id] = str(old_amt + amount)

def remove_item(uid, item, number_to_remove=1):
  itemuser_id = f"{uid}I{item.id}"
  if itemuser_id in db:
    old_amt = int(db[itemuser_id])
    new_value = old_amt - number_to_remove
    if new_value == 0:
      del db[itemuser_id]
    else:
      db[itemuser_id] = str(new_value)

def get_item_count(uid, item_id):
  full_id = f"{uid}I{item_id}"
  if full_id in db:
    return int(db[full_id])
  else:
    return 0
