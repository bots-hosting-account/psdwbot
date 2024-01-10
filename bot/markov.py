import random
from collections import defaultdict

def get_first_chars(words):
  return [word[0] for word in words]

def get_rules(words):
  rules = defaultdict(list)
  for word in words:
    for i, char in enumerate(word[:-1]):
      rules[char].append(word[i + 1])
    rules[word[-1]].append(None)
  
  return dict(rules)

def markov(words, possible_starts, max_len):
  rules = get_rules(words)
  cur_char = random.choice(possible_starts)
  result = cur_char
  
  while len(result) < max_len:
    cur_char = random.choice(rules[cur_char])
    if cur_char == None:
      break
    else:
      result += cur_char

  return result

def markov_sentence(text, max_len=200):
  words = text.lower().split()
  possible_starts = get_first_chars(words)
  return markov([text.lower()], possible_starts, max_len)

def markov_word(text, max_len=200):
  words = text.lower().split()
  possible_starts = get_first_chars(words)
  return markov(words, possible_starts, max_len)

def is_valid_max_markov(text):
  return (
    len(text) >= 2 and text[0] == "!"
    and all(c in "0123456789" for c in text[1:])
    and any(c in "123456789" for c in text[1:])
  )
