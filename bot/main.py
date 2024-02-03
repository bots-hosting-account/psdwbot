print("Starting...")
import discord
from discord.ext import commands
from discord_ui import UI

import os
import sys, random
import bfi as brainf
import roman

from solve import solve_equation
from anagram import anagram
from osm import send_tile_img, zoomin, zoomout
from web_random import get_random_wikipedia_outlink, get_random_unusual_article
from gen_text import get_sentence, get_paragraph, palindromify
from text import frenchify, corrupt, escape
from xkcd import (
  has_xkcd_hyphen, xkcd_hyphenate,
  get_random_xkcd, get_random_calvin_hobbes, get_random_dilbert
)
from eoo import from_post, rand_accent_str, rand_accent_str_r
from features_constants import help_text
from features_help import bot_help
print("Importing divisions...")
import divisions
print("Importing...")
import markov
import markov_wrapper
import markov_moby_dick
import currencygame as cg
import currencygame.work as cgwork
import features
import elements
import stupid_minesweeper
import cgol
import trivia
import channels
import eoo_words
import dad_humour
import earthquakes

import images

from counting_chess import CountingChess
from counting_fibonacci import CountingFibonacci
from counting_custom_fibonacci import CountingCustomFibonacci
from counting_prime import CountingPrime


intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(" ", intents=intents)
ui = UI(client)


