from datetime import datetime

class _Holiday:
  def __init__(self, name, emoji, start, end, effects):
    self.str = emoji + " " + name
    if end is None:
      self.active = f"on {start[0]}/{start[1]}"
    else:
      self.active = f"from {start[0]}/{start[1]}"
      self.active += f" to {end[0]}/{end[1]}"
    self.effects = effects
  
  def format_effects(self, item):
    item_str = str(item)
    self.effects = tuple(effect.format(item_str) for effect in self.effects)
  
  def get_active(self):
    return self.active
  
  def __str__(self):
    return self.str

class Holidays:
  HALLOWEEN = _Holiday("Halloween", ":jack_o_lantern:", (10, 25), (10, 31), ["{}s have an increased chance to spawn", "Using {}s gives an increased payout", "Embeds are coloured appropriately", "Graveyards can be searched"])
  MOLE_DAY = _Holiday("Mole Day", ":mole:", (10, 23), None, ["{}s have an increased chance to spawn"])
  NEW_YEARS_EVE = _Holiday("New Year's Eve", ":mirror_ball:", (12, 31), None, ["Times Square can be searched"])

today = datetime.now()
if today.month == 10 and today.day == 23:
  holiday = Holidays.MOLE_DAY
elif today.month == 10 and today.day >= 25:
  holiday = Holidays.HALLOWEEN
elif today.month == 12 and today.day == 31:
  holiday = Holidays.NEW_YEARS_EVE
else:
  holiday = None


class Item:
  def __init__(self, id, name, sell_price, emoji, description, *, buy_price=None, can_be_used=False):
    self.id = id
    self.name = name
    self.sell_price = sell_price
    self.emoji = emoji
    self.description = description
    self.buy_price = buy_price
    self.can_be_used = can_be_used
  
  def __str__(self):
    return f"{self.emoji} **{self.name}**"

items = {
  "fly": Item("fly", "Fly", 25, ":fly:", "Shoo fly, don't bother me!"),
  "sand": Item("sand", "Sand", 50, "<:sandPile:1143663440662106152>", "There isn't much else to say about it."),
  "newplayerpack": Item("newplayerpack", "New Player Pack", 150, ":envelope:", "`+use` this item to get some money and some useful starting items.", can_be_used=True),
  "salt": Item("salt", "Rock Salt", 200, "<:rocksalt:1131398485762125855>", "Better than storing plaintext."),
  "pumpkin": Item("pumpkin", "Pumpkin", 500, ":jack_o_lantern:", "Finally the right season for this." if holiday == Holidays.HALLOWEEN else "What season is it again?", can_be_used=True),
  "box": Item("box", "Empty Box", 1000, ":package:", "It no longer contains unknown treasure.", buy_price=1500),
  "duck": Item("duck", "Duck", 4500, ":duck:", "Real ducks don't catch as many bugs."),
  "mole": Item("mole", "Mole", 5000, "<:mole:1143666285964701737>", "Or maybe it's a vole."),
  "boarhead": Item("boarhead", "Boar Head", 5800, ":boar:", "Just the head."),
  "shovel": Item("shovel", "Shovel", 3000, "<:shovel:1143689018018631681>", "Good for digging with.", buy_price=5500),
  "rod": Item("rod", "Fishing Rod", 4000, ":fishing_pole_and_fish:", "Now all that's missing is John.", buy_price=6000),
  "dagger": Item("dagger", "Dagger", 3000, ":dagger:", "Makes people think twice before `+rob`bing you.", buy_price=6500),
  "rifle": Item("rifle", "Hunting Rifle", 4500, "<:hunt:1143767520151621672>", "Comes with unbounded ammunition.", buy_price=7000),
  "herring": Item("herring", "Red Herring", 4850, "<:RedHerring:1148460599391572008>", "Distracts you from more important fish."),
  "globe": Item("globe", "Globe", 5000, ":earth_africa:", "Shows at least two continents.", buy_price=8000),
  "gift": Item("gift", "Gift Box", 10_000, ":gift:", "It contains unknown treasure.", can_be_used=True),
  "shark": Item("shark", "Shark", 12_500, ":shark:", "EF, EF, EF, EF..."),
  "skeleton": Item("skeleton", "Skeleton", 25_000, ":skull:", "Fresh from the graveyard."),
  "timeball": Item("timeball", "Time Ball", 50_000, ":mirror_ball:", "Straight from Times Square."),
  "car": Item("car", "Car", 6_000_000, ":red_car:", "It had better fly.", buy_price=11_000_000),
  "macguffin": Item("macguffin", "MacGuffin", 50_000_000, ":sandwich:", "It doesn't matter exactly what it is.")
}

shop_items = tuple(kv[0] for kv in sorted(((k, v) for k, v in items.items() if v.buy_price != None), key=lambda kv: kv[1].buy_price))

def make_rewards(tuples):
  rewards = []
  for item, rarity in tuples:
    rewards.extend([item] * rarity)
  return rewards


if holiday == Holidays.MOLE_DAY:
  dig_rewards = make_rewards((("mole", 1),))
  Holidays.MOLE_DAY.format_effects(items["mole"])
else:
  dig_rewards = make_rewards((
    ("sand", 3), ("pumpkin", 3), ("mole", 3), ("gift", 1), ("salt", 2), ("globe", 1)
  ))
  if holiday == Holidays.HALLOWEEN:
    dig_rewards.extend(["pumpkin"] * 7)
    Holidays.HALLOWEEN.format_effects(items["pumpkin"])

fish_rewards = make_rewards((
  ("salt", 2), ("duck", 3), ("rod", 2), ("car", 1), ("herring", 3), ("shark", 2), (None, 2)
))

hunt_rewards = make_rewards((
  ("fly", 3), ("duck", 2), ("boarhead", 2), ("car", 1), (None, 2)
))
