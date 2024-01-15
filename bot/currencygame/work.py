from discord import Embed
from discord_ui import Button

import random
import time
from asyncio.exceptions import TimeoutError as AETimeoutError

from connect_database import connection

import trivia
from .basic import commit_to_database, ensure, add_money, format
from .mathematics import (
  alter_digit, binomials_to_string, get_multiplied_polynomial_labels
)

jobs = {
  "kindergartener": {
    "article": "a",
    "base": 400,
    "bonus": 15,
    "name": "Kindergartener",
    "shifts": 0
  },
  "highschoolstudent": {
    "article": "a",
    "base": 1000,
    "bonus": 20,
    "name": "High School Student",
    "shifts": 5
  },
  "undergraduate": {
    "article": "an",
    "base": 2000,
    "bonus": 30,
    "name": "Undergraduate",
    "shifts": 10
  },
  "phdstudent": {
    "article": "a",
    "base": 3000,
    "bonus": 35,
    "name": "PhD Student",
    "shifts": 15
  },
  "postdoctorate": {
    "article": "a",
    "base": 4500,
    "bonus": 40,
    "name": "Postdoctorate",
    "shifts": 25
  },
  "historian": {
    "article": "a",
    "base": 5500,
    "bonus": 50,
    "name": "Historian",
    "shifts": 35
  }
}


def get_shifts_worked(uid):
  with connection.cursor() as cursor:
    row = cursor.execute("SELECT shifts FROM work WHERE userid = :uid", uid=str(uid))
  return row[0] if row is not None else 0

def add_work_shift(uid):
  with connection.cursor() as cursor:
    cursor.execute("UPDATE work SET shifts = shifts + 1 WHERE userid = :uid", uid=str(uid))


def get_job_id(uid):
  with connection.cursor() as cursor:
    row = cursor.execute("SELECT job FROM work WHERE userid = :uid", uid=str(uid))
  return row[0] if row is not None else None


