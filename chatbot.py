from constants import QUESTION_TYPES, ENTITY_CATEGORIES
from regex import AOERegex
from aoeData import AOEData

# TODO Unique techs parsing
# TODO map armor class IDs to strings
class AOEChatBot:
  aoeData = None
  aoeRegex = None
  def __init__(self, string_filename, data_filename):
    self.aoeData = AOEData(string_filename, data_filename)
    self.aoeRegex = AOERegex(string_filename)

  def getParsedQuestionAnswer(self, parsed_question):
    (question, question_type) = parsed_question
    response = ""
    entity_names = []
    intent = question_type
    if question_type == QUESTION_TYPES["COST"]:
      (entity) = question
      entity_info = self.aoeData.getEntityInfoByName(entity)
      response = self.aoeData.getEntityCostString(entity_info)
      entity_names = [entity_info["name"]]
    if question_type == QUESTION_TYPES["INFO"]:
      (entity) = question
      entity_info = self.aoeData.getEntityInfoByName(entity)
      response = self.aoeData.getEntitityInfoString(entity_info)
      entity_names = [entity_info["name"]]
    if question_type == QUESTION_TYPES["POSSESSION"]:
      (entity, civ) = question
      response = self.aoeData.getPosessionInfoString(civ, entity)
      entity_names = [civ, entity]
    if question_type == QUESTION_TYPES["UNIQUE_UNIT"]:
      (civ) = question
      
    if question_type == QUESTION_TYPES["UNIQUE_TECH"]:
      (civ, age) = question
      
    if question_type == QUESTION_TYPES["ENTITY_POSSESSION"]:
      (entity) = question
      response = self.aoeData.getEntityPossessionString(entity)
      entity_names = [entity]
    civs_with_entity = self.aoeData.getCivsWithEntity(entity)
    return {
        "response": response,
        "civilization_access": civs_with_entity,
        "entity_names": entity_names,
        "intent": intent
    }
  
  def answerQuestion(self, question):
    parsedResult = self.aoeRegex.parseQuestion(question)
    if (parsedResult):
      answer = self.getParsedQuestionAnswer(parsedResult)
      if answer["response"]:
        related_entities_from_answer = self.aoeRegex.extractEntities(answer["response"])
        answer["related_entities"] = related_entities_from_answer
      return answer
    response = "Sorry, I don't understand that, please try again."
    return {
      "answer": response,
      "entities": [],
      "civilization_access": [],
      "intent": "UNKNOWN",
      "related_entities": []
    }