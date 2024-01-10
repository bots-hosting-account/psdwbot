from counting_base import CountingBase

def is_prime(n):
  for i in range(2, n // 2 + 1):
    if n % i == 0:
      return False
  return True

def get_next_prime_after(number):
  while True:
    number += 1
    if is_prime(number):
      return number

class CountingPrime(CountingBase):
  DATABASE_NAME = "prm"
  DISPLAY_NAME = "prime number"
  
  START_VALUE = "2"

  prime_count = 0
  current_number = 0
  next_number = 0

  @classmethod
  def init_with_values(cls, last_uid, prime_count, current_number, next_number):
    cls.last_uid = last_uid
    cls.prime_count = prime_count
    cls.current_number = current_number
    cls.next_number = next_number
  
  @classmethod
  def get_current_number(cls):
    return cls.current_number
  
  @classmethod
  def get_save_str(cls):
    return f"{cls.last_uid},{cls.prime_count},{cls.current_number},{cls.next_number}"

  @classmethod
  def did_beat_high_score(cls):
    return cls.prime_count > cls.high_score

  @classmethod
  def update_high_score(cls):
    cls.high_score = cls.prime_count
  
  @classmethod
  def is_next(cls, value):
    return int(value) == cls.next_number
  
  @classmethod
  def update(cls, _value):
    cls.prime_count += 1
    cls.current_number = cls.next_number
    cls.next_number = get_next_prime_after(cls.next_number)

  @classmethod
  def reset(cls):
    cls.prime_count = 0
    cls.current_number = 0
    cls.next_number = 2

CountingPrime.initialise()