async def work(cmd_parts, message, client):
  uid = message.author.id
  
  user_job_id = get_job_id(uid)
  if user_job_id is None:
    if len(cmd_parts) > 1:
      await apply(cmd_parts, message)
    else:
      e = Embed(description="You do not currently have a job. Use `+jobs` to see a list of available jobs.")
      await message.reply(embed=e)
    return
  
  labels = set()
  
  if user_job_id == "kindergartener":
    first = random.randint(-30, 30)
    second = random.randint(-30, 30)
    op = random.choice("+-")
    if second < 0:
      second = -second
      op = ("+" if op == "-" else "-")
    if op == "+":
      correct_answer = str(first + second)
    else:
      correct_answer = str(first - second)
    description = f"What is {first} {op} {second}?"
    labels.add(correct_answer)
  
  elif user_job_id == "highschoolstudent":
    first = random.randint(-50, 50)
    second = random.randint(-50, 50)
    op = random.choice("+-x")
    if op == "+":
      correct_answer = str(first + second)
    elif op == "-":
      correct_answer = str(first - second)
    else:
      correct_answer = str(first * second)
    description = f"What is {first} {op} {second}?"
    labels.add(correct_answer)
  
  elif user_job_id == "undergraduate":
    first = random.randint(1, 15)
    second = random.randint(1, 15)
    if random.randint(0, 1) == 0:
      a = random.randint(2, 4)
      a_str = a
    else:
      a = 1
      a_str = ""
    b = (first + second) * a
    c = (first * second) * a
    description = f"If {a_str}x² + {b}x + {c} = 0, and x is an integer, what "
    numbers_same = (first == second)
    if numbers_same:
      description += "is the value of x?"
    else:
      description += "are the possible values of x?"
    str_first = str(first)
    str_second = str(second)
    if numbers_same:
      correct_answer = "-" + str_first
      labels.add(correct_answer)
      while len(labels) < 4:
        first_altered = alter_digit(str_first)
        labels.add(f"-{first_altered}")
    else:
      correct_answer = "-" + str_first + ", -" + str_second
      labels.add(correct_answer)
      while len(labels) < 4:
        first_altered = alter_digit(str_first)
        second_altered = alter_digit(str_second)
        labels.add(f"-{first_altered}, -{second_altered}")
  
  elif user_job_id == "phdstudent":
    a = random.randint(1, 8) * random.choice((1, -1))
    b = random.randint(1, 8)
    c = random.randint(1, 8) * random.choice((1, -1))
    d = random.randint(1, 8)
    if random.randint(1, 3) == 1:
      factor = random.randint(2, 4)
    else:
      factor = ""
    ab_sign = random.choice("+-")
    cd_sign = random.choice("+-")
    a_str = ("" if a == 1 else ("-" if a == -1 else a))
    c_str = ("" if c == 1 else ("-" if c == -1 else c))
    description = f"What is the expanded form of the expression {factor}({a_str}x {ab_sign} {b})({c_str}x {cd_sign} {d})?"
    if ab_sign == "-":
      b *= -1
    if cd_sign == "-":
      d *= -1
    ac = a * c
    ad_bc = a * d + b * c
    bd = b * d
    if factor != "":
      ac *= factor
      ad_bc *= factor
      bd *= factor
    ac_str = ("" if ac == 1 else ("-" if ac == -1 else ac))
    ad_bc_abs = abs(ad_bc)
    ad_bc_sign = ("-" if ad_bc < 0 else "+")
    ad_bc_str = ("" if ad_bc_abs == 1 else str(ad_bc_abs))
    bd_abs = abs(bd)
    bd_sign = ("-" if bd < 0 else "+")
    bd_abs_str = str(bd_abs)
    correct_answer = f"{ac_str}x² {ad_bc_sign} {ad_bc_str}x {bd_sign} {bd_abs}"
    labels.add(correct_answer)
    while len(labels) < 4:
      ad_bc_altered = alter_digit(ad_bc_str)
      bd_altered = alter_digit(bd_abs_str)
      labels.add(f"{ac_str}x² {ad_bc_sign} {ad_bc_altered}x {bd_sign} {bd_altered}")
  
  elif user_job_id == "postdoctorate":
    first = [random.randint(1, 8) * random.choice((1, -1))]
    second = [random.randint(1, 8) * random.choice((1, -1))]
    first.append(random.randint(1, 8))
    second.append(random.randint(1, 8))
    if random.randint(1, 2) == 1:
      first.append(random.randint(1, 8))
    else:
      second.append(random.randint(1, 8))
    first = tuple(first)
    second = tuple(second)
    description = f"What is the expanded form of the expression {binomials_to_string(first, second)}?"
    correct_answer, all_answers = get_multiplied_polynomial_labels(first, second)
    labels.update(all_answers)
  
  elif user_job_id == "historian":
    result = trivia.get_question("hard")
    if result == False:
      await message.reply("Could not work as a Historian, please try again.")
      return
    question, answers, correct_answer_index = result
    description = question
    labels.update(answers)
    correct_answer = answers[correct_answer_index]
  
  else:
    await message.reply("Your job (" + user_job_id + ") is not valid. Please `+resign` and `+apply` for a different job.")
    return
  
  while len(labels) < 4:
    labels.add(alter_digit(correct_answer))
  labels = list(labels)
  random.shuffle(labels)
  buttons = [Button(color="blurple", label=str(label)) for label in labels]
  
  user_job = jobs[user_job_id]
  
  e = Embed(description=description, color=0x242424)
  reply = await message.reply(embed=e, components=buttons)
  try:
    timeout_value = 10
    start_time = time.time()
    btn = await reply.wait_for("button", client, by=message.author, timeout=timeout_value)
    await btn.respond(ninja_mode=True)
    end_time = time.time()
    duration = end_time - start_time
    
    chose_correct_answer = (btn.component.label == correct_answer)
    for button in buttons:
      button.disabled = True
      if button.label == btn.component.label:
        if chose_correct_answer:
          button.color = "green"
        else:
          button.color = "red"
      else:
        button.color = "grey"
    
    if chose_correct_answer:
      ensure(uid)
      
      earned = user_job["base"] + user_job["bonus"] * (timeout_value - round(duration))
      add_money(uid, earned)
      add_work_shift(uid)
      
      commit_to_database()
      
      e = Embed(title="Good work!", description=f"You earned {format(earned)} for your shift.", color=0x00ff00)
    
    else:
      e = Embed(title="Terrible work!", description="You earned nothing for your failure.", color=0xff0000)
    
    e.set_footer(text="Working as " + user_job["article"] + " " + user_job["name"])
    await reply.edit(embed=e, components=None)
  
  except AETimeoutError:
    for button in buttons:
      button.disabled = True
      button.color = "grey"
    
    await reply.edit(components=buttons)


