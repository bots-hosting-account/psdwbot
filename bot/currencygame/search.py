from discord_ui import Button

from random import randint, choice, sample

from asyncio.exceptions import TimeoutError as AETimeoutError

from .items import items, Holidays, holiday
from .basic import commit_to_database, ensure, add_money, format, add_item

search_dict = {
  "couch": "who knows what else is down there...",
  "floor": "good thing you haven't vacuumed in a while!",
  "moon": "thanks Elon",
  "ATM": "hopefully no one saw",
  "ocean": "maybe you can buy some dry clothes now"
}

search_dict_keys = list(search_dict.keys())

if holiday == Holidays.HALLOWEEN:
  search_dict_keys.extend(["graveyard"] * 2)
elif holiday == Holidays.NEW_YEARS_EVE:
  search_dict_keys.extend(["Times Square"] * 2)


def make_search_btn(s, i):
  pre = randint(1, 1000000)
  return Button(color="blurple", custom_id=f"{pre}search{i}", label=s)

async def search(message, client):
  uid = message.author.id
  ensure(uid)
  options = sample(search_dict_keys, 3)
  while len(options) != len(set(options)):
    options = sample(search_dict_keys, 3)

  btns = [make_search_btn(opt, i) for i, opt in enumerate(options)]

  search_msg = await message.reply("**Where do you want to search?**", components=btns)
  try:
    btn = await search_msg.wait_for("button", client, by=message.author, timeout=20)
    await btn.respond(ninja_mode=True)

    label = btn.component.label
    for button in btns:
      button.disabled = True
      if button.custom_id != btn.component.custom_id:
        button.color = "grey"

    if label == "graveyard":
      found = randint(50, 850)
      skeletons = choice((0, 1))
      pumpkins = choice((0, 0, 1, 1, 2))
      add_money(uid, found)
      add_item(uid, items["skeleton"], skeletons)
      add_item(uid, items["pumpkin"], pumpkins)
      new_text = f"You searched the {label} and found {format(found)}"
      if skeletons or pumpkins:
        new_text += ", and dug up "
        if pumpkins:
          new_text += f"{pumpkins}x {items['pumpkin']}"
          if skeletons:
            new_text += " and "
        if skeletons:
          new_text += f"{skeletons}x {items['skeleton']}"
      new_text += "."

    elif label == "Times Square":
      found = randint(200, 1500)
      add_money(uid, found)
      found_ball = randint(1, 2) == 1

      new_text = f"You searched {label} and found {format(found)}"
      if found_ball:
        time_ball_item = items["timeball"]
        add_item(uid, time_ball_item)
        new_text += f", as well as 1x {time_ball_item}"
      new_text += "."

    else:
      found = randint(5, 750)
      add_money(uid, found)
      new_text = f"You searched the {label} and got {format(found)}, {search_dict[label]}"
    
    commit_to_database()
    
    await search_msg.edit(new_text, components=btns)

  except AETimeoutError:
    pass
