import random
from collections import defaultdict
import urllib.request

MOBY_DICK_URL = "https://gist.githubusercontent.com/ktnyt/734e32aab75a4f7df06538dac9f00a5a/raw/8da85d5acabc53fd66af17c252701b0ba395e6c1/moby.txt"

def get_rules(words, context):
  rules = defaultdict(list)
  
  for i in range(len(words) - context):
    rules[tuple(words[i : i + context])].append(words[i + context])
  
  rules[tuple(words[len(words) - context:])].append(None)
  
  return dict(rules)

def markov_with_words(words, max_len, context_length):
  rules = get_rules(words, context_length)
  context = random.choice(tuple(key for key in rules if None not in key))
  result = " ".join(context)
  
  while True:
    cur_word = random.choice(rules[context])
    if cur_word is None:
      break
    else:
      old_result = result
      result += " " + cur_word
      if len(result) <= max_len:
        context = (*context[1:], cur_word)
      else:
        result = old_result
        break
  
  return result

def generate_moby_dick(max_length, context_length):
  page = urllib.request.urlopen(MOBY_DICK_URL)
  charset = page.headers.get_content_charset()
  words = page.read().decode(charset).lower().split()
  return markov_with_words(words, max_length, context_length)

async def send_message(cmd_parts, message):
  has_maximum = len(cmd_parts) >= 2 and cmd_parts[1].isdigit() and int(cmd_parts[1]) > 0
  if has_maximum:
    maximum_length = min(int(cmd_parts[1]), 2000)
  else:
    maximum_length = 200
  
  has_context = len(cmd_parts) >= 3 and cmd_parts[2].isdigit() and int(cmd_parts[2]) > 0
  if has_context:
    context_length = min(int(cmd_parts[2]), 5)
  else:
    context_length = 1
  
  await message.reply(generate_moby_dick(maximum_length, context_length))
