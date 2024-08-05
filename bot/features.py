import random

from discord_ui import SelectMenu, SelectOption
from asyncio.exceptions import TimeoutError as AETimeoutError

from features_constants import features_basic, feature_texts, plushelp_msg


async def run(message, client, recurring=False):
  global features_msg, feature_options

  pre = random.randint(1, 1000000)
  feature_options = [
    SelectOption(label="Basic Commands", value=f"{pre}cmds_basic"),
    SelectOption(label="General Commands", value=f"{pre}cmds_general"),
    SelectOption(label="Text Mangling Commands", value=f"{pre}cmds_text"),
    SelectOption(label="Text Generation Commands", value=f"{pre}cmds_textgen"),
    SelectOption(label="Currency-Related Commands", value=f"{pre}cmds_currency"),
    SelectOption(label="Channel-Related Commands", value=f"{pre}cmds_chans")
  ]
  
  sm = SelectMenu(
    options=feature_options, custom_id="features_menu", max_values=1
  )
  if not recurring:
    features_msg = await message.channel.send(
      features_basic + plushelp_msg, components=[sm]
    )
  
  try:
    sel = await features_msg.wait_for("select", client, by=message.author)
    selected = sel.selected_options[0].value
    new_features = feature_texts[selected]
    await sel.respond(ninja_mode=True)
    await features_msg.edit(new_features + plushelp_msg, components=[sm])
    await run(message, client, True)
  except AETimeoutError:
    await features_msg.edit(features_msg.content + "\n\nThis menu has expired.")
