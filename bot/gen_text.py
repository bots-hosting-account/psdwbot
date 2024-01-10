import random

def is_vowel(c):
  return c.lower() in "aeiou"

def conjugate_3s(verb):
  return verb + ("es" if verb[-1] in "szh" else "s")

with open("assets/words/nouns.txt") as nouns_file:
  nouns = nouns_file.read().split("\n")
with open("assets/words/verbs.txt") as verbs_file:
  verbs = verbs_file.read().split("\n")
with open("assets/words/adjs.txt") as adjs_file:
  adjs = adjs_file.read().split("\n")

determiners = ("a", "the")

def get_noun():
  determiner = random.choice(determiners)
  noun = random.choice(nouns)
  if random.randint(0, 1) == 0:
    adj = random.choice(adjs)
    if determiner == "a" and is_vowel(adj[0]):
      determiner = "an"
    determiner += " " + adj
  elif determiner == "a" and is_vowel(noun[0]):
    determiner = "an"
  return determiner + " " + noun

def get_verb():
  return conjugate_3s(random.choice(verbs))

def get_adj():
  return random.choice(adjs)

def get_sentence(end=".", capitalise_first_word=True):
  sentence = get_noun()
  if capitalise_first_word:
    sentence = sentence.title()
  sentence += " " + get_verb() + " " + get_noun() + end
  return sentence

def get_sentence_multiple():
  n_comma_sentences = random.randint(0, 2)
  p = get_sentence(", " if n_comma_sentences > 0 else " ")
  for _ in range(n_comma_sentences):
    p += get_sentence(", ", capitalise_first_word=False)
  p += "and " + get_sentence(capitalise_first_word=False)
  return p

def get_paragraph():
  num_sentences = random.randint(5, 8)
  res = ""
  for i in range(num_sentences):
    if random.randint(0, 2) > 0:
      res += get_sentence(". ")
    else:
      res += get_sentence_multiple() + " "
  return res[:-1]

def palindromify(s):
  return s + s[:-1][::-1]
