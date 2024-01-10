from counting_base import CountingBase

class CountingChess(CountingBase):
  DATABASE_NAME = "chs"
  DISPLAY_NAME = "word"
  
  START_VALUE = "chess"
  
  MESSAGE_SAME_USER = 'You can\'t say "chess" twice in a row.'
  
  count = 0
  
  @classmethod
  def init_with_values(cls, last_uid, count):
    cls.last_uid = last_uid
    cls.count = count
  
  @classmethod
  def get_current_number(cls):
    return cls.count
  
  @classmethod
  def get_save_str(cls):
    return f"{cls.last_uid},{cls.count}"

  @classmethod
  def did_beat_high_score(cls):
    return cls.count > cls.high_score

  @classmethod
  def update_high_score(cls):
    cls.high_score = cls.count
  
  @staticmethod
  def is_next(value):
    #There is only one possible value
    return True
  
  @classmethod
  def update(cls, _value):
    cls.count += 1

  @classmethod
  def reset(cls):
    cls.count = 0

  @staticmethod
  def get_val_from_message(msg):
    return msg.content
  
  @staticmethod
  def is_valid_input(value):
    return "chess" in value.lower()

CountingChess.initialise()
