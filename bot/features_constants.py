features_basic = """Basic commands:
  • `+hello` — Say hello to the bot
  • `+say` — Make the bot say something
  • `+whoami` — Print who you are
  • `+version` — Print the bot's current version
  • `+features`, `+fea`, `+f` — Print this list
  • `+help` — Get help, or get information about a command
  • `+d` — Delete a command after running it
Additionally, `+p` can be used to run a command without confusion (for example, if another bot has a command called `+say`, you can run `+p say` to only use PsdwBot).
"""
features_general = """General commands:
  • `+ad` — Print an ad for a random website
  • `+trivia` or `+t` — Trivia
  • `+anagram` or `+ana` — Anagrams
  • `+triviagram` or `+tg` — Anagrammed trivia
  • `+solve` or `+s` — A calculator
  • `+genimg` — Image generation
  • `+makeimg`, `+rect`, `+viewimg` — Image painting
  • `+brainfuck`, `+brainf`, `+bf` — Brainfuck interpreter
  • `+earthquakes` — List recent earthquakes
  • `+divisions` — List the provinces/states/etc. of a given country
  • `+minesweeper` — Play a game of Stupid Minesweeper
  • `+chess` — Get the current chess count
  • `+count` — Get the current Fibonacci number
  • `+primecount` or `+prime` — Get the current prime number
  • `+highscore` or `+hs` — Get the high score for prime counting
  • `+fibhs` — Get the high score for custom Fibonacci counting
  • `+cgol` — Play Conway's Game of Life
  • `+osm` — OpenStreetMap viewer
  • `+zoomin` — Zoom in, for `+osm`
  • `+zoomout` — Zoom out, for `+osm`
  • `+roman` — Convert to and from Roman numerals
  • `+xkcd` — Get a random xkcd comic
  • `+calvinandhobbes`, `+cah` — Get a random Calvin and Hobbes comic
  • `+outlink` — Get a random outlink from a Wikipedia article
  • `+unusual` — Get a random unusual Wikipedia article
  • `+element`, `+el` — Get information about an element"""
features_text = """Text mangling commands:
  • `+palindrome` — Palindromify text
  • `+posteoo` — Convert from postfix accents to proper accents
  • `+accent` — Randomly accent a string (none, high, low, falling)
  • `+accent` — Randomly accent a string (none, high, low, falling) with a higher chance of no accent
  • `+accentr` — Randomly accent a string (none, high, low, falling, rising)
  • `+accentr2` — Randomly accent a string (none, high, low, falling, rising) with a higher chance of no accent
  • `+corrupt` — Corrupt text
  • `+frenchify` or `+french` — Mækę tèxt Frénçh
  • `+corruptfrench` — Corrupt text, then mækę it Frénçh
  • `+corruptfrenchn` or `+cfn` — Repeatedly apply corruptfrench to text
  • `+ultrafrench` or `+uf` — Repeatedly corrupt text, then make it French
  • `+wordelements` or `+wel` — Break a word into elements"""
features_textgen = """Text generation commands:
  • `+sentence` — Generate a random sentence
  • `+paragraph` or `+para` — Generate a random paragraph
  • `+frenchparagraph` or `+frenchpara` — Generate a random paragraph, then mækę it Frénçh
  • `+corruptparagraph` or `+corruptpara` — Generate a random paragraph, then corrupt it
  • `+corruptfrenchparagraph` or `+corruptfrenchpara` — Generate a random paragraph, then corrupt it and mækę it Frénçh
  • `+cfnparagraph` or `+cfnpara` — Generate a random paragraph, then repeatedly apply corruptfrench to it
  • `+ultrafrenchpara` or `+ufpara` — Generate a random paragraph, repeatedly corrupt it, then mækę it Frénçh
  • `+markov`, `+m` — Generate a random sentence based on a given sentence, using Markov chains
  • `+markovword`, `+markovwords`, `+mw` — Generate a random word based on a given list of words, using Markov chains
  • `+mobydick`, `+moby`, `+md` — Generate random text using *Moby-Dick* and Markov chains
  • `+markovadj`, `+madj`, `+ma` — Generate a random "adjective" using Markov chains
  • `+markovnoun`, `+mnoun`, `+mn` — Generate a random "noun" using Markov chains
  • `+markovverb`, `+mverb`, `+mv` — Generate a random "verb" using Markov chains"""
features_chans = """Channel-related commands:
  • `+chan` — Say something to another channel (use the name of a channel in the current server)
  • `+savechan` or `+vc` — Save the current channel as a supplied name (should only be one word long)
  • `+getchan` or `+gc` — Get the name and server name of a channel saved by `+savechan` (`+getchan saved-name`)
  • `+saychan` or `+yc` — Say something to another channel (use a name saved by `+savechan` - `+saychan saved-name content`)
  • `+saychanc` or `+ycc` — Same as `+saychan`, except the message is surrounded by a code block (\`\`\` \`\`\`) before being sent
The `+savechan` and `+saychan` commands can be used for cross-server messaging."""
features_currency = """Currency-related commands:
  • `+beg` — Beg for money
  • `+search` — Search for money
  • `+hunt` — Hunt
  • `+fish` — Fish
  • `+dig` — Dig
  • `+rob` or `+steal` — Rob a user
  • `+balance` or `+bal` — View your balance
  • `+networth` or `+net` — View your net worth
  • `+gamble` — Gamble some of your money for a chance to double it—or lose it all
  • `+inventory` or `+inv` — View your inventory
  • `+item` or `+view` — View a specific item
  • `+shop` or `+store` — View the shop
  • `+items` or `+allitems` — See a list of all items
  • `+buy` — Buy an item
  • `+sell` — Sell an item
  • `+use` — Use an item
  • `+jobs` — View a list of available jobs
  • `+apply` — Apply for a job
  • `+work` — Work at a job
  • `+resign` or `+quit` — Resign from a job
  • `+leaderboard` or `+rich` — See the leaderboard for this server
  • `+leaderboard g` or `+rich g` — See the global leaderboard
  • `+netleaderboard` or `+netrich` — See the net worth leaderboard for this server
  • `+netleaderboard g` or `+netrich g` — See the global net worth leaderboard
  • `+event` — View the current event
"""

feature_texts = {
  "cmds_basic": features_basic,
  "cmds_general": features_general,
  "cmds_text": features_text,
  "cmds_textgen": features_textgen,
  "cmds_chans": features_chans,
  "cmds_currency": features_currency
}

plushelp_msg = "\nFor more information about a specific command, use `+help command_name` (where `command_name` is the name of the command)."

help_text = """PsdwBot - A general-purpose bot made by psdw
Type `+features` for a list of commands.
For information about a specific command, try `+help command`."""
