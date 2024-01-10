from discord import Embed
import csv

def make_word(word, english, pos, ipa, etymology, notes):
  return {
    "word": word, "english": english, "pos": ("ADJ" if pos == "ADV" else pos),
    "ipa": ipa, "etymology": etymology, "notes": notes
  }

def get_words(filename):
  words = []
  with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      words.append(make_word(*row))
  return words

words = get_words("assets/eoo_words.csv")

def search(query, search_eoo=False):
  search_field = "word" if search_eoo else "english"
  
  dict_query = query.strip().lower()
  results = [word for word in words if word[search_field].lower() == dict_query]
  if search_eoo:
    results = results[:1]
  
  e = Embed(title=f'Search results for "{query}"', color=0x33aa33)
  
  if len(results) == 0:
    e.add_field(name="No results", value="No words matched your search query.", inline=False)
  else:
    for result in results:
      homonyms = [word for word in words if word["word"] == result["word"] and word["pos"] == result["pos"]]
      
      value = ""
      for i, word in enumerate(homonyms):
        bold = "**" if word["english"].lower() == dict_query else ""
        sp = "\n\u200b\t\u200b\t\u200b\t\u200b\t\u200b    "
        value += "\u200b\t" + str(i + 1) + ". " + bold + word["english"] + bold
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
