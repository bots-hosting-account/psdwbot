import discord
import os, random
from PIL import Image, ImageDraw


async def generate_image(cmd_parts, message):
  w = h = 200
  if len(cmd_parts) > 1:
    size = cmd_parts[1]
    if size.isdigit():
      w = h = int(size)
    else:
      wh = size.split("x")
      if len(wh) == 2 and wh[0].isdigit() and wh[1].isdigit():
        w = int(wh[0]) or 200
        h = int(wh[1]) or 200
  
  if len(cmd_parts) > 3 and len(cmd_parts[3]) == 3:
    r, g, b = cmd_parts[3]
    if not (r in "01" and g in "01" and b in "01"):
      r = g = b = 1
    else:
      r = int(r)
      g = int(g)
      b = int(b)
  else:
    r = g = b = 1
  
  red = random.randint(0, 255) * r
  green = random.randint(0, 255) * g
  blue = random.randint(0, 255) * b
  
  image = Image.new("RGB", (w, h))
  colours = list((red, green, blue) for i in range(w * h))
  image.putdata(colours)
  
  rw = rh = 0
  if len(cmd_parts) > 2:
    resize = cmd_parts[2]
    if resize.isdigit():
      rw = rh = int(resize)
    else:
      rwh = resize.split("x")
      if len(rwh) == 2:
        try:
          rw = float(rwh[0])
          rh = float(rwh[1])
        except ValueError:
          pass
  
  if rw and rh:
    real_width = int(w * rw)
    real_height = int(h * rh)
    real_size = (real_width, real_height)
    image = image.resize(real_size, resample=Image.NEAREST)
  
  image.save("assets/images/genimg.png")
  with open("assets/images/genimg.png", "rb") as file_pointer:
    file = discord.File(file_pointer)
    await message.channel.send(file=file)
  
  image.save("assets/images/last.png")


async def make_image(cmd_parts, message):
  w = h = 200
  if len(cmd_parts) > 1:
    size = cmd_parts[1]
    if size.isdigit():
      w = h = int(size)
    else:
      wh = size.split("x")
      if len(wh) == 2 and wh[0].isdigit() and wh[1].isdigit():
        w = int(wh[0]) or 200
        h = int(wh[1]) or 200
  
  image = Image.new("RGB", (w, h), (255, 255, 255))
  
  try:
    with open("assets/images/count.txt") as f:
      image_id = int(f.read()) + 1
  except:
    image_id = 1
  
  image.save(f"assets/images/{image_id}.png")
  with open("assets/images/count.txt", "w") as f:
    f.write(str(image_id))
  
  await message.channel.send(f"Saved as {image_id}")


async def view_image(cmd_parts, message):
  image_id = cmd_parts[1] if len(cmd_parts) > 1 else ""
  
  id_is_valid = (image_id.isdigit() or image_id == "last")
  filename = f"assets/images/{image_id}.png"
  
  if id_is_valid and os.path.isfile(filename):
    image = Image.open(f"assets/images/{image_id}.png")
    image_size = f"{image.size[0]}x{image.size[1]}"
    
    with open(filename, "rb") as file_pointer:
      file = discord.File(file_pointer)
      await message.channel.send(image_size, file=file)
    
    #Copy image to last.png
    image.load()
    image.save("assets/images/last.png")
    image.close()
  
  else:
    await message.channel.send("No such image")


async def draw_rect(cmd_parts, message):
  if len(cmd_parts) < 5 or not all(map(str.isdigit, cmd_parts[2:6])):
    await message.channel.send("Usage: `+rect [image or last] left top right bottom red green blue`")
    return
  
  image_id = cmd_parts[1]

  id_is_valid = (image_id.isdigit() or image_id == "last")
  filename = f"assets/images/{image_id}.png"
  
  if id_is_valid and os.path.isfile(filename):
    image = Image.open(filename)
    image.load()
    
    draw = ImageDraw.Draw(image)
    pos_and_size = list(map(int, cmd_parts[2:6]))

    colour = cmd_parts[6:]
    if len(colour) == 3 and all(map(str.isdigit, colour)):
      colour = tuple(map(int, colour))
    else:
      colour = "black"

    print(pos_and_size, colour)
    draw.rectangle(pos_and_size, fill=colour, width=0)
    
    image.save(filename)
    if image_id != "last":
      image.save("assets/images/last.png")
  
    image_size = f"{image.size[0]}x{image.size[1]}"
    
    with open(filename, "rb") as file_pointer:
      file = discord.File(file_pointer)
      await message.channel.send(image_size, file=file)
  
  else:
    await message.channel.send("No such image")
