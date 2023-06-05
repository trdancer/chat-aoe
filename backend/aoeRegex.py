import re
import json
import helpers
from constants import QUESTION_TYPES
import logging
logging.basicConfig(filename="logs/queries.log", level=logging.DEBUG)

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
    "parthian": "parthian tactics",
  }
  civ_synonyms = {
    "Aztec": "aztecs",
    "aztec": "aztecs",
    "Bengali": "bengalis",
    "bengali": "bengalis",
    "Berber": "berbers",
    "berber": "berbers",
    "Bohemian": "bohemians",
    "bohemian": "bohemians",
    "Briton": "britons",
    "briton": "britons",
    "Bulgarian": "bulgarians",
    "bulgarian": "bulgarians",
    "Burgundian": "burgundians",
    "burgundian": "burgundians",
    "Burma": "burmese",
    "burma": "burmese",
    "Byzantine": "byzantines",
    "byzantine": "byzantines",
    "Celt": "celts",
    "celt": "celts",
    "China": "chinese",
    "china": "chinese",
    "Cuman": "cumans",
    "cuman": "cumans",
    "Dravidian": "dravidians",
    "dravidian": "dravidians",
    "Ethiopian": "ethiopians",
    "ethiopian": "ethiopians",
    "Frank": "franks",
    "frank": "franks",
    "Goth": "goths",
    "goth": "goths",
    "Gurjara": "Gurjaras",
    "gurjara": "gurjaras",
    "Gurjar": "Gurjaras",
    "gurjar": "gurjaras",
    "Hindustani": "Hindustanis",
    "hindustani": "hindustanis",
    "Hun": "Huns",
    "hun": "huns",
    "Inca": "Incas",
    "inca": "incas",
    "Incan": "Incas",
    "incan": "incas",
    "Italian": "Italians",
    "italian": "italians",
    "Italy": "Italians",
    "italy": "italians",
    "Japan": "Japanese",
    "japan": "japanese",
    # "Khmer": "Khmers",
    # "khmer": "khmers",
    "Korean": "Koreans",
    "korean": "koreans",
    "Korea": "Koreans",
    "korea": "koreans",
    "Lithuanian": "Lithuanians",
    "lithuanian": "lithuanians",
    "Lithuania": "Lithuanians",
    "lithuania": "lithuanians",
    "Magyar": "Magyars",
    "magyar": "magyars",
    "Malaysia": "Malay",
    "malaysia": "malay",
    "Malian": "Malians",
    "malian": "malians",
    "Mali": "Malians",
    "mali": "malians",
    "Mayan": "Mayans",
    "mayan": "mayans",
    "Maya": "Mayans",
    "maya": "mayans",
    "Mongol": "Mongols",
    "mongol": "mongols",
    "Mongolia": "Mongols",
    "mongolia": "mongols",
    "Persian": "Persians",
    "persian": "persians",
    "Persia": "Persians",
    "persia": "persians",
    "Pole": "Poles",
    "pole": "poles",
    "Poland": "Poles",
    "poland": "poles",
    "Polish": "Poles",
    "polish": "poles",
    "Portugal": "Portuguese",
    "portugal": "portuguese",
    "Saracen": "Saracens",
    "saracen": "saracens",
    "Sicilian": "Sicilians",
    "sicilian": "sicilians",
    "Sicily": "Sicilians",
    "sicily": "sicilians",
    "Slav": "Slavs",
    "slav": "slavs",
    "Slavic": "Slavs",
    "slavic": "slavs",
    "Spanish": "Spanish",
    "spanish": "spanish",
    "Spain": "Spanish",
    "spain": "spanish",
    "Spainard": "Spanish",
    "spainard": "spanish",
    "Tatar": "Tatars",
    "tatar": "tatars",
    "Teuton": "Teutons",
    "teuton": "teutons",
    "Turk": "Turks",
    "turk": "turks",
    "Turkey": "Turks",
    "turkey": "turks",
    "Turkish": "Turks",
    "turkish": "turks",
    "Vietnam": "Vietnamese",
    "vietnam": "vietnamese",
    "Viking": "Vikings",
    "viking": "vikings",
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
    entities_list = ['(' + helpers.firstLetterHelper(re.sub("\(|\)", "", e)) + ')' for e in list(id_description_map.values())[0:426]]
    entities_string = "|".join(entities_list)
    self.weak_entities_match = entities_string
    temp_synonyms_string = ['(' + k + ')' for k in self.synonyms.keys()]
    temp_civ_synonyms_string = ['(' + ck + ')' for ck in self.civ_synonyms.keys()]
    
    self.civ_name_match = f'{"|".join(temp_civ_synonyms_string)}|{"|".join(self.civ_names)}'
    self.entities_match = f'{"|".join(temp_synonyms_string)}|{self.civ_name_match}|{entities_string}'


    self.cost_matches = list(map(re.compile, [
      f'(H|h)ow much do(es)? (the )?(?P<subject>{self.entities_match}) ((upgrade|tech(nology)?) )?cost',
      f'((W|w)hat do(es)? )?((T|t)he )?(?P<subject>{self.entities_match}) ((upgrade|tech(nology)?) )?cost',
      f'((W|w)hat is )?((T|t)he )?((C|c)ost|(P|p)rice) (of )?(?P<subject>{self.entities_match})',
    ]))

    self.civ_posession_matches = list(map(re.compile, [
      f'((D|d)o(es)? )?((T|t)he )?(?P<civilization_name>{self.civ_name_match}) (get(s)?|have|has) (the )?(?P<subject>{self.entities_match})( (upgrade|tech(nology)?))?',
    ]))

    self.info_matches = list(map(re.compile, [
      f'(W|w)hat (does )?(the )?(?P<subject>{self.entities_match}) ((upgrade|tech(nology)?) )?do',
      f'(T|t)ell me about (?P<subject>{self.entities_match})( (upgrade|tech(nology)?))?',
      f'(E|e)xplain (the )?(?P<subject>{self.entities_match})( (upgrade|tech(nology)?))?',
      f'^(?P<subject>{self.entities_match})$'
    ]))
    self.unique_tech_match = list(map(re.compile, [
      f'((W|w)hat (is|are) )?((T|t)he )?(?P<civilization_name>{self.civ_name_match})((\')?s)? ((?P<age>(C|c)astle|(I|i)mperial) (age )?)?(unique tech((nologie|nology)?)|UT|ut)s?',
    ]))

    self.unique_unit_match = list(map(re.compile, [
      f'((W|w)hat (is|are) )?((T|t)he )?(?P<civilization_name>{self.civ_name_match})((\')?s)? (unique unit|UU|uu)s?',
    ]))

    self.entity_possession_match = list(map(re.compile, [
      f'(((W|w)h(at|ich) )?((is|are) )?)?((T|t)he )?(C|c)iv(ilization)?s? ((that )?(get|have)|with) (the )?(?P<subject>{self.entities_match})( (upgrade|tech(nology)?))?',
    ]))
  # TODO logical operators of civs that get X but not Y, AND Y, OR Y
  # TODO This vs. that only if they are not techs
  # TODO what is the name of civ UT/UU
  # TODO These questions:
  
  # What is the pikemen’s attack bonus versus camels?

  # How much anti cavalry damage do Byzantine cataphracts resist?

  # What is the movement speed of a capped ram with drill?

  # What’s the hitpoints of a Viking man-at-arms in Castle Age?

  # Do hand cannoneers benefit from ballistics?

  # How many petards does it take to destroy a castle?

  # How many +2 crossbows does it take to kill a +2 knight with bloodlines in one shot?

  # Did Spirit of the Law make a video on [x topic]?

  # Has T-West done a pacifist run on [x scenario] yet?

  # Can 25 knights beat 25 Teutonic knights?

  # Does 40 archers trade well against 20 skirmishers?

  def getMatchEntity(self, match):
    subject = match.group('subject')
    real_entity_name = self.synonyms.get(subject)
    if (not real_entity_name):
      real_entity_name = self.civ_synonyms.get(subject, subject)
    return real_entity_name.lower()
  
  def getMatchCiv(self, match):
    civ = match.group('civilization_name')
    real_civ_name = self.civ_synonyms.get(civ, civ).lower()
    return real_civ_name
  
  def extract_entities_possession(self, match):
    return (self.getMatchEntity(match), self.getMatchCiv(match))

  def extract_age(self, match):
    return match.group('age')
  
  def parseQuestionWithMatches(self, question:str, matches):
    for pattern in matches:
      m = pattern.search(question)
      if (m):
        return m
    return None

  def parseQuestion(self, question:str):
    cleaned_question = re.sub("\?|\.|\\n", "", question).strip(" ")
    match_result = None
    try:
      match_result = self.parseQuestionWithMatches(cleaned_question, self.civ_posession_matches)
      if match_result:
        logging.info({"intent": QUESTION_TYPES["POSSESSION"], "cleaned_query": cleaned_question})
        return (self.extract_entities_possession(match_result), QUESTION_TYPES["POSSESSION"])
      
      match_result = self.parseQuestionWithMatches(cleaned_question, self.cost_matches)
      if (match_result):
        logging.info({"intent": QUESTION_TYPES["COST"], "cleaned_query": cleaned_question})
        return (self.getMatchEntity(match_result), QUESTION_TYPES["COST"])
      
      match_result = self.parseQuestionWithMatches(cleaned_question, self.info_matches)
      if (match_result):
        logging.info({"intent": QUESTION_TYPES["INFO"], "cleaned_query": cleaned_question})
        return (self.getMatchEntity(match_result), QUESTION_TYPES["INFO"])
      
      match_result = self.parseQuestionWithMatches(cleaned_question, self.unique_unit_match)
      if (match_result):
        logging.info({"intent": QUESTION_TYPES["UNIQUE_UNIT"], "cleaned_query": cleaned_question})
        return (self.getMatchCiv(match_result), QUESTION_TYPES["UNIQUE_UNIT"])
      
      match_result = self.parseQuestionWithMatches(cleaned_question, self.unique_tech_match)
      if (match_result):
        logging.info({"intent": QUESTION_TYPES["UNIQUE_TECH"], "cleaned_query": cleaned_question})
        return ((self.getMatchCiv(match_result), self.extract_age(match_result)), QUESTION_TYPES["UNIQUE_TECH"])
      
      match_result = self.parseQuestionWithMatches(cleaned_question, self.entity_possession_match)
      if (match_result):
        logging.info({"intent": QUESTION_TYPES["ENTITY_POSSESSION"], "cleaned_query": cleaned_question})
        return (self.getMatchEntity(match_result), QUESTION_TYPES["ENTITY_POSSESSION"])
      logging.info({"intent": -1, "cleaned_query": cleaned_question, "raw_query": question})
      
      
      return None
    except Exception as e:
      logging.error(f'error matching query \"{question}\" with error: {e}')
      return None

  # Return a list of all identifiable AOE entity strings from a given string
  def extractEntities(self, s):
    m = re.findall(self.weak_entities_match, s)
    es = [list(filter(lambda en : len(en) > 1, list(ms))) for ms in m]
    flat = [helpers.toTitleCase(e) for ls in es for e in ls]
    unique_entities = list(set(flat))
    return unique_entities
