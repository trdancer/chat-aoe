from copy import deepcopy
import pprint
from typing import Any, List

from constants.aoe_constants import ENTITY_ATTRIBUTE_VALUES, LANGUAGE_PART_VALUES


QUESTION_TYPES = {
  "ENTITY_COST": "ENTITY_COST",
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
  QUESTION_TYPES["ENTITY_COST"]: {
      "patterns": [
          # How much does (the) XXX (upgrade) cost
          f'how much do(es)? (the )?(?P<subject>{ENTITY_PLACEHOLDER}) ((upgrade|tech(nology)?) )?cost',
          # (What does) the XXX (tech) cost
          f'(what do(es)? )?(the )?(?P<subject>{ENTITY_PLACEHOLDER}) ((upgrade|tech(nology)?) )?cost',
          # What is the price of XXX (tech)
          f'(what is )?(the )?(cost|price) (of )?(the )?(?P<subject>{ENTITY_PLACEHOLDER})( upgrade|tech(nology)?)?',
      ],
      "value": QUESTION_TYPES["ENTITY_COST"]
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


ENTITY_COST_PATTERNS = [
  {
    "value": QUESTION_TYPES['ENTITY_COST'],
    "pattern": [
      {
          "token": "how",
          "required": True,
      },
      {
          "token": "much",
          "required": True,
      },
      {
          "token": "does",
          "required": True,
      },
      {
          "token": "the",
          "required": False,
      },
      {
          "token": LANGUAGE_PART_VALUES['ENTITY'],
          "required": True,
      },
      {
          "token": LANGUAGE_PART_VALUES['ENTITY_TYPE_SPECIFIER'],
          "required": False,
      },
      {
          "token": LANGUAGE_PART_VALUES['ENTITY_ATTRIBUTE'],
          "allowedTokenValues": [ENTITY_ATTRIBUTE_VALUES['COST']],
          "required": True,
      },
    ],
  },
  {
      "value": QUESTION_TYPES["ENTITY_COST"],
      "pattern": [
          {
              "token": "what",
              "required": True,
          },
          {
              "token": "does",
              "required": True,
          },
          {
              "token": "the",
              "required": False,
          },
          {
              "token": LANGUAGE_PART_VALUES['ENTITY'],
              "required": True,
          },
          {
              "token": LANGUAGE_PART_VALUES['ENTITY_TYPE_SPECIFIER'],
              "required": False,
          },
          {
              "token": LANGUAGE_PART_VALUES['ENTITY_ATTRIBUTE'],
              "allowedTokenValues": [ENTITY_ATTRIBUTE_VALUES['COST']],
              "required": True,
          },
      ],
  },
]

QUESTIONS = ENTITY_COST_PATTERNS
def makeQuestionDict():
    qd : dict[str, List[dict[str, Any]]]= {}
    for question in QUESTIONS:
        pattern = question['pattern']
        curToken = { "required": False, "token": "" }
        i = 0
        while not curToken['required'] and i < len(pattern):
            curToken = pattern[i]
            key = curToken['token']
            elements = qd.get(key, [])
            entry = deepcopy(curToken)
            entry['question'] = question
            elements.append(entry)
            qd[key] = elements
            i = i + 1
        if i == len(pattern) or curToken['token'] == '':
            continue
        else:
            curToken = pattern[i]
            key = curToken['token']
            elements = qd.get(key, [])
            entry = deepcopy(curToken)
            entry['question'] = question
            elements.append(entry)
            qd[key] = elements
    return qd
     
QUESTION_DICT = makeQuestionDict()

"""
# ENTITY_COST
# How much does (the) [ENTITY] [ENTITY_TYPE_SPECIFIER] [ENTITY_ATTRIBUTES.COST]
# (What does) (the) [ENTITY] [ENTITY_TYPE_SPECIFIER] [ENTITY_ATTRIBUTES.COST]

# ENTITY_ATTRIBUTE
# What is the [ENTITY_ATTRIBUTE] of [ENTITY] [ENTITY_TYPE_SPECIFIER]
# How much [ENTITY_ATTRIBUTE] does [ENTITY] have
# [ENTITY_ATTRIBUTE] of [ENTITY]

# CIV_ENTITY_POSSESSION
# Does/do [CIVILIZATION] get/have [ENTITY] [ENTITY_TYPE_SPECIFIER]
# [CIVILZATION], do they get [ENTITY] [ENTITY_TYPE_SPECIFIER]

# ENUMERATE_CIV_POSSESSION_OF_ENTITY
# Which [CIV_KEYWORD] get [ENTITY] [ENTITY_TYPE_SPECIFIER]
# Tell me the [CIV_KEYWORD] that have [ENTITY] [ENTITY_TYPE_SPECIFIER]

# TECHNOLOGY_EFFECT
# What does [ENTITY.TECH] tech do
# What is the effect of [ENTITY.TECH]
# Explain the effect of [ENTITY.TECH]
# How does [ENTITY.TECH] work

# ENTITY_DESCRIPTION
# Tell me about [ENTITY] [ENTITY_TYPE_SPECIFIER]
# Describe [ENTITY] [ENTITY_TYPE_SPECIFIER]
# Info about [ENTITY] [ENTITY_TYPE_SPECIFIER]

# ENUMERATE_TECHNOLOGY_EFFECT_ENTITY
# What upgrades/techs effect [ENTITY.UNIT|ENTITY.BUILDING]
# What effects [ENTITY.UNIT|ENTITY.BUILDING]
# What effects [ENTITY.UNIT|ENTITY.BUILDING]

# YN_TECH_EFFECT_ENTITY
# Do [ENTITY] get effected by [ENTITY.TECH]
# Do [ENTITY] get impacted by [ENTITY.TECH]
# Does [ENTITY.TECH] effect [ENTITY] 
# Does [ENTITY.TECH] apply to [ENTITY] 
# Does [ENTITY.TECH] impact [ENTITY]

# ENUMERATE_ENTITY_BY_TECH
# Which [ENTITY_TYPE_SPECIFIER] get effected by [ENTITY.TECH]
# What gets effected by [ENTITY.TECH]
# What does [ENTITY.TECH] apply to

# CIV_INFO
# Tell me about [CIVILIZATION]
# What/who are the [CIVILIZATION]

# CIV_ATTRIBUTE
# What is the [CIVILIZATION_ATTRIBUTE] of [CIVILIZATION]
# What is [CIVILIZATION]'s [CIVILIZATION_ATTRIBUTE]

# CIV_UNIQUE_ENTITY
# what is [CIVILZATION] [AGE_SPECIFIER] [CIV_ATTRIBUTE.UU|CIV_ATTRIBUTE.UT]
# What are [CIVILIZATION]'s [CIV_SPECIFIER.UU|CIV_ATTRIBUTE.UT]

# CIV_UNIQUE_ENTITY_NAME 
# What is [CIVILIZATION] [AGE_SPECIFIER] [CIV_ATTRIBUTE.UU|CIV_ATTRIBUTE.UT] called?
# What is the name of [CIVILIZATION] [AGE_SPECIFIER] [CIV_ATTRIBUTE.UU|CIV_ATTRIBUTE.UT]?

# CIV_ATTRIBUTE_DESCRIPTION
# What does the [CIVILIZATION] [AGE_SPECIFIER] [CIV_ATTRIBUTE.UT] do
# What is the effect of [CIVILIZATION] [AGE_SPECIFIER] [CIV_ATTRIBUTE.UT]
# What is the impact of [CIVILIZATION] [AGE_SPECIFIER] [CIV_ATTRIBUTE.UT]

# CIV_BONUSES
# What are the [BONUS_SPECIFIER] [CIV_ATTRIBUTE.BONUS] of [CIVILIZATION]
# What [BONUS_SPECIFIER] [CIV_ATTRIBUTE.BONUS] do [CIVILIZATION] get
# Tell me the [BONUS_SPECIFIER] [CIV_ATTRIBUTE.BONUS] of [CIVILIZATION]
# Tell me the [CIVILIZATION] [BONUS_SPECIFIER] [CIV_ATTRIBUTE.BONUS]

# CIV_REGION
# What [CIV_ATTRIBUTE.REGION] are [CIVILIZATION] from
# What is the [CIV_ATTRIBUTE.REGION] of [CIVILIZATION]
# From what [CIV_SPECIFER.REGION] are [CIVILIZATION]

# CIV_ARCHITECTURE_INFO
# What is the [CIV_ATTRIBUTE.ARCH] of [CIVILIZATION]
# What [CIV_ATTRIBUTE.ARCH] does [CIVILIZATION] have

# CIV_DESCRIPTION_INFO
# What type of [CIVILIZATION_KEYWORD] is [CIVILIZATION]
# What is the focus of [CIVILIZATION]
# Focus of [CIVILIZATION]

# CIV_DLC_INFO
# What [CIV_ATTRIBUTE.EXPANSION] is [CIVILIZATION] part of
# [CIVILIZATION] is part of what [CIVILIZATION_ATTRIBUTE.EXPANSION]

# CIV_RELEASE_DATE
# What year did [CIVILIZATION] get released
# When did [CIVILIZATION] come out


"""