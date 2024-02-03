import discord

from connect_database import connection

from .items import items, Holidays, holiday

#################################### Embed-related

if holiday == Holidays.HALLOWEEN:
  EMBED_COLOUR = 0xff7700
else:
  EMBED_COLOUR = 0x242424

#################################### Database-related

def commit_to_database():
  connection.commit()

#################################### UID-related

def ensure(uid):
  with connection.cursor() as cursor:
    uid_str = str(uid)
    count_row = tuple(cursor.execute("SELECT COUNT(*) FROM balances WHERE id = :id", id=uid_str))
    if count_row[0] == 0:
      cursor.execute("INSERT INTO balances (id, balance) VALUES (:id, 0)", id=uid_str)
      cursor.execute("INSERT INTO inventory (userid, item, amount) VALUES (:id, 'newplayerpack', 1)", id=uid_str)
      commit_to_database()

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

def get_money(uid):
  with connection.cursor() as cursor:
    cursor.execute("SELECT balance FROM balances WHERE id = :id", id=str(uid))
    row = cursor.fetchone()
  return row[0] if row is not None else 0

def add_money(uid, amt):
  ensure(uid)
  with connection.cursor() as cursor:
    cursor.execute("UPDATE balances SET balance = balance + :amount WHERE id = :id", amount=amt, id=str(uid))
  commit_to_database()

def set_money(uid, amt):
  ensure(uid)
  with connection.cursor() as cursor:
    cursor.execute("UPDATE balances SET balance = :amount WHERE id = :id", amount=amt, id=str(uid))
  commit_to_database()

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

def user_has_item(uid, item):
  with connection.cursor() as cursor:
    count_row = tuple(cursor.execute("SELECT COUNT(*) FROM inventory WHERE userid = :id AND item = :item", id=str(uid), item=item.id))
  return count_row[0] == 1

def add_item(uid, item, amount=1):
  with connection.cursor() as cursor:
    if user_has_item(uid, item):
      cursor.execute("UPDATE inventory SET amount = amount + :amount WHERE userid = :id AND item = :item", amount=amount, id=str(uid), item=item.id)
    else:
      cursor.execute("INSERT INTO inventory (userid, item, amount) VALUES (:id, :item, :amount)", id=str(uid), item=item.id, amount=amount)
  commit_to_database()

def remove_item(uid, item, number_to_remove=1):
  with connection.cursor() as cursor:
    row = tuple(cursor.execute("SELECT amount FROM inventory WHERE userid = :id AND item = :item", id=str(uid), item=item.id))
    old_amount = row[0]
    new_amount = max(old_amount - number_to_remove, 0)
    cursor.execute("UPDATE inventory SET amount = :amount WHERE userid = :id AND item = :item", amount=new_amount, id=str(uid), item=item.id)
  commit_to_database()

def get_item_count(uid, item):
  with connection.cursor() as cursor:
    cursor.execute("SELECT amount FROM inventory WHERE userid = :id AND item = :item", id=str(uid), item=item.id)
    row = cursor.fetchone()
  return row[0] if row is not None else 0