async def eval_cmd(message):
  #Remove plus sign and leading whitespace
  command_and_arguments = message.content[1:].lstrip()
  
  cmd_parts = command_and_arguments.split()
  plus_d = False
  while cmd_parts[0] in ("p, d"):
    if cmd_parts[0] == "d":
      plus_d = True
    cmd_parts.pop(0)
  
  cmd = cmd_parts[0].lower()
  
  if cmd == "hello":
    await message.channel.send(f"Hello to you too, {message.author.name}!")
  
  elif cmd == "help":
    if len(cmd_parts) > 1:
      await message.channel.send(embed=bot_help(cmd_parts[1]))
    else:
      await message.channel.send(help_text)
  
  elif cmd == "say":
    msg = " ".join(cmd_parts[1:])
    bad = len(msg) == 0 or "<@&" in msg or "@everyone" in msg or "@here" in msg
    if bad:
      msg = "No."
    await message.channel.send(msg)
  
  elif cmd in ("version", "ver"):
    await message.channel.send(f"PsdwBot\nUsing Python version {sys.version}\nThis is the second occurrence of PsdwBot.")
  
  elif cmd == "ad":
    a = ("https://discord.com", "https://oracle.com", "https://xkcd.com", "https://python.org", "https://www.wikidata.org", "https://ramiro.org", "https://pypi.org/")
    await message.channel.send(random.choice(a))
  
  elif cmd == "whoami":
    whoareyou = message.author.nick or message.author.name.split("#")[0]
    await message.channel.send(whoareyou)
  
  elif cmd in ("features", "fea", "f"):
    await features.run(message, client)
  
  elif cmd in ("palindrome", "palindromify", "pal"):
    if len(cmd_parts) > 1:
      await message.channel.send(palindromify(" ".join(cmd_parts[1:])))
    else:
      await message.channel.send(palindromify("a man a plan a c"))
  
  elif cmd in ("frenchify", "french"):
    if len(cmd_parts) > 1:
      string = " ".join(cmd_parts[1:])
    else:
      string = "Francais"
    await message.channel.send(frenchify(string))
  
  elif cmd == "corrupt":
    if len(cmd_parts) > 1:
      string = " ".join(cmd_parts[1:])
    else:
      string = "The quick brown fox jumps over the lazy dog."
    await message.channel.send(escape(corrupt(string)))
  
  elif cmd in ("corruptfrench", "cf"):
    if len(cmd_parts) > 1:
      string = " ".join(cmd_parts[1:])
    else:
      string = "The quick brown fox jumps over the lazy dog."
    string = escape(frenchify(corrupt(string)))
    await message.channel.send(string)
  
  elif cmd in ("corruptfrenchn", "cfn"):
    string = None
    if len(cmd_parts) < 2:
      await message.channel.send("Usage: `+corruptfrenchn n text...`")
    elif any(c not in "0123456789" for c in cmd_parts[1]):
      await message.channel.send("n must be a nonnegative integer")
    elif len(cmd_parts) > 2:
      string = " ".join(cmd_parts[2:])
    else:
      string = "The quick brown fox jumps over the lazy dog."
    if string != None:
      n = int(cmd_parts[1])
      for i in range(n):
        string = frenchify(corrupt(string))
      await message.channel.send(escape(string))
  
  elif cmd in ("ultrafrench", "uf"):
    string = None
    if len(cmd_parts) < 2:
      await message.channel.send("Usage: `+ultrafrench n text...`")
    elif any(c not in "0123456789" for c in cmd_parts[1]):
      await message.channel.send("n must be a nonnegative integer")
    elif len(cmd_parts) > 2:
      string = " ".join(cmd_parts[2:])
    else:
      string = "The quick brown fox jumps over the lazy dog."
    if string != None:
      n = int(cmd_parts[1])
      for i in range(n):
        string = corrupt(string)
      await message.channel.send(escape(frenchify(string)))
  
  elif cmd in ("savechan", "vc"):
    await channels.save_channel_to_db(cmd_parts, message)
  
  elif cmd in ("getchan", "gc"):
    await channels.send_get_channel_message(cmd_parts, message)
  
  elif cmd in ("saychan", "saychanc", "yc", "ycc"):
    format_as_code = cmd in ("saychanc", "ycc")
    await channels.send_message_in_saved_channel(cmd_parts, message, format_as_code)
  
  elif cmd == "chan":
    await channels.send_message_in_channel(cmd_parts, message, client)
  
  elif cmd in ("brainfuck", "brainf", "bf"):
    co_in = "".join(cmd_parts[1:]).split("!", 1)
    code = co_in[0]
    stdin = co_in[1] if len(co_in) > 1 else ""
    output = brainf.interpret(code, input_data=stdin, buffer_output=True) or "(empty)"
    await message.channel.send(output)
  
  elif cmd in ("divisions", "divs", "div", "states", "admindivs", "provinces", "regions"):
    await divisions.send_message(cmd_parts, message)
  
  elif cmd in ("addrole", "removerole"):
    if len(cmd_parts) <= 2:
      await message.reply(f"Usage: `+{cmd} member_id role_name` or `+{cmd} member_id role_id`")
    else:
      member_id = cmd_parts[1]
      if not member_id.isdigit():
        member_id = member_id[2:-1] #<@member_id>
      if not member_id.isdigit():
        await message.reply(f"Usage: `+{cmd} member_id role_name` or `+{cmd} member_id role_id`")
      else:
        member = message.guild.get_member(int(member_id))
        if not member:
          await message.reply(f"Error: No member in the server has the ID `{member_id}`")
        else:
          if not message.author.guild_permissions.manage_roles:
            await message.reply("You do not have permissions")
          else:
            role_name = " ".join(cmd_parts[2:])
            role = discord.utils.get(message.guild.roles, name=role_name)
            error_msg = f"The role `{role_name}` does not exist"
            if not role:
              role_id = cmd_parts[2]
              if not role_id.isdigit():
                role_id = role_id[3:-1] #<@&role_id>
              if not role_id.isdigit():
                await message.reply(error_msg)
              else:
                role_id = int(role_id)
                role = discord.utils.get(message.guild.roles, id=role_id)
            if not role:
              await message.reply(error_msg)
            else:
              if cmd == "addrole":
                await member.add_roles(role)
              else:
                await member.remove_roles(role)
              if not plus_d:
                await message.reply("Done")
  
  elif cmd in ("earthquakes", "earthquake", "eq"):
    await earthquakes.send_message(cmd_parts, message)
  
  elif cmd == "genimg":
    await images.generate_image(cmd_parts, message)
  
  elif cmd == "makeimg":
    await images.make_image(cmd_parts, message)
  
  elif cmd == "viewimg":
    await images.view_image(cmd_parts, message)
  
  elif cmd == "rect":
    await images.draw_rect(cmd_parts, message)
  
  elif cmd == "dad":
    await dad_humour.send_message(cmd_parts, message)
  
  elif cmd in ("element", "el"):
    await elements.send_get_element_message(cmd_parts, message)
  
  elif cmd in ("wordelements", "wel"):
    await elements.send_word_elements_message(cmd_parts, message, use_names=False)
  
  elif cmd in ("wordelementsnames", "welnames", "weln"):
    await elements.send_word_elements_message(cmd_parts, message, use_names=True)
  
  elif cmd in ("solve", "s", "calculate", "calc"):
    try:
      result = solve_equation("".join(cmd_parts[1:]))
      if result == None:
        result = "Error: Invalid equation"
      await message.channel.send(str(result))
    except OverflowError:
      await message.channel.send("Error: Result is too large")
  
  elif cmd in ("anagram", "ana"):
    s = " ".join(cmd_parts[1:]) if len(cmd_parts) > 1 else "The quick brown fox jumped over the lazy dog"
    await message.channel.send(anagram(s))
  
  elif cmd in ("trivia", "triv", "t", "triviagram", "tg"):
    is_triviagram = "g" in cmd
    await trivia.run(message, client, is_triviagram)
  
  elif cmd == "osm":
    valid = len(cmd_parts[1:]) == 3
    if valid:
      try:
        zoom = int(cmd_parts[1])
        lat = float(cmd_parts[2])
        long = float(cmd_parts[3])
      except:
        valid = False
    
    if valid:
      await send_tile_img(lat, long, zoom, message.channel)
    else:
      await message.channel.send("Usage: `+osm zoom lat long`")
  
  elif cmd == "zoomin":
    await zoomin(message)
  
  elif cmd == "zoomout":
    await zoomout(message)
  
  elif cmd == "unusual":
    article = get_random_unusual_article()
    await message.channel.send(article)
  
  elif cmd == "outlink":
    if len(cmd_parts) > 1:
      article = get_random_wikipedia_outlink("_".join(cmd_parts[1:]))
      await message.channel.send(article)
    else:
      await message.channel.send("Usage: `+outlink pagename`")
  
  elif cmd == "sentence":
    n = 1
    if len(cmd_parts) > 1 and cmd_parts[1].isdigit():
      n = max(1, int(cmd_parts[1]))
    await message.channel.send(" ".join(get_sentence() for _ in range(n)))
  
  elif cmd in ("para", "paragraph", "frenchpara", "frenchparagraph", "corruptpara", "corruptparagraph", "corruptfrenchpara", "corruptfrenchparagraph"):
    if cmd in ("frenchpara", "frenchparagraph"):
      paraf = lambda: frenchify(get_paragraph())
    
    elif cmd in ("corruptpara", "corruptparagraph"):
      paraf = lambda: corrupt(get_paragraph())
    
    elif cmd in ("corruptfrenchpara", "corruptfrenchparagraph"):
      paraf = lambda: frenchify(corrupt(get_paragraph()))
    
    else:
      paraf = get_paragraph
    
    n = 1
    if len(cmd_parts) > 1 and cmd_parts[1].isdigit():
      n = max(1, int(cmd_parts[1]))
    for _ in range(n):
      await message.channel.send(paraf())
  
  elif cmd in ("cfnparagraph", "cfnpara", "ultrafrenchpara", "ufpara"):
    if len(cmd_parts) < 2:
      await message.channel.send(f"Usage: `+{cmd} n`")
    elif any(c not in "0123456789" for c in cmd_parts[1]):
      await message.channel.send("n must be a nonnegative integer")
    else:
      string = get_paragraph()
      n = int(cmd_parts[1])
      if "cfn" in cmd:
        for i in range(n):
          string = frenchify(corrupt(string))
        await message.channel.send(escape(string))
      else:
        for i in range(n):
          string = corrupt(string)
        await message.channel.send(escape(frenchify(string)))

  elif cmd in ("markov", "m", "markovword", "markovwords", "mw"):
    use_words = "w" in cmd
    await markov_wrapper.send_message(cmd_parts, message, use_words)
  
  elif cmd in ("moby", "mobydick", "md"):
    await markov_moby_dick.send_message(cmd_parts, message)
  
  elif cmd in ("markovadjective", "madj", "ma"):
    with open("assets/words/adjs.txt") as adjs_file:
      await message.channel.send(markov.word(adjs_file.read()))
  
  elif cmd in ("markovnoun", "mnoun", "mn"):
    with open("assets/words/nouns.txt") as nouns_file:
      await message.channel.send(markov.word(nouns_file.read()))
  
  elif cmd in ("markovverb", "mverb", "mv"):
    with open("assets/words/verbs.txt") as verbs_file:
      await message.channel.send(markov.word(verbs_file.read()))
  
  elif cmd == "ssm":
    await message.channel.send(" ".join(mm.name for mm in message.channel.guild.members))
  
  elif cmd == "roman":
    if len(cmd_parts) > 1:
      s = cmd_parts[1]
      if s.isdigit():
        try:
          await message.reply(roman.toRoman(int(s)))
        except roman.OutOfRangeError:
          await message.reply(f"Error: integer must be between 0 and 4999 inclusive, {s} was given")
      else:
        try:
          await message.reply(roman.fromRoman(s.upper()))
        except roman.InvalidRomanNumeralError:
          await message.reply("Please provide a valid integer or Roman numeral.")
    else:
      await message.reply("Usage: `+roman [Roman numeral]` or `+roman [integer]`")
  
  elif cmd == "minesweeper":
    await stupid_minesweeper.run(message, client)
  
  elif cmd == "posteoo":
    if len(cmd_parts) > 1:
      await message.reply(from_post(" ".join(cmd_parts[1:])))
    else:
      await message.reply("Usage: `+posteoo [text]`")

  elif cmd in ("accent", "accent2", "accentr", "accentr2"):
    accent_fn = rand_accent_str_r if "r" in cmd else rand_accent_str
    is_two = cmd[-1] == "2"
    if len(cmd_parts) > 1:
      await message.reply(accent_fn(" ".join(cmd_parts[1:]), is_two))
    else:
      await message.reply(f"Usage: `+{cmd} [text]`")
  
  elif cmd == "beg":
    await cg.beg(message)
  
  elif cmd in ("balance", "bal"):
    await cg.balance(message, cmd_parts, client)
  
  elif cmd in ("net", "networth"):
    await cg.balance(message, cmd_parts, client, net_worth=True)
  
  elif cmd in ("gamble", "bet", "wager"):
    await cg.gamble(cmd_parts, message)
  
  elif cmd in ("inventory", "inv"):
    await cg.inventory(cmd_parts, message, client)
  
  elif cmd == "buy":
    await cg.buy(cmd_parts, message)
  
  elif cmd == "sell":
    await cg.sell(cmd_parts, message)
  
  elif cmd == "search":
    await cg.search(message, client)

  elif cmd == "dig":
    await cg.dig(message)

  elif cmd == "fish":
    await cg.fish(message)

  elif cmd == "hunt":
    await cg.hunt(message)

  elif cmd == "use":
    await cg.use_item(cmd_parts, message)
  
  elif cmd in ("item", "view"):
    await cg.view_item(cmd_parts, message)
  
  elif cmd in ("leaderboard", "lb", "rich"):
    if len(cmd_parts) > 1 and cmd_parts[1][0] in "Gg":
      rich_users = client.users
    else:
      rich_users = message.guild.members
    await cg.leaderboard(client, message.channel, rich_users)
  
  elif cmd in ("netleaderboard", "netlb", "netrich"):
    if len(cmd_parts) > 1 and cmd_parts[1][0] in "Gg":
      rich_users = client.users
    else:
      rich_users = message.guild.members
    await cg.net_worth_leaderboard(client, message.channel, rich_users)

  elif cmd in ("shop", "store", "market"):
    await cg.shop(message, client)
  
  elif cmd == "event":
    await cg.event_message(message)
  
  elif cmd in ("items", "allitems"):
    await cg.view_items(message, client)
  
  elif cmd in ("rob", "steal"):
    await cg.rob(cmd_parts, message)

  elif cmd == "work":
    await cgwork.work(cmd_parts, message, client)
  
  elif cmd == "jobs":
    await cgwork.list_jobs(message)
  
  elif cmd == "apply":
    await cgwork.apply(cmd_parts, message)
  
  elif cmd in ("resign", "quit"):
    await cgwork.resign(message)
  
  elif cmd in ("addbal", "setbal"):
    if len(cmd_parts) > 2 and str(message.author.id).startswith("84607"):
      #Admin only
      uid = cmd_parts[1]
      amt = cmd_parts[2]
      if uid.isdigit() and (amt.isdigit() or (amt[0] == "-" and amt[1:].isdigit())):
        if cmd == "addbal":
          cg.add_money(uid, int(amt))
          await message.channel.send(f"Addbal done, {uid} now has {cg.format(cg.get_money(uid))}")
        elif amt[0] != "-":
          cg.set_money(uid, int(amt))
          await message.channel.send(f"Setbal done, {uid} now has {cg.format(int(amt))}")
        else:
          await message.channel.send("Cannot set balance to a negative amount")
      else:
        await message.channel.send(f"Incorrect syntax (+{cmd} uid amt)")
  
  elif cmd == "sort":
    if len(cmd_parts) < 2:
      if message.reference is not None and message.reference.resolved:
        #Replying to a message
        mrmid = message.reference.message_id
        old_message = await message.channel.fetch_message(mrmid)
        words = old_message.content.split()
        if len(words) == 0:
          await message.channel.send("No.")
        else:
          await message.channel.send(" ".join("".join(sorted(w, key=str.lower)) for w in words))
    
    else:
      if len(cmd_parts) == 1:
        await message.channel.send("No.")
      else:
        await message.channel.send(" ".join("".join(sorted(w, key=str.lower)) for w in cmd_parts[1:]))
  
  elif cmd == "cgol":
    if len(cmd_parts) > 1 and cmd_parts[1].isdigit():
      pos = int(cmd_parts[1])
      await cgol.run(message, client, pos)
    else:
      await message.reply("Usage: `+cgol pos`\nType `+cgol 129298419` for an example.")
  
  elif cmd == "xkcd":
    await message.reply(get_random_xkcd())

  elif cmd in ("calvinandhobbes", "cah"):
    await get_random_calvin_hobbes(message, client, message.author)

  elif cmd == "dilbert":
    await get_random_dilbert(message, client, message.author)
  
  elif cmd == "chess":
    await message.reply(f"The current chess count is **{CountingChess.get_current_number()}**.")
  
  elif cmd == "chesshs":
    await message.reply(f"The highest-reached chess count is **{CountingChess.get_high_score()}**.")

  elif cmd in ("count", "fibcount"):
    await message.reply(f"The current Fibonacci number is **{CountingFibonacci.get_current_number()}**.")
  
  elif cmd in ("counths", "fibcounths", "fibhs"):
    await message.reply(f"The highest-reached Fibonacci number is **{CountingFibonacci.get_high_score()}**.")
  
  elif cmd in ("customcount", "custcount", "customfibcount", "custfibcount", "customfib", "custfib"):
    await message.reply(f"The current custom Fibonacci number is **{CountingCustomFibonacci.get_current_number()}**.")
  
  elif cmd in ("customhs", "cusths", "customfibhs", "custfibhs"):
    await message.reply(f"The highest-reached custom Fibonacci number is **{CountingCustomFibonacci.get_high_score()}**.")

  elif cmd in ("primecount", "prime"):
    await message.reply(f"The current prime number is **{CountingPrime.get_current_number()}**.")

  elif cmd == "primehs":
    await message.reply(f"The highest-reached prime number is **{CountingPrime.get_high_score()}**.")
  
  elif cmd in ("dictionary", "dict"):
    if len(cmd_parts) < 2:
      help_embed = discord.Embed(title="Invalid Usage", description="Usage: `+dictionary query`\nSearch for an entry in [Eo'iona's dictionary](https://conworkshop.com/dictionary.php?L=EOO) (updated as of 2024/01/01).\n`query` must be an English word/phrase.")
      await message.reply(embed=help_embed)
    else:
      query = " ".join(cmd_parts[1:])
      await message.reply(embed=eoo_words.search(query))
  
  elif cmd in ("revdictionary", "reversedictionary", "revdict"):
    if len(cmd_parts) < 2:
      help_embed = discord.Embed(title="Invalid Usage", description="Usage: `+reversedictionary query`\nSearch for an entry in [Eo'iona's dictionary](https://conworkshop.com/dictionary.php?L=EOO) (updated as of 2024/01/01).\n`query` must be an Eo'iona word/phrase.")
      await message.reply(embed=help_embed)
    else:
      query = " ".join(cmd_parts[1:])
      e_embed = eoo_words.search(query, search_eoo=True)
      await message.reply(embed=e_embed)

  elif cmd == "react":
    if len(cmd_parts) < 3 or len(cmd_parts) == 4:
      await message.reply("Usage: `+react message_id emoji_name` (for a message in the same channel) or `+react server_id channel_id message_id emoji_name`")
    elif len(cmd_parts) == 3:
      channel = message.channel
      search_messages = await channel.history(limit=100).flatten()
      emsg = discord.utils.get(search_messages, id=int(cmd_parts[1]))
      try:
        emoji = discord.utils.get(client.emojis, name=cmd_parts[2])
        await emsg.add_reaction(emoji)
      except:
        await emsg.add_reaction(cmd_parts[4])
    else:
      server = discord.utils.get(client.guilds, id=int(cmd_parts[1]))
      channel = discord.utils.get(server.channels, id=int(cmd_parts[2]))
      search_messages = await channel.history(limit=100).flatten()
      emsg = discord.utils.get(search_messages, id=int(cmd_parts[3]))
      try:
        emoji = discord.utils.get(client.emojis, name=cmd_parts[4])
        await emsg.add_reaction(emoji)
      except:
        await emsg.add_reaction(cmd_parts[4])

  elif cmd == "namedisc":
    member = discord.utils.get(client.users, id=int(cmd_parts[1]))
    await message.channel.send(f"Name: {member.name}\nDiscriminator: {member.discriminator}\nId: {member.id}")
  
  elif cmd == "listservers":
    for guild in client.guilds:
      print(f"In guild {guild.name}")
  
  elif cmd == "tmp":
    svr = client.guilds[8]
    svrnfo = f"""Server {svr.name}
Owner: {svr.owner}
Member count: {svr.member_count}
Channels:\n"""
    for c in svr.channels:
      svrnfo += str(type(c))[8:-2] + " " + c.name + "\n"
    await message.reply(svrnfo)
  
  elif cmd == "update":
    if str(message.author.id)[:10] == "8460701070":
      await message.channel.send("Updating...")
      await client.logout()
      exit()
    else:
      await message.channel.send("Not you!")
  
  
  #If +d was used, delete the message
  if plus_d:
    await message.delete()


