from discord_ui import SelectMenu, SelectOption
from asyncio.exceptions import TimeoutError as AETimeoutError

from features_constants import features_basic, feature_texts, plushelp_msg


async def run(message, client):
  feature_options = [
    SelectOption(label="Basic Commands", value="cmds_basic"),
    SelectOption(label="General Commands", value="cmds_general"),
    SelectOption(label="Text Mangling Commands", value="cmds_text"),
    SelectOption(label="Text Generation Commands", value="cmds_textgen"),
    SelectOption(label="Currency-Related Commands", value="cmds_currency"),
    SelectOption(label="Channel-Related Commands", value="cmds_chans")
  ]
  
  features_menu = SelectMenu(
    options=feature_options, custom_id="features_menu", max_values=1
  )
  features_msg = await message.channel.send(
    features_basic + plushelp_msg, components=[features_menu]
  )

  await _run_internal(message, client, features_msg, features_menu)


async def _run_internal(message, client, features_msg, features_menu):
  try:
    sel = await features_msg.wait_for("select", client, by=message.author)
    selected = sel.selected_options[0].value
    new_features = feature_texts[selected]
    await sel.respond(ninja_mode=True)
    await features_msg.edit(new_features + plushelp_msg, components=[features_menu])
    await _run_internal(message, client, features_msg, features_menu)
  except AETimeoutError:
    await features_msg.edit(features_msg.content + "\n\nThis menu has expired.")
