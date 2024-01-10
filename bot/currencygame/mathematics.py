import random

variables = ("", "x", "x²", "x³")


def alter_digit(n):
  if n[0] == "-":
    minimum_index = 1
  else:
    minimum_index = 0
  index = random.randrange(minimum_index, len(n))
  if index == int(n[0] == "-"):
    minimum_digit = 1
  else:
    minimum_digit = 0
  new_digit = str(random.randint(minimum_digit, 9))
  return n[:index] + new_digit + n[index + 1:]


def binomials_to_string(*binomials):
  result = ""
  for binomial in binomials:
    result += "("
    if binomial[0] > 1:
      result += str(binomial[0])
    elif binomial[0] == -1:
      result += "-"
    elif binomial[0] != 1:
      result += str(binomial[0])
    variable_index = len(binomial) - 1
    result += variables[variable_index]
    for i, term in enumerate(binomial[1:]):
      if term > 1:
        result += " + " + str(term)
      elif term < -1:
        result += " - " + str(abs(term))
      elif term == 1:
        result += " + "
        if i == len(binomial) - 2:
          result += str(term)
      elif term == -1:
        result += " - "
        if i == len(binomial) - 2:
          result += str(abs(term))
      variable_index -= 1
      result += variables[variable_index]
    result += ")"
  return result


def multiply_polynomials(first, second):
  result = []
  max_first_order = len(first) - 1
  max_second_order = len(second) - 1
  for i, first_term in enumerate(first):
    first_order = max_first_order - i
    for j, second_term in enumerate(second):
      print(first_term,"x",second_term,"@",i,j)
      order = first_order + (max_second_order - j)
      result.append((first_term * second_term, order))
  return result


def get_multiplied_polynomial_labels(first, second):
  product = multiply_polynomials(first, second)
  
  order_map = {}
  for term, order in product:
    if order in order_map:
      order_map[order] += term
    else:
      order_map[order] = term
  
  result = []
  orders = sorted(order_map.keys(), reverse=True)
  for order in orders:
    result.append((order_map[order], order))

  labels = set()
  correct = ""
  template = []
  coefficient_strings = []
  
  if result[0][0] == 1:
    correct = ""
  elif result[0][0] == -1:
    correct = "-"
    template.append("-")
  else:
    first_coefficient = str(result[0][0])
    correct = first_coefficient
    template.append(True)
    coefficient_strings.append(first_coefficient)
  correct += variables[result[0][1]]
  template.append(variables[result[0][1]])
  for term, order in result[1:]:
    if term != 0:
      if term < 0:
        correct += " - "
        template.append(" - ")
        if term != -1 or order == 0:
          coefficient = str(abs(term))
          correct += coefficient
          template.append(True)
          coefficient_strings.append(coefficient)
      else:
        correct += " + "
        template.append(" + ")
        if term != 1 or order == 0:
          coefficient = str(term)
          correct += coefficient
          template.append(True)
          coefficient_strings.append(coefficient)
      correct += variables[order]
      if order > 0:
        template.append(variables[order])
  
  labels.add(correct)
  while len(labels) < 4:
    label = ""
    coefficient_index = 0
    for term in template:
      if term == True:
        coefficient = coefficient_strings[coefficient_index]
        label += alter_digit(coefficient)
        coefficient_index += 1
      else:
        label += term
    labels.add(label)
  
  return correct, labels
