import urllib.request
import re, random

def get_random_outlink(url, criteria, prefix):
  try:
    quoted_url = urllib.parse.quote(url).replace("%3A//", "://")
    page = urllib.request.urlopen(quoted_url)
    contents = str(page.read())
    pattern = '<a href="(.+?)">.*?</a>'
    links = re.findall(pattern, contents)
    
    links = [link for link in links if criteria(link)]
  
    if len(links) > 0:
      links = [k.split('"')[0] for k in links]
      return prefix + random.choice(links)
    else:
      return "No outlinks were found."
  
  except urllib.error.HTTPError as http_error:
    return str(http_error)

def is_valid_wikilink(link):
  return link.startswith("/wiki/") and ":" not in link and link != "/wiki/Main_Page"


def get_random_unusual_article():
  return get_random_wikipedia_outlink("Wikipedia:Unusual_articles")

def get_random_wikipedia_outlink(page_name):
  url = "https://en.wikipedia.org/wiki/" + page_name
  prefix = "https://en.wikipedia.org"
  return get_random_outlink(url, is_valid_wikilink, prefix)
