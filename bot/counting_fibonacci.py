from counting_base import CountingBase

class CountingFibonacci(CountingBase):
  DATABASE_NAME = "fib"
  DISPLAY_NAME = "Fibonacci number"
  
  START_VALUE = "0"
  
  current_number = None
  next_number = None
  
  @classmethod
  def init_with_values(cls, *values):
    cls.last_uid = values[0]
    if len(values) == 3:
      cls.current_number = values[1]
      cls.next_number = values[2]
    else:
      cls.current_number = 1
      cls.next_number = 0
  
  @classmethod
  def get_current_number(cls):
    return cls.current_number

  @classmethod
  def get_save_str(cls):
    return f"{cls.last_uid},{cls.current_number},{cls.next_number}"
  
  @classmethod
  def did_beat_high_score(cls):
    return cls.current_number > cls.high_score
  
  @classmethod
  def update_high_score(cls):
    cls.high_score = cls.current_number

  @classmethod
  def is_next(cls, value):
    return int(value) == cls.next_number
  
  @classmethod
  def update(cls, value):
    cur = cls.current_number
    cls.current_number = cls.next_number
    cls.next_number += cur
  
  @classmethod
  def reset(cls):
    cls.current_number = 1
    cls.next_number = 0

CountingFibonacci.initialise()
