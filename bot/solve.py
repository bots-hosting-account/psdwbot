class TokenType:
  Empty = "Empty"
  Num = "Num"
  Add = "Add"
  Sub = "Sub"
  Mul = "Mul"
  Div = "Div"
  Pow = "Pow"
  BrL = "BrL"
  BrR = "BrR"
  Ops = (Add, Sub, Mul, Div, Pow)
  Brks = (BrL, BrR)
  
  @staticmethod
  def get_from(c):
    if c in "0123456789.":
      return TokenType.Num
    elif c == "+":
      return TokenType.Add
    elif c == "-":
      return TokenType.Sub
    elif c == "*":
      return TokenType.Mul
    elif c == "/":
      return TokenType.Div
    elif c == "^":
      return TokenType.Pow
    elif c == "(":
      return TokenType.BrL
    elif c == ")":
      return TokenType.BrR
    else:
      return TokenType.Empty

class Token:
  def __init__(self, value, type):
    self.value = value
    self.type = type
  def __repr__(self):
    return f"{self.type}: {self.value}"
  def __str__(self):
    return self.__repr__()

def solve_equation(equation):
  equation = "".join(equation.split())
  equation = equation.replace("÷", "/")
  equation = equation.replace("**", "^")
  parsed = parse_equation(equation)
  
  if parsed is None or not valid(parsed):
    return None
  
  result = parse(parsed)
  if result is None:
    return None
  
  if len(result) != 1 or result[0].type != TokenType.Num:
    return None
  
  result = result[0].value

  try:
    result = round(result, 10)
  except TypeError:
    result = round(float(result), 10)
  if result % 1 == 0:
    result = int(result)
  return result

def match_brackets(toks):
  brk = {}
  tmp = []
  for i, t in enumerate(toks):
    if t.type == TokenType.BrL:
      tmp.append(i)
    elif t.type == TokenType.BrR:
      if len(tmp) < 1:
        return None
      b = tmp.pop()
      brk[i] = b
      brk[b] = i
  return None if len(tmp) > 0 else brk

def parse_equation(equation):
  ct = equation[0]
  cty = TokenType.get_from(ct)
  toks = []
  
  for c in equation[1:]:
    if cty in TokenType.Brks:
      toks.append(Token(ct, cty))
      ct = c
      cty = TokenType.get_from(c)
      continue
    
    tt = TokenType.get_from(c)
    if tt == TokenType.Empty:
      return None
    elif tt == cty:
      ct += c
    else:
      toks.append(Token(ct, cty))
      ct = c
      cty = tt
  if len(ct) > 0:
    toks.append(Token(ct, cty))
  
  return toks

def valid(parsed):
  for t in parsed:
    if t.type in TokenType.Ops and len(t.value) != 1:
      return False
    elif t.type == TokenType.Num:
      if t.value.count(".") > 1 or t.value == ".":
        return False
      if t.value.startswith("."):
        t = "0" + t
      if t.value.endswith("."):
        t += "0"
  return True

def parse(toks):
  if toks[-1].type in TokenType.Ops:
    return None

  brk = match_brackets(toks)
  if brk is None:
    return None
  
  while len(brk) > 0:
    if not any(map(lambda tn: tn.type in TokenType.Brks, toks)):
      break
    
    v = max(brk.keys())
    k = brk[v]
    replacement = parse(toks[k + 1:v])
    if replacement is None:
      return None
    tlm = len(toks[k:v + 1]) - len(replacement)
    toks[k:v + 1] = replacement
    
    if len(toks) == 1:
      return toks
    
    del brk[k]
    del brk[v]
    brk_old = brk.copy()
    for nk in brk_old:
      if max(nk, brk_old[brk_old[nk]]) >= k:
        brk[brk_old[nk]] -= tlm
  
  solve_implicit_mul(toks)
  
  if not (solve_binop(toks, {
        TokenType.Pow: lambda x, y: x ** y
      })
      and solve_binop(toks, {
        TokenType.Mul: lambda x, y: x * y,
        TokenType.Div: lambda x, y: y and x / y
      })
      and solve_binop(toks, {
        TokenType.Add: lambda x, y: x + y,
        TokenType.Sub: lambda x, y: x - y
      })):
    return None
  
  return toks

def solve_implicit_mul(toks):
  i = 0
  while i < len(toks) - 1:
    if toks[i].type == toks[i + 1].type == TokenType.Num:
      product = parse_value(toks[i].value) * parse_value(toks[i + 1].value)
      toks[i] = Token(product, TokenType.Num)
      del toks[i + 1]
    else:
      i += 1

def solve_binop(toks, type_op_fn_dict):
  i = 0
  while i < len(toks):
    if toks[i].type in type_op_fn_dict:
      if not (toks[i - 1].type == toks[i + 1].type == TokenType.Num):
        return False
      
      toks[i] = Token(type_op_fn_dict[toks[i].type](parse_value(toks[i - 1].value), parse_value(toks[i + 1].value)), TokenType.Num)
      del toks[i + 1]
      del toks[i - 1]
      i -= 2
    i += 1
  return True

def parse_value(value):
  if isinstance(value, str):
    if value.isdigit():
      return int(value)
    else:
      return float(value)
  else:
    return value
