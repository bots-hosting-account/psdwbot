import random
from collections import defaultdict
import urllib.request

from markov import is_valid_max

MOBY_DICK_URL = "https://gist.githubusercontent.com/ktnyt/734e32aab75a4f7df06538dac9f00a5a/raw/8da85d5acabc53fd66af17c252701b0ba395e6c1/moby.txt"

def get_rules(words):
  rules = defaultdict(list)
  
  for i, word in enumerate(words[:-1]):
    rules[word].append(words[i + 1])
  
  rules[words[-1]].append(None)

  return dict(rules)

def markov_with_words(words, max_len):
  rules = get_rules(words)
  cur_word = random.choice(words)
  result = cur_word
  
  while True:
    cur_word = random.choice(rules[cur_word])
    if cur_word is None:
      break
    else:
      old_result = result
      result += " " + cur_word
      if len(result) > max_len:
        result = old_result
        break

  return result

def generate_moby_dick(max_len=200):
  page = urllib.request.urlopen(MOBY_DICK_URL)
  charset = page.headers.get_content_charset()
  words = page.read().decode(charset).lower().split()
  return markov_with_words(words, max_len)

async def send_message(cmd_parts, message):
  has_maximum = len(cmd_parts) >= 2 and is_valid_max(cmd_parts[1])

  if has_maximum:
    maximum_length = min(int(cmd_parts[1]), 2000)
    await message.reply(generate_moby_dick(maximum_length))
  else:
    await message.reply(generate_moby_dick())
