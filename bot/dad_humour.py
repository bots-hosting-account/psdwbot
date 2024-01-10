from PIL import ImageDraw, ImageFont
import Image, random

def draw_rand_line(draw, xmin, ymin, xmax, ymax):
  xo1 = random.randint(-5, 5)
  xo2 = random.randint(-5, 5)
  y1 = random.randint(ymin - 5, ymax + 5)
  y2 = random.randint(ymin - 5, ymax + 5)
  
  draw.line((xmin + xo1, y1, xmax + xo2, y2), fill=0, width=5)

def add_to_image(name, time):
  font = ImageFont.truetype("assets/images/Roboto-Regular.ttf", 30)
  
  img = Image.open("assets/images/dad.jpg")
  img.load()
  
  draw = ImageDraw.Draw(img)
  draw.text((236, 16), name, (255, 255, 255), font=font)
  
  if len(time) == 5:
    font2 = ImageFont.truetype("assets/images/Roboto-Regular.ttf", 23)
    draw.text((404, 150), time, (255, 255, 255), font=font2)
  else:
    font2 = ImageFont.truetype("assets/images/Roboto-Regular.ttf", 24)
    draw.text((410, 150), time, (255, 255, 255), font=font2)

  for i in range(5):
    #Name
    draw_rand_line(draw, 76, 32, 229, 44)
    #Time
    draw_rand_line(draw, 412, 184, 453, 194)
  
  img.save("assets/images/dad2.jpg")
