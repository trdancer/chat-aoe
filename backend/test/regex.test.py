import sys

sys.path.append('../')

from regex import AOERegex
from constants import QUESTION_TYPES

questions = [
  {
    "question": "The quick brown fox jumps over the lazy dog",
    "expected": None,
  },
  { 
    "question": "Do britons get bloodlines?",
    "expected": (('bloodlines', 'britons'), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do britons get bloodlines",
    "expected": (('bloodlines', 'britons',), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do Britons get bloodlines",
    "expected": (('bloodlines', 'Britons',), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do britons get Bloodlines",
    "expected": (('bloodlines', 'britons',), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do Britons get Bloodlines",
    "expected": (('bloodlines', 'Britons',), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "do Britons get Bloodlines",
    "expected": (('bloodlines', 'Britons',), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "do Britons get Bloodlines  ",
    "expected": (('bloodlines', 'Britons',), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Britons get Bloodlines",
    "expected": (('bloodlines', 'Britons',), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Britons have Bloodlines",
    "expected": (('bloodlines', 'Britons',), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do Britons have Bloodlines",
    "expected": (('bloodlines', 'Britons',), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "",
    "expected": None
  }, 
  { 
    "question": "Do Britins get Bloodlines",
    "expected": None
  }, 
  { 
    "question": "Do Britons get Broodlines",
    "expected": None
  }, 
  { 
    "question": "Does Hindustanis have Ring Archer Armor?",
    "expected": (('ring archer armor', 'Hindustanis'), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Does Hindustanis get Ring Archer Armor?",
    "expected": (('ring archer armor', 'Hindustanis'), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do Hindustanis have Ring archer Armor",
    "expected": (('ring archer armor', 'Hindustanis'), QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Does Hindustanis have Rink archer Armor",
    "expected": None
  },
  { 
    "question": "How much does hoardings cost?",
    "expected": ('hoardings', QUESTION_TYPES["COST"])
  }, 
  { 
    "question": "How much does hoardings coast?",
    "expected": None
  }, 
  { 
    "question": "How much does hoardings cost",
    "expected": ('hoardings', QUESTION_TYPES["COST"])
  }, 
  { 
    "question": "How much does hoardings coast",
    "expected": None,
  }, 
  { 
    "question": "",
    "expected": None
  }, 
  { 
    "question": "What does hoardings cost",
    "expected": ('hoardings', QUESTION_TYPES["COST"])
  },
  { 
    "question": "What does Hoardings cost",
    "expected": ('hoardings', QUESTION_TYPES["COST"])
  },
  { 
    "question": "What does hoardings coast",
    "expected": None
  },
  { 
    "question": "What does hoardings cost?",
    "expected": ('hoardings', QUESTION_TYPES["COST"])
  },
  { 
    "question": "What does hoardings coast?",
    "expected": None
  },
  {
    "question": "hoardings cost?",
    "expected": ('hoardings', QUESTION_TYPES["COST"])
  },
  {
    "question": "hoardings coast",
    "expected": None
  },
  {
    "question": "How much does Ring Archer Armor cost?",
    "expected": ('ring archer armor', QUESTION_TYPES["COST"])
  },
  {
    "question": "How much does Elite Karambit Warrior cost?",
    "expected": ('elite karambit warrior', QUESTION_TYPES["COST"])
  },
  {
    "question": "What is the cost of Elite Karambit Warrior?",
    "expected": ('elite karambit warrior', QUESTION_TYPES["COST"])
  },
  {
    "question": "Cost of Elite Karambit Warrior.",
    "expected": ('elite karambit warrior', QUESTION_TYPES["COST"])
  },
  {
    "question": "Cost Ring Archer Armor.",
    "expected": ('ring archer armor', QUESTION_TYPES["COST"])
  },
  {
    "question": "What does Ring Archer Armor do",
    "expected": ('ring archer armor', QUESTION_TYPES["INFO"])
  },
  {
    "question": "What does Ring Archer Armor do?",
    "expected": ('ring archer armor', QUESTION_TYPES["INFO"])
  },
  {
    "question": "what does Ring Archer Armor do?",
    "expected": ('ring archer armor', QUESTION_TYPES["INFO"])
  },
  {
    "question": "what Ring Archer Armor do?",
    "expected": ('ring archer armor', QUESTION_TYPES["INFO"])
  },
  {
    "question": "tell me about Ring Archer Armor",
    "expected": ('ring archer armor', QUESTION_TYPES["INFO"])
  },
  {
    "question": "tell me about Ring Archer Armor",
    "expected": ('ring archer armor', QUESTION_TYPES["INFO"])
  },
  {
    "question": "tell me about Ring Archer Armor.",
    "expected": ('ring archer armor', QUESTION_TYPES["INFO"])
  },
  {
    "question": "Ring Archer Armor.",
    "expected": ('ring archer armor', QUESTION_TYPES["INFO"]), 
  },
  {
    "question": "What does bloodlines do?",
    "expected": ('bloodlines', QUESTION_TYPES["INFO"])
  },
  {
    "question": "Explain bloodlines",
    "expected": ('bloodlines', QUESTION_TYPES["INFO"])
  },
  {
    "question": "Explain Byzantines",
    "expected": ('byzantines', QUESTION_TYPES["INFO"])
  },
  {
    "question": "explain Elite Karambit Warrior",
    "expected": ('elite karambit warrior', QUESTION_TYPES["INFO"])
  },
  {
    "question": "What are Malay's unique technologies",
    "expected": (('Malay', None), QUESTION_TYPES["UNIQUE_TECH"])
  },
  {
    "question": "What are malay's unique technologies",
    "expected": (('malay', None), QUESTION_TYPES["UNIQUE_TECH"])
  },
  {
    "question": "What are Malay unique technologies",
    "expected": (('Malay', None), QUESTION_TYPES["UNIQUE_TECH"])
  },
  {
    "question": "Malay unique technologies",
    "expected": (('Malay', None), QUESTION_TYPES["UNIQUE_TECH"])
  },
  {
    "question": "Malay unique techs",
    "expected": (('Malay', None), QUESTION_TYPES["UNIQUE_TECH"])
  },
  {
    "question": "What are Malay castle age unique technologies",
    "expected": (('Malay', 'castle'), QUESTION_TYPES["UNIQUE_TECH"])
  },
  {
    "question": "What are Malay castle unique technologies",
    "expected": (('Malay', 'castle'), QUESTION_TYPES["UNIQUE_TECH"])
  },
  {
    "question": "What are Malay imperial age unique technologies",
    "expected": (('Malay', 'imperial'), QUESTION_TYPES["UNIQUE_TECH"])
  },
  {
    "question": "What is Malay's imperial unique technology",
    "expected": (('Malay', 'imperial'), QUESTION_TYPES["UNIQUE_TECH"])
  },
  {
    "question": "What is Malay's imperial UT",
    "expected": (('Malay', 'imperial'), QUESTION_TYPES["UNIQUE_TECH"])
  },
  {
    "question": "What is Celts unique unit",
    "expected": ('Celts', QUESTION_TYPES["UNIQUE_UNIT"])
  },
  {
    "question": "What are Celts unique unit",
    "expected": ('Celts', QUESTION_TYPES["UNIQUE_UNIT"])
  },
  {
    "question": "What is Celts UU",
    "expected": ('Celts', QUESTION_TYPES["UNIQUE_UNIT"])
  },
  {
    "question": "What is Bohemians's uu",
    "expected": ('Bohemians', QUESTION_TYPES["UNIQUE_UNIT"])
  },
  {
    "question": "What civilizations get bloodlines",
    "expected": ('bloodlines', QUESTION_TYPES["ENTITY_POSSESSION"])
  },
  {
    "question": "Which civilizations get bloodlines",
    "expected": ('bloodlines', QUESTION_TYPES["ENTITY_POSSESSION"])
  },
  {
    "question": "Which civilizations have bloodlines",
    "expected": ('bloodlines', QUESTION_TYPES["ENTITY_POSSESSION"])
  },
  {
    "question": "What civilizations have bloodlines",
    "expected": ('bloodlines', QUESTION_TYPES["ENTITY_POSSESSION"])
  },
  {
    "question": "What are the civilizations that have bloodlines",
    "expected": ('bloodlines', QUESTION_TYPES["ENTITY_POSSESSION"])
  },
  {
    "question": "What are the civilizations that get bloodlines",
    "expected": ('bloodlines', QUESTION_TYPES["ENTITY_POSSESSION"])
  },
  {
    "question": "What are civilizations that get bloodlines",
    "expected": ('bloodlines', QUESTION_TYPES["ENTITY_POSSESSION"])
  },
  {
    "question": "What are civilizations with bloodlines",
    "expected": ('bloodlines', QUESTION_TYPES["ENTITY_POSSESSION"])
  },
]

def main():
  aoeRegex = AOERegex("../data/strings.json")
  fails = 0
  for i, q in enumerate(questions):
    result = aoeRegex.parseQuestion(q["question"])
    if (not result == q["expected"]):
      fails += 1
      print(f'Test {i} Failed')
      print(f'Expected {q["expected"]} but got "{result}"')
      print("Question:", q["question"])
      print()
      break
    # print(f'NO MATCH on "{test_set["question"]}"')
    # else:
      # print('Test passed')
  print("Failures:", fails)

main()