@client.event
async def on_reaction_remove(reaction, _user):
  brentoa = discord.utils.get(client.emojis, name="Brentoa")
  if reaction.emoji == brentoa:
    await reaction.message.add_reaction(brentoa)


@client.event
async def on_reaction_add(reaction, user):
  if user != client.user:
    col = discord.utils.get(client.emojis, name="col")
    endcol = discord.utils.get(client.emojis, name="endcol")
    if reaction.emoji == col:
      await reaction.message.add_reaction(col)
      await reaction.message.add_reaction(endcol)
    elif reaction.emoji == endcol:
      await reaction.message.add_reaction(endcol)


@client.event
async def on_ready():
  print("Logged in as", client.user)
  await client.change_presence(activity=discord.Game(name="+help / +p help"))
  
  channels.initialise(client)


@client.listen("on_message")
async def on_message(message: discord.Message):
  if message.channel.id in (
    987822002146516998, 987822035239591946,
    987822052436230214, 988236648863113266,
    988493298400395294
  ) or "brentoa" in message.content.lower():
    try:
      emoji = discord.utils.get(client.emojis, name="Brentoa")
      await message.add_reaction(emoji)
    except:
      print("No Brentoa emoji found")
  
  if message.author == client.user:
    return
  
  if message.content.startswith("+"):
    if len(message.content) > 1:
      await eval_cmd(message)
  else:
    if has_xkcd_hyphen(message.content):
      await message.reply(xkcd_hyphenate(message.content))
    else:
      mcl = message.content.lower()
      if ("thanks" in mcl or "thank you" in mcl) and not ("no" in mcl):
        await message.channel.send("you're welcome")
    
    if message.channel.name == "prime-chess":
      await CountingPrime.check(message)
      await CountingChess.check(message)
    elif message.channel.name == "fibonacci":
      await CountingFibonacci.check(message)
    elif message.channel.name == "custom-fibonacci":
      await CountingCustomFibonacci.check(message)


if __name__ == "__main__":
  client.run(open("../token.txt").read())
