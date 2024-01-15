from counting_base import CountingBase

class CountingCustomFibonacci(CountingBase):
  DATABASE_NAME = "cuf"
  DISPLAY_NAME = "custom Fibonacci number"
  
  START_VALUE = "the next number entered"

  first_number = None
  second_number = None
  
  current_number = None
  next_number = None
  
  @classmethod
  def init_with_values(cls, *values):
    cls.last_uid = values[0]
    if len(values) >= 2:
      cls.first_number = values[1]
    if len(values) >= 3:
      cls.second_number = values[2]
    if len(values) >= 4:
      cls.current_number = values[3]
      cls.next_number = values[4]
  
  @classmethod
  def get_current_number(cls):
    if cls.current_number is None:
      return cls.first_number
    else:
      return cls.current_number
  
  @classmethod
  def get_save_str(cls):
    if cls.first_number is None:
      return str(cls.last_uid)
    elif cls.second_number is None:
      return f"{cls.last_uid},{cls.first_number}"
    else:
      return f"{cls.last_uid},{cls.first_number},{cls.second_number},{cls.current_number},{cls.next_number}"

  @classmethod
  def did_beat_high_score(cls):
    return cls.second_number is not None and cls.current_number > cls.second_number and cls.current_number > cls.high_score

  @classmethod
  def update_high_score(cls):
    cls.high_score = cls.current_number
  
  @classmethod
  def is_next(cls, value):
    return cls.second_number is None or int(value) == cls.next_number
  
  @classmethod
  def update(cls, value):
    if cls.first_number is None:
      cls.first_number = int(value)
    elif cls.second_number is None:
      cls.second_number = int(value)
      cls.current_number = cls.second_number
      cls.next_number = cls.first_number + cls.second_number
    else:
      cur = cls.current_number
      cls.current_number = cls.next_number
      cls.next_number += cur

  @classmethod
  def reset(cls):
    cls.first_number = None
    cls.second_number = None
    
    cls.current_number = None
    cls.next_number = None

CountingCustomFibonacci.initialise()
