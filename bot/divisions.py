import requests
import country_converter

get_query = lambda iso: (
"""SELECT DISTINCT ?item ?itemLabel ?admindiv ?admindivLabel WHERE {
  ?item wdt:P150 ?admindiv.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  {
    SELECT DISTINCT ?item WHERE {
      ?item p:P150 ?statement0.
      ?statement0 (ps:P150/(wdt:P279*)) _:anyValueP150.
      ?item p:P297 ?statement1.
      ?statement1 (ps:P297) _:anyValueP297.
      ?item p:P297 ?iso.
      ?iso (ps:P297) \"""" + iso + """\".
    }
    LIMIT 300
  }
  MINUS {
    ?admindiv p:P1366 ?former.
    ?former (ps:P1366/(wdt:P279*)) _:anyValueP1366.
  }
}""")

QUERY_URL = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"

def get_iso_code(country):
  iso_code = country_converter.convert(names=[country], to="ISO2")
  if type(iso_code) == list:
    return iso_code[0]
  else:
    return iso_code

def get_short_name(country):
  short_name = country_converter.convert(names=[country], to="name_short")
  if type(short_name) == list:
    return short_name[0]
  else:
    return short_name

async def get_divisions(iso_code):
  params = {"query": get_query(iso_code), "format": "json"}
  data = requests.get(QUERY_URL, params=params).json()
  
  divisions = []
  for item in data["results"]["bindings"]:
    divisions.append(item["admindivLabel"]["value"])
  
  divisions.sort()
  return divisions


async def send_message(cmd_parts, message):
  if len(cmd_parts) < 2:
    command = cmd_parts[0]
    await message.reply(f"Usage: `+{command} country`\nTry `+help {command}` for more information.")
    return

  country = " ".join(cmd_parts[1:])
  iso_code = get_iso_code(country)
  if iso_code == "not found":
    await message.reply("The requested country does not exist. If it does, try using a different name.")
    return

  short_name = get_short_name(iso_code)
  divmsg = await message.reply(f"Fetching divisions for {short_name} ({iso_code}). This might take a minute...")

  divisions = await get_divisions(iso_code)
  divtext = "\n".join(divisions)
  if len(divtext) > 0:
    await divmsg.edit(divtext)
  else:
    await divmsg.edit("The requested country does not exist or has no administrative divisions.")
