import parse
import aoeData
questions = [
  {
    "question": "The quick brown fox jumps over the lazy dog",
    "expected": None,
  },
  { 
    "question": "Do britons get bloodlines?",
    "expected": (('bloodlines', 'britons'), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do britons get bloodlines",
    "expected": (('bloodlines', 'britons',), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do Britons get bloodlines",
    "expected": (('bloodlines', 'Britons',), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do britons get Bloodlines",
    "expected": (('Bloodlines', 'britons',), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do Britons get Bloodlines",
    "expected": (('Bloodlines', 'Britons',), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "do Britons get Bloodlines",
    "expected": (('Bloodlines', 'Britons',), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "do Britons get Bloodlines  ",
    "expected": (('Bloodlines', 'Britons',), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Britons get Bloodlines",
    "expected": (('Bloodlines', 'Britons',), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Britons have Bloodlines",
    "expected": (('Bloodlines', 'Britons',), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do Britons have Bloodlines",
    "expected": (('Bloodlines', 'Britons',), aoeData.QUESTION_TYPES["POSSESSION"])
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
    "expected": (('Ring Archer Armor', 'Hindustanis'), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Does Hindustanis get Ring Archer Armor?",
    "expected": (('Ring Archer Armor', 'Hindustanis'), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Do Hindustanis have Ring archer Armor",
    "expected": (('Ring archer Armor', 'Hindustanis'), aoeData.QUESTION_TYPES["POSSESSION"])
  }, 
  { 
    "question": "Does Hindustanis have Rink archer Armor",
    "expected": None
  },
  { 
    "question": "How much does hoardings cost?",
    "expected": ('hoardings', aoeData.QUESTION_TYPES["COST"])
  }, 
  { 
    "question": "How much does hoardings coast?",
    "expected": None
  }, 
  { 
    "question": "How much does hoardings cost",
    "expected": ('hoardings', aoeData.QUESTION_TYPES["COST"])
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
    "expected": ('hoardings', aoeData.QUESTION_TYPES["COST"])
  },
  { 
    "question": "What does Hoardings cost",
    "expected": ('Hoardings', aoeData.QUESTION_TYPES["COST"])
  },
  { 
    "question": "What does hoardings coast",
    "expected": None
  },
  { 
    "question": "What does hoardings cost?",
    "expected": ('hoardings', aoeData.QUESTION_TYPES["COST"])
  },
  { 
    "question": "What does hoardings coast?",
    "expected": None
  },
  {
    "question": "hoardings cost?",
    "expected": ('hoardings', aoeData.QUESTION_TYPES["COST"])
  },
  {
    "question": "hoardings coast",
    "expected": None
  },
  {
    "question": "How much does Ring Archer Armor cost?",
    "expected": ('Ring Archer Armor', aoeData.QUESTION_TYPES["COST"])
  },
  {
    "question": "How much does Elite Karambit Warrior cost?",
    "expected": ('Elite Karambit Warrior', aoeData.QUESTION_TYPES["COST"])
  },
  {
    "question": "What is the cost of Elite Karambit Warrior?",
    "expected": ('Elite Karambit Warrior', aoeData.QUESTION_TYPES["COST"])
  },
  {
    "question": "Cost of Elite Karambit Warrior.",
    "expected": ('Elite Karambit Warrior', aoeData.QUESTION_TYPES["COST"])
  },
  {
    "question": "Cost Ring Archer Armor.",
    "expected": ('Ring Archer Armor', aoeData.QUESTION_TYPES["COST"])
  },
  {
    "question": "What does Ring Archer Armor do",
    "expected": ('Ring Archer Armor', aoeData.QUESTION_TYPES["INFO"])
  },
  {
    "question": "What does Ring Archer Armor do?",
    "expected": ('Ring Archer Armor', aoeData.QUESTION_TYPES["INFO"])
  },
  {
    "question": "what does Ring Archer Armor do?",
    "expected": ('Ring Archer Armor', aoeData.QUESTION_TYPES["INFO"])
  },
  {
    "question": "what Ring Archer Armor do?",
    "expected": ('Ring Archer Armor', aoeData.QUESTION_TYPES["INFO"])
  },
  {
    "question": "tell me about Ring Archer Armor",
    "expected": ('Ring Archer Armor', aoeData.QUESTION_TYPES["INFO"])
  },
  {
    "question": "tell me about Ring Archer Armor",
    "expected": ('Ring Archer Armor', aoeData.QUESTION_TYPES["INFO"])
  },
  {
    "question": "tell me about Ring Archer Armor.",
    "expected": ('Ring Archer Armor', aoeData.QUESTION_TYPES["INFO"])
  },
  {
    "question": "Ring Archer Armor.",
    "expected": ('Ring Archer Armor', aoeData.QUESTION_TYPES["INFO"]), 
  },
  {
    "question": "What does bloodlines do?",
    "expected": ('bloodlines', aoeData.QUESTION_TYPES["INFO"])
  },
  {
    "question": "Explain bloodlines",
    "expected": ('bloodlines', aoeData.QUESTION_TYPES["INFO"])
  },
  {
    "question": "Explain Byzantines",
    "expected": ('Byzantines', aoeData.QUESTION_TYPES["INFO"])
  },
  {
    "question": "explain Elite Karambit Warrior",
    "expected": ('Elite Karambit Warrior', aoeData.QUESTION_TYPES["INFO"])
  },
]

def main():
  fails = 0
  for i, q in enumerate(questions):
    result = parse.parseQuestion(q["question"])
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