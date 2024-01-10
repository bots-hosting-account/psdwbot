from discord_ui import Button
from asyncio.exceptions import TimeoutError as AETimeoutError
import urllib.request, json, random, re
from anagram import anagram
import currencygame as cg

TRIVIA_URL = "http://masonmackinnon.com/trivia/api.php"


async def run(message, client, is_triviagram):
  result = get_question()
  if result == False:
    await message.channel.send("Error: Could not get trivia")
    return
  
  question, answers, correct_answer_index = result
  
  if is_triviagram:
    print("TG:", question, answers)
    answers = list(map(lambda a: anagram(a).title(), answers))
    question = anagram(question).title() + "?"
  
  correct_answer = answers[correct_answer_index]
  pre = random.randint(1, 1000000)
  buttons = []
  for i in range(4):
    buttons.append(Button(custom_id=f"{pre}trivia{i + 1}", color="blurple", label=answers[i]))
  
  question_msg = await message.channel.send(content=question, components=[buttons[:2], buttons[2:]])

  try:
    answered = await question_msg.wait_for("button", client, by=message.author, timeout=20)
    correct = answered.component.label == correct_answer

    colour = "green" if correct else "red"
    
    for button in buttons:
      if answered.component.label == button.label:
        button.color = colour
      else:
        button.color = "gray"
      button.disabled = True
    
    question_msg = await question_msg.edit(content=question, components=[buttons[:2], buttons[2:]])
    
    user = message.author.mention
    
    if correct:
      await answered.channel.send(f"{user} is correct!")
      cg.add_money(message.author.id, 500)
    else:
      await answered.channel.send(f"{user} is an idiot, the correct answer is {correct_answer} of course")
    
    await answered.respond(ninja_mode=True)
  except AETimeoutError:
    for button in buttons:
      button.color = "gray"
      button.disabled = True
    await question_msg.edit(content=question, components=[buttons[:2], buttons[2:]])


def get_question(difficulty=None):
  request_url = TRIVIA_URL
  if difficulty is not None:
    request_url += "?difficulty=" + difficulty
  
  with urllib.request.urlopen(request_url) as url:
    url_content = url.read().decode()
    try:
      data = json.loads(url_content)
    except Exception as e:
      raise e
    if "error" in data:
      return False
  
  answers = tuple(re.sub(
    '(&#[0-9]{3};)', lambda m: chr(int(m.group(1)[2:5])), data[f"ans{i}"]
  ) for i in range(1, 5))
  
  question = data["question"]
  correct_answer_index = int(data["correct"]) - 1
  return question, answers, correct_answer_index
