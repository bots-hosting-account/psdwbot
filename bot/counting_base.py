import sys

from connect_database import connection

class CountingBase:
  """
    Base class for different types of counting.
    
    Subclasses must define (all static or classmethods):
    - init_with_values(...values: type(get_val_from_message()))
    - get_current_number()
    - get_save_str()
    - did_beat_high_score()
    - update_high_score()
    - is_next(value: str)
    - update(value: str)
    - reset()
    - DATABASE_NAME, DISPLAY_NAME, and START_VALUE
    
    Subclasses may override (also all static or classmethods):
    - parse_save_str(save_str: str)
    - get_val_from_message(msg: discord.Message)
    - is_valid_input(value: str)
    - get_high_score()
    - MESSAGE_SAME_USER and/or MESSAGE_INCORRECT
    
    Don't forget to call initialise() on all subclasses
  """
  
  MESSAGE_SAME_USER = "You can't count two numbers in a row."
  MESSAGE_INCORRECT = "Wrong number."
  
  last_uid = None
  high_score = None

  @classmethod
  def parse_save_str(cls, save_str):
    return map(int, save_str.split(","))
  
  @classmethod
  def initialise(cls):
    with connection.cursor() as cursor:
      cursor.execute("SELECT save, highscore FROM counting WHERE name = :name", name=cls.DATABASE_NAME)
      save_str, high_score = cursor.fetchone()
      cls.init_with_values(*cls.parse_save_str(save_str))
      cls.high_score = int(high_score)
  
  @staticmethod
  def is_valid_input(value):
    return all(c in "0123456789" for c in value)

  @classmethod
  def get_high_score(cls):
    return cls.high_score

  @staticmethod
  def get_val_from_message(msg):
    return msg.content.lower().strip().split()[0]
  
  @classmethod
  async def check(cls, msg, client):
    if len(msg.content) == 0:
      return

    with connection.cursor() as cursor:
      val = cls.get_val_from_message(msg)
      if not cls.is_valid_input(val):
        return
      
      if msg.author.id != cls.last_uid and cls.is_next(val):
        await msg.add_reaction("\u2705")
        cls.last_uid = msg.author.id
        cls.update(val)
      
        if cls.did_beat_high_score():
          cls.update_high_score()
          high_score_str = str(cls.get_high_score())
          cursor.execute("UPDATE counting SET highscore = :highscore WHERE name = :name", highscore=high_score_str, name=cls.DATABASE_NAME)
      
      else:
        if msg.author.id == cls.last_uid:
          error = cls.MESSAGE_SAME_USER
        else:
          error = cls.MESSAGE_INCORRECT
        await msg.add_reaction("\u274c")
        await msg.reply(f"{msg.author.mention} RUINED IT AT **{cls.get_current_number()}**!! Next {cls.DISPLAY_NAME} is **{cls.START_VALUE}**. **{error}**")
        cls.last_uid = 0
        cls.reset()
      
      cursor.execute("UPDATE counting SET save = :save WHERE name = :name", save=cls.get_save_str(), name=cls.DATABASE_NAME)
      
      connection.commit()
