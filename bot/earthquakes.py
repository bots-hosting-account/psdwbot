import urllib.request

url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.csv"

def get_lines():
  page = urllib.request.urlopen(url)
  charset = page.headers.get_content_charset()
  return page.read().decode(charset).split("\n")

def get_earthquake_data(line):
  date = line[:10]
  time = line[11:19]
  info = line[line.index('"') + 1:line.rindex('"')]
  mag = line.split(",")[4]
  return(f"{time} {date} — magnitude {mag}, {info}")

def get_n_earthquakes(n):
  lines = get_lines()
  data = []
  for i in range(n):
    line = lines[i + 1]
    data.append(get_earthquake_data(line))
  return data

def get_max_earthquakes():
  lines = get_lines()
  data = []
  total_len = 0
  i = 0
  while total_len <= 2000:
    line = lines[i + 1]
    dt = get_earthquake_data(line)
    data.append(dt)
    total_len += len(dt) + 1
    i += 1
  if total_len > 2000:
    data.pop()
  return data
