def firstLetterHelper(s:str):
  words = s.split()
  new_word = ""
  for word in words:
    first = word[0]
    rest = word[1:]
    new_word = f'{new_word} ({first.upper()}|{first.lower()}){rest}'
  return new_word.strip()

def toTitleCase(s:str):
  return " ".join(map(lambda el : el[0].upper() + el[1:] , s.split(' ')))

def parseEntityDescription(desc:str):
  return desc.split("\n")[1]

def parseCivDescription(desc:str):
  spl = desc.split("\n")
  civ_type = spl[0].replace("<br>", "")
  bonuses = spl[2:]
  return { "civ_type": civ_type, "bonuses": bonuses }