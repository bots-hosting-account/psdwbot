from discord import Embed
import csv

def make_word(word, english, hint, pos, ipa, etymology, notes):
  return {
    "word": word,
    "english": english,
    "hint": hint,
    "pos": ("ADJ" if pos == "ADV" else pos),
    "ipa": ipa,
    "etymology": etymology,
    "notes": notes
  }

def get_words(filename):
  words = []
  with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      words.append(make_word(*row))
  return words

def search(query, search_eoo=False):
  words = get_words("assets/eoo_words.csv")

  search_field = "word" if search_eoo else "english"
  dict_query = query.strip().lower()

  results = []
  seen = set()
  for word in words:
    if word[search_field].lower() == dict_query:
      seen_key = (word["word"], word["pos"])
      if seen_key not in seen:
        results.append(word)
        seen.add(seen_key)

  e = Embed(title=f'Search results for "{query}"', color=0x33aa33)

  if len(results) == 0:
    e.add_field(name="No results", value="No words matched your search query.", inline=False)
  else:
    for result in results:
      homonyms = [word for word in words if word["word"] == result["word"] and word["pos"] == result["pos"]]

      value = ""
      for i, word in enumerate(homonyms):
        if not search_eoo and word["english"].lower() == dict_query:
          bold = "**"
        else:
          bold = ""
        sp = "\n\u200b\t\u200b\t\u200b\t\u200b\t\u200b    "
        value += "\u200b\t" + str(i + 1) + ". " + bold + word["english"] + bold
        if len(word["hint"]) > 0:
          value += " (" + word["hint"] + ")"
        if len(word["etymology"]) > 0:
          value += sp + word["etymology"].replace("\n", sp)
        if len(word["notes"]) > 0:
          value += sp + word["notes"].replace("\n", sp)
        value += "\n"

      pos = word["pos"].lower()
      if pos == "adj":
        pos = "adj. or adv"
      name = word["word"] + " *" + pos + ".*"
      e.add_field(name=name, value=value[:-1], inline=False)

  return e
