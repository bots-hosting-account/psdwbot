element_list = []
element_lookup = []
element_symbols = []

with open("elements.txt", "r") as elements_file:
  for line in elements_file.read().split("\n"):
    vals = line.split()
    element_list.append(line)
    element_lookup.append(tuple(v.lower() for v in vals))
    element_symbols.append(vals[1].lower())


async def send_word_elements_message(cmd_parts, message, *, use_names):
  if len(cmd_parts) < 2:
    await message.channel.send(f"Usage: `+{cmd_parts[0]} words`")
    return
  
  results = []
  for word in cmd_parts[1:]:
    wel_result = word_elements(word, use_names)
    results.append(wel_result or "Word cannot be broken into elements")
  
  result = "\n".join(results)
  await message.channel.send(result)

def word_elements(w, use_names):
  w = "".join(c for c in w.lower() if ord(c) in range(97, 123))
  result = word_elements_util(w, [], "")
  
  if result == False:
    return None
  else:
    if use_names:
      result = (element_lookup[element_symbols.index(element)][2] for element in result)
    return " ".join(result).title()

def word_elements_util(w, got_list, got_str):
  if got_str == w:
    return got_list

  for symbol in element_symbols:
    try_str = got_str + symbol
    if len(try_str) <= len(w) and w[:len(try_str)] == try_str:
      result = word_elements_util(w, got_list + [symbol], try_str)
      if result != False:
        return result
  
  return False


async def send_get_element_message(cmd_parts, message):
  if len(cmd_parts) < 2:
    await message.reply(f"Usage: `+{cmd_parts[0]} datum`, where `datum` is the name, symbol, or atomic number of an element")
    return
  
  datum = cmd_parts[1]
  element = get_element(datum)
  await message.channel.send(element or "No such element")

def get_element(s):
  s = s.lower()
  for i, vals in enumerate(element_lookup):
    if s in vals:
      return element_list[i]
  
  return None
