from discord_ui import ActionRow, Button, SelectMenu

import markov


async def send_message(cmd_parts, message, is_word):
  markov_function = markov.word if is_word else markov.sentence
  has_maximum = len(cmd_parts) >= 2 and markov.is_valid_max(cmd_parts[1])
  
  if len(cmd_parts) < (3 if has_maximum else 2):
    if message.reference is None or not message.reference.resolved:
      command = cmd_parts[0]
      await message.channel.send(f"Usage: `+{command} text` or `+{command} !max text`\nWhen replying to a message: `+{command}` or `+{command} !max`\nTry `+help {command}` for more information.")
      return
    
    replied_id = message.reference.message_id
    old_message = await message.channel.fetch_message(replied_id)
    
    texts = [old_message.content] if old_message.content else []
    if len(old_message.embeds) > 0:
      old_embed = old_message.embeds[0]
      if old_embed.title:
        texts.append(old_embed.title)
      if old_embed.description:
        texts.append(old_embed.description)
      if old_embed.author:
        texts.append(old_embed.author.name)
      if old_embed.footer:
        texts.append(old_embed.footer.text)
      if old_embed.fields:
        for field in old_embed.fields:
          texts.append(field.name)
          texts.append(field.value)

    if len(old_message.components) > 0:
      for component in old_message.components:
        if isinstance(component, ActionRow):
          for item in component.children:
            if isinstance(item, Button):
              if item.label:
                texts.append(item.label)
            elif isinstance(item, SelectMenu):
              for option in item.options:
                if option.label:
                  texts.append(option.label)

        elif isinstance(component, Button):
          if component.label:
            texts.append(component.label)

        elif isinstance(component, SelectMenu):
          for option in component.options:
            if option.label:
              texts.append(option.label)
    
    text = " ".join(texts)
    
    if len(text) > 0:
      if has_maximum:
        max_len = int(cmd_parts[1][1:])
        if max_len > 2000:
          max_len = 2000
        await message.channel.send(markov_function(text, max_len))
      else:
        await message.channel.send(markov_function(text))
    
    else:
      await message.channel.send("Error: No text was provided")
  
  elif has_maximum:
    #Input is in the command
    text = " ".join(cmd_parts[2:])
    max_len = int(cmd_parts[1][1:])
    if max_len > 2000:
      max_len = 2000
    await message.channel.send(markov_function(text, max_len))
  
  else:
    text = " ".join(cmd_parts[1:])
    await message.channel.send(markov_function(text))
