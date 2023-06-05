QUESTION_TYPES = {
  "COST": 0,
  "POSSESSION": 1,
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

API_PREFIX = "api"
API_VERSION = "v1"

DEFAULT_RESPONSE = {
  "response": "Sorry, I couldn't answer that question",
  "entity_names": [],
  "civilization_access": [],
  "intent": -1,
  "related_entities": []
}