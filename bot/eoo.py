import random

post_letter_map = {
  "A": "A", "a": "a",
  "A/": "Á", "a/": "á",
  "A\\": "À", "a\\": "à",
  "A^": "Â", "a^": "â",
  "A*": "Ǎ", "a*": "ǎ",
  "E": "E", "e": "e",
  "E/": "É", "e/": "é",
  "E\\": "È", "e\\": "è",
  "E^": "Ê", "e^": "ê",
  "E*": "Ě", "e*": "ě",
  "I": "I", "i": "i",
  "I/": "Í", "i/": "í",
  "I\\": "Ì", "i\\": "ì",
  "I^": "Î", "i^": "î",
  "I*": "Ǐ", "i*": "ǐ",
  "O": "O", "o": "o",
  "O/": "Ó", "o/": "ó",
  "O\\": "Ò", "o\\": "ò",
  "O^": "Ô", "o^": "ô",
  "O*": "Ǒ", "o*": "ǒ"
}

accent_dict = {
  "A": "AÁÀÂ",
  "E": "EÉÈÊ",
  "I": "IÍÌÎ",
  "O": "OÓÒÔ",
  "a": "aáàâ",
  "e": "eéèê",
  "i": "iíìî",
  "o": "oóòô"
}
accent_dict_2 = {k: k + v for k, v in accent_dict.items()}

accent_dict_r = {
  "A": "AÁÀÂǍ",
  "E": "EÉÈÊĚ",
  "I": "IÍÌÎǏ",
  "O": "OÓÒÔǑ",
  "a": "aáàâǎ",
  "e": "eéèêě",
  "i": "iíìîǐ",
  "o": "oóòôǒ"
}
accent_dict_r_2 = {k: k + v for k, v in accent_dict_r.items()}

def from_post(s):
  for k, v in post_letter_map.items():
    s = s.replace(k, v)
  return s

def rand_accent_char(d):
  return lambda c: random.choice(d.get(c, c))

def rand_accent_str(s, two):
  d = accent_dict_2 if two else accent_dict
  return "".join(map(rand_accent_char(d), s))

def rand_accent_str_r(s, two):
  d = accent_dict_r_2 if two else accent_dict_r
  return "".join(map(rand_accent_char(d), s))