async def list_jobs(message):
  uid = message.author.id

  shifts_worked = get_shifts_worked(uid)
  
  description = "The faster you complete a shift, the higher the bonus for that shift. Use `+apply` to apply for a job."
  for job in jobs.values():
    description += "\n\n"
    job_name = job["name"]
    shifts_to_unlock = job["shifts"]
    if shifts_worked < shifts_to_unlock:
      description += ":x: *" + job_name + "* (locked)"
    else:
      description += ":white_check_mark: **" + job_name + "**"
    description += f"\n* Base salary: {format(job['base'])}\n* Bonus per second: {format(job['bonus'])}\n* Successful shifts required to unlock: {shifts_to_unlock:,}"
  
  e = Embed(title="Job Listings", description=description)
  shift_s = "shift" if shifts_worked == 1 else "shifts"
  e.set_footer(text=f"You have worked {shifts_worked:,} {shift_s} successfully.")
  await message.reply(embed=e)


async def apply(cmd_parts, message):
  uid = message.author.id
  
  user_job_id = get_job_id(uid)
  if user_job_id is not None:
    if user_job_id in jobs:
      user_job = jobs[user_job_id]
      e = Embed(description=f"You are already working as {user_job['article']} **{user_job['name']}**. Use `+resign` to resign.")
    else:
      e = Embed(description=f"You are already working as {user_job_id}, which is an invalid job. Please `+resign` and `+apply` for a different job.")
    await message.reply(embed=e)
    return
  
  if len(cmd_parts) < 2:
    await message.reply("Usage: `+apply job_title`")
    return
  
  job_id = "".join(cmd_parts[1:]).replace("_", "").lower()
  if job_id in jobs:
    new_job = jobs[job_id]
    if get_shifts_worked(uid) >= new_job["shifts"]:
      with connection.cursor() as cursor:
        uid_str = str(uid)
        count_row = cursor.execute("SELECT COUNT(*) FROM work WHERE userid = :id", id=uid_str)
        if count_row[0] == 1:
          cursor.execute("UPDATE work SET job = :job WHERE userid = :uid", job=job_id, uid=uid_str)
        else:
          cursor.execute("INSERT INTO work (userid, job, shifts) VALUES (:uid, :job, 0)", uid=uid_str, job=job_id)
      
      commit_to_database()
      e = Embed(title="You are now working as " + new_job["article"] + " **" + new_job["name"] + "**", description=f"Your base salary per shift is {format(new_job['base'])}.")
    else:
      e = Embed(title="Not enough shifts", description="You do not have enough work experience to work as " + new_job["article"] + " **" + new_job["name"] + "**.")
  
  else:
    e = Embed(description="No such job exists. Use `+jobs` to see a list of available jobs.")
  
  await message.reply(embed=e)


async def resign(message):
  uid = message.author.id
  
  user_job_id = get_job_id(uid)
  if user_job_id is None:
    e = Embed(description="You do not currently have a job. Use `+jobs` to see a list of available jobs.")
    await message.reply(embed=e)
    return
  
  with connection.cursor() as cursor:
    cursor.execute("UPDATE work SET job = null WHERE userid = :uid", uid=str(uid))
  commit_to_database()
  
  if user_job_id in jobs:
    user_job = jobs[user_job_id]
    e = Embed(description=f"You resigned from your position as {user_job['article']} **{user_job['name']}**.")
  else:
    e = Embed(description="You resigned from your position as " + user_job_id + ".")
  
  await message.reply(embed=e)
