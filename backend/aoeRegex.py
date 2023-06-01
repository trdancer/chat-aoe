import re
import json
import helpers
from constants import QUESTION_TYPES

class AOERegex():
  civ_names = [
    "(A|a)ztecs",
    "(B|b)engalis",
    "(B|b)erbers",
    "(B|b)ohemians",
    "(B|b)ritons",
    "(B|b)ulgarians",
    "(B|b)urgundians",
    "(B|b)urmese",
    "(B|b)yzantines",
    "(C|c)elts",
    "(C|c)hinese",
    "(C|c)umans",
    "(D|d)ravidians",
    "(E|e)thiopians",
    "(F|f)ranks",
    "(G|g)oths",
    "(G|g)urjaras",
    "(H|h)industanis",
    "(H|h)uns",
    "(I|i)ncas",
    "(I|i)talians",
    "(J|j)apanese",
    "(K|k)hmer",
    "(K|k)oreans",
    "(L|l)ithuanians",
    "(M|m)agyars",
    "(M|m)alay",
    "(M|m)alians",
    "(M|m)ayans",
    "(M|m)ongols",
    "(P|p)ersians",
    "(P|p)oles",
    "(P|p)ortuguese",
    "(S|s)aracens",
    "(S|s)icilians",
    "(S|s)lavs",
    "(S|s)panish",
    "(T|t)atars",
    "(T|t)eutons",
    "(T|t)urks",
    "(V|v)ietnamese",
    "(V|v)ikings",
  ]
  # TODO add singular of civilization names like "Korean" or "Mayan"
  synonyms = {
    "camel": "camel rider",
    "camels": "camel rider",
    "heavy camel": "heavy camel rider",
    "heavy camels": "heavy camel rider",
    "imperial camel": "imperial camel rider",
    "imperial camels": "imperial camel rider",
    "crossbow": "crossbowman",
    "crossbows": "crossbowman",
    "arbalest": "arbesester",
    "arbalests": "arbesester",
    "hca": "Heavy Cavalry Archer",
    "bbc": "Bombard Cannon",
    "so": "siege onager",
    "ram": "battering ram",
    "rams": "battering ram",
    "mango": "mangonel",
    "mangos": "mangonel",
    "janis": "janissary",
    "shotel": "shotel warrior",
    "shotels": "shotel warrior",
    "elite shotel": "elite shotel warrior",
    "elite shotels": "elite shotel warrior",
    "karambit": "karambit warrior",
    "karambits": "karambit warrior",
    "elite karambit": "elite karambit warrior",
    "elite karambits": "elite karambit warrior",
    "fire": "fire ship",
    "fires": "fire ship",
    "fast fire": "fast fire ship",
    "fast fires": "fast fire ship",
    "demo": "demolition ship",
    "demos": "demolition ship",
    "transport": "transport ship",
    "transports": "transport ship",
    "rattan": "rattan archer",
    "rattans": "rattan archer",
    "rattan": "rattan archer",
    "elite rattan": "elite rattan archer",
    "elite rattans": "elite rattan archer",
    "palisade": "palisade wall",
    "palisades": "palisade wall",
    "wall": "stone wall",
    "walls": "stone wall",
    "scout": "scout cavalry",
    "scouts": "scout cavalry",
    "light cav": "light cavalry",
    "light cavs": "light cavalry",
    "urumi": "urumi swordsman",
    "urumis": "urumi swordsman",
    "elite urumi": "elite urumi swordsman",
    "elite urumis": "elite urumi swordsman",
    "spear": "spearman",
    "spears": "spearman",
    "pike": "pikeman",
    "pikes": "pikeman",
    "halb": "halberdier",
    "halbs": "halberdier",
    "steppies": "steppe lancer",
    "elite steppies": "elite steppe lancers",
    "chakram": "chakram thrower",
    "chakrams": "chakram thrower",
    "elite chakram": "elite chakram thrower",
    "elite chakrams": "elite chakram thrower",
    "shrivamsha": "shrivamsha rider",
    "shrivamshas": "shrivamsha rider",
    "elite shrivamsha": "elite shrivamsha rider",
    "elite shrivamshas": "elite shrivamsha rider",
    "axeman": "throwing axeman",
    "axemen": "throwing axeman",
    "elite axeman": "elite throwing axeman",
    "elite axemen": "elite throwing axeman",
    "woad": "woad raider",
    "woads": "woad raider",
    "woadies": "woad raider",
    "elite woad": "elite woad raider",
    "elite woads": "elite woad raider",
    "elite woadies": "elite woad raiders",
    "jaguar": "jaguar warrior",
    "jaguars": "jaguar warrior",
    "jags": "jaguar warrior",
    "elite jaguar": "elite jaguar warrior",
    "elite jaguars": "elite jaguar warrior",
    "elite jags": "elite jaguar warrior",
    "eagle": "eagle warrior",
    "eagles": "eagle warrior",
    "elite eagle": "elite eagle warrior",
    "elite eagles": "elite eagle warrior",
    "plume": "plumed archer",
    "plumes": "plumed archer",
    "elite plume": "elite plumed archer",
    "elite plumes": "elite plumed archer",
    "conq": "conquistador",
    "conqs": "conquistador",
    "elite conq": "elite conquistador",
    "elite conqs": "elite conquistador",
    "genoese": "genoese crossbowman",
    "genoese crowssbow": "genoese crossbowman",
    "elite genoese": "elite genoese crossbowman",
    "elite genoese crossbow": "elite genoese crossbowman",
    "magyar hussar": "magyar huszar",
    "magyar hussars": "magyar huszar",
    "elite magyar hussar": "elite magyar huszar",
    "elite magyar hussars": "elite magyar huszar",
    "turtle": "turtle ship",
    "turtles": "turtle ship",
    "elite turtle": "elite turtle ship",
    "elite turtles": "elite turtle ship",
    "carto": "cartography",
    "scale mail": "Scale Mail Armor",
    "chain mail": "Chain Mail Armor",
    "plate mail": "Plate Mail Armor",
    "plate barding": "Plate Barding Armor",
    "scale barding": "Scale Barding Armor",
    "chain barding": "Chain Barding Armor",
    "padded archer": "Padded Archer Armor",
    "leather archer": "Leather Archer Armor",
    "ring archer": "ring archer armor",
    "feudal": "feudal age",
    "imperial": "imperial age",
    "parthian": "parthian tactics"
  }
  entities_match = None
  weak_entities_match = None
  civ_name_match = None
  cost_matches = None
  civ_posession_matches = None
  info_matches = None
  unique_unit_match = None
  unique_tech_match = None
  entity_possession_match = None

  def __init__(self, strings_filename):
    strings_file = open(strings_filename)
    id_description_map = json.load(strings_file)
    entities_list = ['(' + helpers.firstLetterHelper(re.sub("\(|\)", "", e)) + ')' for e in list(id_description_map.values())[0:418]]
    entities_string = "|".join(entities_list)
    self.weak_entities_match = entities_string
    temp_synonyms_string = ['(' + k + ')' for k in self.synonyms.keys()]
    self.entities_match = f'{"|".join(temp_synonyms_string)}|{entities_string}'

    self.civ_name_match = "|".join(self.civ_names)

    # TODO add 'price' key word
    self.cost_matches = list(map(re.compile, [
      f'(H|h)ow much do(es)? (?P<subject>{self.entities_match}) cost',
      f'((W|w)hat do(es)? )?(?P<subject>{self.entities_match}) cost',
      f'((W|w)hat is )?((T|t)he )?(C|c)ost (of )?(?P<subject>{self.entities_match})',
    ]))

    self.civ_posession_matches = list(map(re.compile, [
      f'((D|d)o(es)? )?(?P<civilization_name>{self.civ_name_match}) (get(s)?|have|has) (?P<subject>{self.entities_match})',
    ]))

    self.info_matches = list(map(re.compile, [
      f'(W|w)hat (does )?(?P<subject>{self.entities_match}) do',
      f'(T|t)ell me about (?P<subject>{self.entities_match})',
      f'(E|e)xplain (?P<subject>{self.entities_match})',
      f'^(?P<subject>{self.entities_match})$'
    ]))
    self.unique_tech_match = list(map(re.compile, [
      f'((W|w)hat (is|are) )?(?P<civilization_name>{self.civ_name_match})((\')?s)? ((?P<age>(C|c)astle|(I|i)mperial) (age )?)?(unique tech((nologie|nology)?)|UT|ut)s?',
    ]))

    self.unique_unit_match = list(map(re.compile, [
      f'((W|w)hat (is|are) )?(?P<civilization_name>{self.civ_name_match})((\')?s)? (unique unit|UU|uu)s?',
    ]))

    self.entity_possession_match = list(map(re.compile, [
      f'(((W|w)h(at|ich) )?((is|are) )?)?((T|t)he )?(C|c)iv(ilization)?s? ((that )?(get|have)|with) (?P<subject>{self.entities_match})',
    ]))
  # TODO add "the" support before entities
  # TODO logical operators of civs that get X but not Y, AND Y, OR Y
  # TODO This vs. that only if they are same entity class


  def getMatchEntity(self, match):
    subject = match.group('subject')
    real_entity_name = self.synonyms.get(subject, subject).lower()
    return real_entity_name

  def extract_civilization(self, match):
    return match.group('civilization_name')
  
  def extract_entities_possession(self, match):
    return (self.getMatchEntity(match), match.group('civilization_name'))

  def extract_age(self, match):
    return match.group('age')
  
  def parseQuestionWithMatches(self, question:str, matches):
    for pattern in matches:
      m = pattern.search(question)
      if (m):
        return m
    return None

  def parseQuestion(self, question:str):
    cleaned_question = re.sub("\?|\.", "", question).strip(" ")
    match_result = None
    try:
      match_result = self.parseQuestionWithMatches(cleaned_question, self.civ_posession_matches)
      if match_result:
        return (self.extract_entities_possession(match_result), QUESTION_TYPES["POSSESSION"])
      
      match_result = self.parseQuestionWithMatches(cleaned_question, self.cost_matches)
      if (match_result):
        return (self.getMatchEntity(match_result), QUESTION_TYPES["COST"])
      
      match_result = self.parseQuestionWithMatches(cleaned_question, self.info_matches)
      if (match_result):
        return (self.getMatchEntity(match_result), QUESTION_TYPES["INFO"])
      
      match_result = self.parseQuestionWithMatches(cleaned_question, self.unique_unit_match)
      if (match_result):
        return (self.extract_civilization(match_result), QUESTION_TYPES["UNIQUE_UNIT"])
      
      match_result = self.parseQuestionWithMatches(cleaned_question, self.unique_tech_match)
      if (match_result):
        return ((self.extract_civilization(match_result), self.extract_age(match_result)), QUESTION_TYPES["UNIQUE_TECH"])
      
      match_result = self.parseQuestionWithMatches(cleaned_question, self.entity_possession_match)
      if (match_result):
        return (self.getMatchEntity(match_result), QUESTION_TYPES["ENTITY_POSSESSION"])
      
      
      return None
    except Exception as e:
      print(e)
      return None

  # Return a list of all identifiable AOE entity strings from a given string
  def extractEntities(self, s):
    m = re.findall(self.weak_entities_match, s)
    es = [list(filter(lambda en : len(en) > 1, list(ms))) for ms in m]
    flat = [helpers.toTitleCase(e) for ls in es for e in ls]
    unique_entities = list(set(flat))
    return unique_entities
