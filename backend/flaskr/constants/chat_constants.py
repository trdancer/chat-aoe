from backend.flaskr.constants.aoe_constants import ENTITY_TYPES


QUESTION_TYPES = {
  "COST": 0,
  "CIV_POSSESSION": 1,
  "INFO": 2,
  "UNIQUE_TECH": 3,
  "UNIQUE_UNIT": 4,
  "ENTITY_POSSESSION": 5,
}

ENTITY_CATEGORIES = {
  "CIVILIZATION": "civilizations",
  "UNIT": "units",
  "TECH": "techs",
  "BUILDING": "buildings",
}


DEFAULT_RESPONSE = {
  "response": "Sorry, I couldn't answer that question",
  "entity_names": [],
  "civilization_access": [],
  "intent": -1,
  "related_entities": []
}

CHAT_UNSUCCESSFULL_MESSAGES = [
  "Sorry, I couldn't answer that question",
  "Unfortunately, I'm unable to understand.",
  "Not quite sure what you mean, maybe try rephrasing your question",
  "Wololo!",
  "Looks like that's I can't answer that question right now.",
  "Oops, I can't figure out what you mean, maybe try rephrasing your question?"
  "Seems like I can't research that technology right now, maybe if I can advance to the next age I'll be able to!"
]

CHAT_ERROR_MESSAGES = [
  "Oh-oh, something went wrong on my end!",
  "Sorry, look like I didn't get my build order right.",
  "I'm still stuck in the Dark Age..."
]

ENTITY_PLACEHOLDER = "__CHAT_AOE_ENTITY__"
CIVILIZATION_PLACEHOLDER = "__CHAT_AOE_CIVILIZATION__"
QUESTION_PATTERNS = {
  QUESTION_TYPES["COST"]: {
      "patterns": [
          # How much does (the) XXX (upgrade) cost
          f'how much do(es)? (the )?(?P<subject>{ENTITY_PLACEHOLDER}) ((upgrade|tech(nology)?) )?cost',
          # (What does) the XXX (tech) cost
          f'(what do(es)? )?(the )?(?P<subject>{ENTITY_PLACEHOLDER}) ((upgrade|tech(nology)?) )?cost',
          # What is the price of XXX (tech)
          f'(what is )?(the )?(cost|price) (of )?(the )?(?P<subject>{ENTITY_PLACEHOLDER})( upgrade|tech(nology)?)?',
      ],
      "value": QUESTION_TYPES["COST"]
  },
  QUESTION_TYPES['CIV_POSSESSION']: {
      "patterns": [
        # Does XXX get YYY (Upgrade)?
        f'(do(es)? )?(the )?(?P<civilization_name>{CIVILIZATION_PLACEHOLDER}) (get(s)?|have|has) (the )?(?P<subject>{ENTITY_PLACEHOLDER})( (upgrade|tech(nology)?))?',
      ],
      "value": QUESTION_TYPES['CIV_POSSESSION']
  },
  QUESTION_TYPES['ENTITY_POSSESSION']: {
      "patterns": [
          # Which civs get XXX technology?
          f'((wh(at|ich) )?((is|are) )?)?(the )?(C|c)iv(ilization)?s? ((that )?(get|have)|with) (the )?(?P<subject>{ENTITY_PLACEHOLDER})( (upgrade|tech(nology)?))?',
      ],
      "value": QUESTION_TYPES['ENTITY_POSSESSION'],
  },
  QUESTION_TYPES['INFO']: {
      "patterns": [
          # What does XXX tech do?
          f'what (does )?(the )?(?P<subject>{ENTITY_PLACEHOLDER}) ((upgrade|tech(nology)?) )?do',
          # Tell me about XXX technology
          f'tell me about (?P<subject>{ENTITY_PLACEHOLDER})( (upgrade|tech(nology)?))?',
          # Explain the effect of XXX
          f'explain (the )?(effect|affect (of )?)?(?P<subject>{ENTITY_PLACEHOLDER})( (upgrade|tech(nology)?))?',
          # How does XXX work?
          f'how does (?P<subject>{ENTITY_PLACEHOLDER}) (upgrade|tech(nology)) work'
      ],
      "value": QUESTION_TYPES['INFO'],
  },
  QUESTION_TYPES["UNIQUE_TECH"]: {
      "patterns": [
          # what is CIV's castle age unique technology
          # What are CIV's unique technologies
          f'(what (is|are) )?(the )?(?P<civilization_name>{CIVILIZATION_PLACEHOLDER})((\')?s)? ((?P<age>castle|imperial) (age )?)?(unique tech((nologie|nology)?)|ut)s?',
      ],
      "value": QUESTION_TYPES['UNIQUE_TECH'],
  },
  QUESTION_TYPES['UNIQUE_UNIT']: {
      "patterns": [
          # What are CIV's unique units
          f'(what (is|are) )?(the )?(?P<civilization_name>{CIVILIZATION_PLACEHOLDER})((\')?s)? (unique unit|uu)s?',
      ],
      "value": QUESTION_TYPES['UNIQUE_UNIT'],
  },
}


"""
How much does (the) [UNIT|TECHNOLOGY|UPGRADE|BUILDING] [SPECIFIER]? cost
(What does) the [UNIT|TECHNOLOGY|UPGRADE|BUILDING] [SPECIFIER]? cost
What is the price of [UNIT|TECHNOLOGY|UPGRADE|BUILDING] [SPECIFIER]?

# Does/do [CIV] get/have [UNIT|TECHNOLOGY|UPGRADE|BUILDING] [SPECIFIER]?
# [CIV], do they get [UNIT|TECHNOLOGY|UPGRADE|BUILDING] [SPECIFIER]?

# Which civs/civilizations/nations get [UNIT|TECHNOLOGY|UPGRADE|BUILDING] [SPECIFIER]?
# Tell me the civilizations/civs/nations that have [UNIT|TECHNOLOGY|UPGRADE|BUILDING] [SPECIFIER]?

# What does [TECHNOLOGY] tech do?
# Explain the effect of [TECHNOLOGY]
# How does [TECHNOLOGY] work?

# Tell me about [TECHNOLOGY|UNIT|BUILDING|UPGRADE] [SPECIFIER]

# CIV INFO
# Tell me about [CIV]
# What/who are the [CIV]

# CIV SPECIFIC
# what is [CIV] [AGE_SPECIFIER]? [CIV_SPECIFIER]?
# What are [CIV]'s unique technologies
# What are [CIV]'s unique units
# What is [CIV] [AGE_SPECIFIER] [UT] called?
# What does the [CIV] [AGE_SPECIFIER] [UT] do

"""