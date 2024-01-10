import replit

last_uid, fib_count, next_fib = map(int, replit.db["fib"].split(","))
high_score = int(replit.db["fibhs"])

def nth_fib(n):
  a, b = 0, 1
  for i in range(n):
    a, b = b, a + b
  return a

def get_cur_fib():
  return nth_fib(fib_count - 1)

async def check(msg):
  if len(msg.content) == 0:
    return
  
  val = msg.content.lower().strip().split()[0]
  if all(c in "0123456789" for c in val):
    global last_uid
    global fib_count
    global next_fib
    global high_score
    
    if msg.author.id != last_uid and int(val) == next_fib:
      try:
        await msg.add_reaction("✅")
        last_uid = msg.author.id
        fib_count += 1
        if next_fib > high_score:
          high_score = next_fib
          replit.db["fibhs"] = str(high_score)
        next_fib = nth_fib(fib_count)
      except:
        print("User probably blocked the bot")
    else:
      if msg.author.id == last_uid:
        what_wrong = "You can't count two numbers in a row."
      else:
        what_wrong = "Wrong number."
      try:
        await msg.add_reaction("❌")
        await msg.reply(f"{msg.author.mention} RUINED IT AT **{get_cur_fib()}**!! Next Fibonacci number is **0**. **{what_wrong}**")
        last_uid = 0
        fib_count = 0
        next_fib = 0
      except:
        print("User probably blocked the bot")
    
    replit.db["fib"] = f"{last_uid},{fib_count},{next_fib}"
