import random 

def anagram(s):
  a = [c for c in s.lower() if c.isalnum() or c == " "]
  spaces = (i for i, c in enumerate(a) if c == " ")
  a = [c for c in a if c != " "]
  random.shuffle(a)
  for i in spaces:
    a.insert(i, " ")
  a = "".join(a).split()
  random.shuffle(a)
  a = " ".join(w[0].upper() + w[1:].lower() if len(w) > 0 else "" for w in a)
  return a

