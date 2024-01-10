import discord

features_help_dict = {
  "p": (
    ["command..."],
    "If another bot has a command with the same name as one of PsdwBot's commands, this command can be used to specify that you want PsdwBot. Can be used with `+d`.",
    ["say Hello", "d say This is text", "d p d p d d p d p hello"]
  ),
  "d": (
    ["command..."],
    "Delete a command after running it. Can be used with `+p`.",
    ["hello", "say This is text", "p hello"]
  ),
  "hello": (
    [""],
    "Say hello to the bot.",
    [""]
  ),
  "help": (
    ["", "command"],
    "Get help, or get information about a specific command.",
    ["", "say"]
  ),
  "say": (
    ["text..."],
    "Make the bot say something.",
    ["Hello", "This has multiple words"]
  ),
  "version": (
    [""],
    "Get the bot's current version",
    [""],
    ["ver"]
  ),
  "ad": (
    [""],
    "Get an ad for a website.",
    [""]
  ),
  "whoami": (
    [""],
    "Be told who you are (your nickname or username).",
    [""]
  ),
  "features": (
    [""],
    "List the bot's features.",
    [""],
    ["fea", "f"]
  ),
  "palindrome": (
    ["", "text..."],
    "Palindromify text.",
    ["", "red rum sir"],
    ["palindromify", "pal"]
  ),
  "frenchify": (
    ["", "text..."],
    "Mâké tėxt Frėńçh.",
    ["", "This is some text."],
    ["french"]
  ),
  "corrupt": (
    ["", "text..."],
    "Corrupt text.",
    ["", "This is some text."]
  ),
  "corruptfrench": (
    ["", "text..."],
    "Corrupt text, then mâké it Frėńçh. See also `+corrupt` and `+french`.",
    ["", "This is some text."],
    ["cf"]
  ),
  "corruptfrenchn": (
    ["number text..."],
    "Corrupt text, then mâké it Frėńçh, `number` times. See also `+corruptfrench` and `+ultrafrench`.",
    ["5 This is some text."],
    ["cfn"]
  ),
  "ultrafrench": (
    ["number text..."],
    "Corrupt text `number` times, then mâké it Frėńçh. See also `+corruptfrench` and `+corruptfrenchn`.",
    ["5 This is some text."],
    ["uf"]
  ),
  "savechan": (
    ["savename"], #, "savename s"
    "Save the current text channel as `savename` for future use by `+getchan`, `+saychan`, or `+saychanc`. `savename` must not be empty.",
    ["TheBestChannel"],
    ["vc"]
  ),
  "getchan": (
    ["savename"], #, "savename s"
    "Get the name and server of the text channel which has been saved as `savename` by `+savechan`.",
    ["TheBestChannel"],
    ["gc"]
  ),
  "saychan": (
    ["savename text..."], #, "savename s"
    "Say `text` in the text channel which has been saved as `savename` by `+savechan`. Unlike `+say`, this command preserves whitespace.",
    ["TheBestChannel Hello world"],
    ["yc"]
  ),
  "saychanc": (
    ["savename text..."], #, "savename s"
    "Put `text` into a code block and say it in the text channel which has been saved as `savename` by `+savechan`. This command is equivalent to `+saychan`, other than the usage of a code block. Unlike `+say`, this command preserves all whitespace.",
    ["TheBestChannel Hello world"],
    ["ycc"]
  ),
  "chan": (
    ["channel text..."],
    "Get a channel by its name or ID and send `text` to it. `channel` can be the name of a channel in the current server, or the ID of any channel accessible to the bot. Unlike `+say`, this command preserves all whitespace.",
    ["general Hello channel"]
  ),
  "brainfuck": (
    ["brainfuck program...", "brainfuck program...!input..."],
    "Run a program written in brainfuck, an esoteric programming language. If `program` contains an exclamation mark, then everything to the left of the mark will be run as the program and everything to its right will be the program's input; otherwise, the program will have no input.",
    ["-[------->+<]>-.-[->+++++<]>++.+++++++..+++.[--->+<]>-----.--[->++++<]>-.--------.+++.------.--------.", ",.,.,.,.,.!Hello", ",.,.,.,.,.!1!+2!"],
    ["brainf", "bf"]
  ),
  "divisions": (
    ["country"],
    "List the first-level administrative divisions (provinces, states, etc.) of various countries. Various formats can be used, including common names, official names, and [ISO 3166-2 codes](https://en.wikipedia.org/wiki/ISO_3166-2). The divisions are taken from Wikidata.",
    ["Canada", "ch", "U.S. Minor Outlying Islands"],
    ["divs", "div", "states", "admindivs", "provinces", "regions"]
  ),
  "earthquakes": (
    ["", "number"],
    "Get a list of recent earthquakes from the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.csv).\n\nIf `number` is given, it will be the number of earthquakes returned. Otherwise, the command will return as many earthquakes as it can.",
    ["", "5"],
    ["earthquake", "eq"]
  ),
  "genimg": (
    ["", "size", "size resize", "size resize colstring"],
    """Generate a random image, optionally with a certain size and scale factor, and optionally excluding certain colours.

`size` specifies the width and height of the image in pixels. If it is provided, it can either be a single positive integer or two positive integers separated by `x`. If it is a single number, then it will be the width as well as the height; if it is two numbers, then the first number will be the width and the second one will be the height. The default image size is 200px by 200px (`200x200`, or simply `200`).

`resize` specifies the scaling of the image. It has the same format as `size`. For example, a value of `2` or `2x2` will effectively double the size of each pixel; to see this in action, try the 4th and 5th example. The default scale is `1x1`, or simply `1` (i.e. no resizing).

`colstring` must be made of three binary digits (`0` or `1`), which control the red, green, and blue channels of the image, respectively. `0` disables a colour while `1` enables it. For example, if the colstring is `100`, then only shades of red will be used in the generated image, and if it is `011`, then only shades of green and blue will be used. A colstring of `000` will generate a fully black image. The default colstring is `111` (all colours enabled).""",
    ["", "50", "100x50", "50 4", "100x25 2x8", "200 1 110", "10x20 20x10 001"]
  ),
  "makeimg": (
    ["", "size"],
    "Generate a random image. For a description of the `size` parameter, see `+help genimg`.",
    ["", "100", "100x50"]
  ),
  "rect": (
    ["id left top right bottom", "id left top right bottom red green blue"],
    """Draw a rectangle on an image.

`id` can either be `last`, `latest`, or a positive integer. If it is `last` or `latest`, the rectangle will be drawn on the most recently sent image (from `+genimg`, `+makeimg`, or `+viewimg`), which will then be edited to include the new rectangle; if `id` is an integer, the rectangle will drawn on the image whose ID is equal to `id` (images can be made using `+genimg` or `+makeimg`).

`left`, `top`, `right`, and `bottom` are measured in pixels and must be non-negative integers.

If `red`, `green`, and `blue` are supplied, then the matching RGB colour will be used as the colour of the rectangle; otherwise, it will be black.""",
    ["1 40 40 50 50", "1 100 105 195 190 255 125 0", "1 0 0 200 200 255 255 255"]
  ),
  "element": (
    ["clue"],
    "Get information about an element. `clue` can be its atomic number, symbol, or name.",
    ["5", "Pb", "vanadium"],
    ["el"]
  ),
  "wordelements": (
    ["words..."],
    "Break words into the symbols of chemical elements. See also `+wordelementsnames`.",
    ["xenon", "Unbreakable.", "More arsenic hospitalisation"],
    ["wel"]
  ),
  "wordelementsnames": (
    ["words..."],
    "Break words into the names of chemical elements. See also `+wordelements`.",
    ["names", "More arsenic hospitalisation"],
    ["weln", "welnames"]
  ),
  "solve": (
    ["equation..."],
    "Solve an equation. This command supports addition, subtraction, multiplication, division, and exponentiation, as well as parentheses (up to a point). `equation` can have whitespace.",
    ["(3/4) + 5"],
    ["s", "calculate", "calc"]
  ),
  "anagram": (
    ["", "text..."],
    "Make an anagram.",
    ["This is some text"],
    ["ana"]
  ),
  "trivia": (
    [""],
    "Get a trivia question.",
    [""],
    ["t"]
  ),
  "triviagram": (
    [""],
    "Get an anagrammed trivia question.",
    [""],
    ["tg"]
  ),
  "openstreetmap": (
    [""],
    "An OpenStreetMap viewer.",
    [""]
  ),
  "unusual": (
    [""],
    "Get a random article from Wikipedia's [list of unusual articles](https://en.wikipedia.org/wiki/Wikipedia:Unusual_articles).",
    [""]
  ),
  "xkcd": (
    [""],
    "Get a random xkcd comic.",
    [""]
  ),
  "calvinandhobbes": (
    [""],
    "Get a random Calvin and Hobbes comic.",
    [""],
    ["cah"]
  ),
  "markov": (
    ["sentence", "!max sentence"],
    'Generate a random "sentence" which should resemble the original `sentence`. This command uses, and is named for, [Markov chains](https://brilliant.org/wiki/markov-chains/).\n\nIf `max` is supplied and is greater than zero, it will be the maximum possible length of the resulting "sentence".\n\nSee also: `+markovword`, `+markovadjective`, `+markovnoun`, and `+markovverb`.',
    ["This is an example sentence", "!3 This is an example sentence"],
    ["m"]
  ),
  "markovword": (
    ["words", "!max words"],
    'Generate a random "word" which should resemble the original `words`. This command uses, and is named for, [Markov chains](https://brilliant.org/wiki/markov-chains/).\n\nIf `max` is supplied and is greater than zero, it will be the maximum possible length of the resulting "word".\n\nSee also: `+markov`, `+markovadjective`, `+markovnoun`, and `+markovverb`.',
    ["Java Python JavaScript csharp cplusplus objectivec rust", "Alden Alec Anton Arden Arlen Armand Arron Augustus Avery Benedict Bennett Branden Charles", "!4 Alden Alec Anton Arden Arlen Armand Arron Augustus Avery Benedict Bennett Branden"],
    ["markovwords", "mw"]
  ),
  "markovadjective": (
    [""],
    'Generate a random "adjective" using [Markov chains](https://brilliant.org/wiki/markov-chains/) and a list of more than 1000 real English adjectives.\n\nSee also: `+markov` and `+markovword`, `+markovnoun`, and `+markovverb`.',
    [""],
    ["madj", "ma"]
  ),
  "markovnoun": (
    [""],
    'Generate a random "noun" using [Markov chains](https://brilliant.org/wiki/markov-chains/) and a list of a few thousand real English nouns.\n\nSee also: `+markov`, `+markovword`, `+markovadjective`, and `+markovverb`.',
    [""],
    ["mnoun", "mn"]
  ),
  "markovverb": (
    [""],
    'Generate a random "verb" using [Markov chains](https://brilliant.org/wiki/markov-chains/) and a list of around 1000 real English verbs.\n\nSee also: `+markov`, `+markovword`, `+markovadjective`, and `+markovnoun`.',
    [""],
    ["mverb", "mv"]
  )
}

