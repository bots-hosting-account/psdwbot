import math
from discord import Embed

osm_msg = None
osm_zoomlatlong = None

OSM_URL = "https://a.tile.openstreetmap.fr/osmfr/{}/{}/{}.png"

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

async def send_tile_img(lat, long, zoom, channel):
  global osm_msg, osm_zoomlatlong
  tx, ty = deg2num(lat, long, zoom)
  attribution = "© OpenStreetMap contributors | https://www.openstreetmap.org/copyright"
  em = Embed()
  url = OSM_URL.format(zoom, tx, ty)
  print(url)
  em.set_image(url=url)
  osm_msg = await channel.send(attribution, embed=em)
  osm_zoomlatlong = (zoom, lat, long)

async def zoomin(message):
  global osm_msg, osm_zoomlatlong
  if osm_zoomlatlong is None:
    await message.reply("Cannot zoom in to nothing, use the `+osm` command first")
  else:
    zoom, lat, long = osm_zoomlatlong
    if zoom < 19:
      zoom += 1
      osm_zoomlatlong = (zoom, lat, long)
      em = Embed()
      tx, ty = deg2num(lat, long, zoom)
      url = OSM_URL.format(zoom, tx, ty)
      em.set_image(url=url)
      await osm_msg.edit(osm_msg.content, embed=em)
    else:
      await message.reply("Cannot zoom in any further")

async def zoomout(message):
  global osm_msg, osm_zoomlatlong
  if osm_zoomlatlong is None:
    await message.reply("Cannot zoom out of nothing, use the `+osm` command first")
  else:
    zoom, lat, long = osm_zoomlatlong
    if zoom > 0:
      zoom -= 1
      osm_zoomlatlong = (zoom, lat, long)
      em = Embed()
      tx, ty = deg2num(lat, long, zoom)
      url = OSM_URL.format(zoom, tx, ty)
      em.set_image(url=url)
      await osm_msg.edit(osm_msg.content, embed=em)
    else:
      await message.reply("Cannot zoom out any further")
