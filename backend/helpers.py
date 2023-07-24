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
  civType = spl[0].replace("<br>", "")
  bonuses = spl[2:]
  return { "civType": civType, "bonuses": bonuses }

def parseFileNameVersion(filename:str):
  # assumes filename is named like so:
  # patch_{version}_data
  splitString = filename.split('_')
  if (len(splitString) < 2):
    raise Exception("Invalid data file name")
  return splitString[1]

def lowerCaseKeys(d:dict):
  new_dict:dict = {}
  for key, value in d.items():
    new_dict[key.lower()] = value
  return new_dict

def makeArmorAttackDict(a:dict):
  return {
    "armorId": a["Class"],
    "amount": a["Amount"],
  }