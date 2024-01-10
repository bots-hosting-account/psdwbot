from discord_ui import Button

from asyncio.exceptions import TimeoutError as AETimeoutError


async def paginate_embed(client, message, e, fields, inline):
  await _send_paginated_embed(client, message, e, fields, inline, 0)

async def _send_paginated_embed(client, message, e, fields, inline, current_page, reply=None):
  items_per_page = 8
  last_page, last_count = divmod(len(fields), items_per_page)
  if last_count == 0:
    last_page -= 1

  e.clear_fields()
  for name, value in fields[current_page * items_per_page:(current_page + 1) * items_per_page]:
    e.add_field(name=name, value=value, inline=inline)

  e.set_footer(text=f"Page {current_page + 1} of {last_page + 1}")
  left_button = Button(color="blurple", emoji=client.get_emoji(1148446344403497050))
  right_button = Button(color="blurple", emoji=client.get_emoji(1148446357359689748))
  components = [left_button, right_button]

  if reply is None:
    reply = await message.reply(embed=e, components=components)
  else:
    await reply.edit(embed=e, components=components)
  try:
    btn = await reply.wait_for("button", client, by=message.author, timeout=20)
    await btn.respond(ninja_mode=True)

    if btn.component.custom_id == components[0].custom_id:
      current_page -= 1
      if current_page < 0:
        current_page = last_page
    else:
      current_page += 1
      if current_page > last_page:
        current_page = 0

    await _send_paginated_embed(client, message, e, fields, inline, current_page, reply)
  except AETimeoutError:
    components[0].disabled = True
    components[1].disabled = True
    await reply.edit(embed=e, components=components)
