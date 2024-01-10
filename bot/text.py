import random

letters_lower = {
  "a": "aàáâäæãåā",
  "c": "cçćč",
  "e": "eèéêëēėę",
  "i": "iìįīíïî",
  "l": "lł",
  "n": "nńñ",
  "o": "oôöòóœøōõ",
  "s": "sśš",
  "u": "uûüùúū",
  "y": "yÿ",
  "z": "zžźż"
}
letters_upper = {
  k.upper(): v.upper() for k, v in letters_lower.items()
}
letters = {**letters_lower, **letters_upper}

corruption_list = [
  -2, -1, -1, -1, 0, 0, 0, 1, 1, 1, 2
]
corruption_min = 32 - min(corruption_list)
corruption_max = 126 - max(corruption_list)

def get_letter(c):
  if c in letters:
    return random.choice(letters[c])
  else:
    return c

def frenchify(s):
  r = list(s)
  r = [get_letter(c) for c in r]
  return "".join(r)

def corrupt_char(c):
  if corruption_min <= ord(c) <= corruption_max:
    offset = random.choice(corruption_list)
    return chr(ord(c) + offset)
  return c

def corrupt(text):
  return "".join(map(corrupt_char, text))

def escape(text):
  return text.replace("\\", "\\\\").replace("`", "\\`").replace("_", "\\_").replace("*", "\\*").replace("~", "\\~")
