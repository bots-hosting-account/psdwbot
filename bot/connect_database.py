import oracledb

from connect_database_internal import get_connection

class _Connection:
  def __init__(self):
    self.con = get_connection()
  
  def cursor(self):
    cursor = self.con.cursor()
    try:
      cursor.execute("SELECT NULL FROM DUAL")
    except AttributeError:
      self.con.close()
      self.con = get_connection()
      cursor = self.con.cursor()
    return cursor
  
  def commit(self):
    self.con.commit()

connection = _Connection()