features_alias_dict = {}
for name, feature in features_help_dict.items():
  if len(feature) > 3:
    for alias in feature[3]:
      features_alias_dict[alias] = name

def bot_help(cmd_name):
  if cmd_name[0] == "+":
    cmd_name = cmd_name[1:]
  cmd_name = cmd_name.lower()
  
  if cmd_name in features_help_dict:
    cmd = features_help_dict[cmd_name]
  elif cmd_name in features_alias_dict:
    cmd_name = features_alias_dict[cmd_name]
    cmd = features_help_dict[cmd_name]
  else:
    description = f"**Command `+{cmd_name}` not found**"
    description += "\n\nTry `+features` for a list of commands. Please note that not all commands have help text yet."
    e = discord.Embed(description=description, color=0x242424)
    return e
  
  description = "**Usage:**"
  for usage in cmd[0]:
    sp = " " if len(usage) > 0 else ""
    description += f"\n• `+{cmd_name}{sp}{usage}`"
  description += "\n\n" + cmd[1]

  description += "\n\n**Examples:**"
  for example in cmd[2]:
    sp = " " if len(example) > 0 else ""
    description += f"\n• `+{cmd_name}{sp}{example}`"
  
  if len(cmd) > 3:
    description += "\n\nAliases: "
    description += ", ".join(f"`+{alias}`" for alias in cmd[3])
  
  e = discord.Embed(title=f"Help — `+{cmd_name}`", description=description, color=0x242424)
  return e
