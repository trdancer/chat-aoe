# Tech tree data fetched from Siege Engineers AOE2 Tech tree project
# September 2022

# import re
# import aoeData
# def main():
#   print("Welcome to the Age of Empires 2 Definitive Edition Tech Tree bot.")
#   print("You can ask me things like:")
#   print("\t- Do the Britons get Bloodlines?")
#   print("\t- Does Hindustanis have Ring Archer Armor?")
#   print("\t- How much does Hoardings cost?")
#   print("Capitalzation and punctuation is not necessary")
#   print("Enter Q or Quit at anytime to exit.")
#   answerQuestion()



# def answerQuestion():
#   userInput = input('Input: ')
#   if (re.match("[qQ](uit)?", userInput)):
#     print('Quitting...')
#     exit(0)
#   parsedResult = parse.parseQuestion(userInput)
#   if (parsedResult):
#     print("I recognize that question")
#     answer = aoeData.getParsedQuestionAnswer(parsedResult)
#     print(answer["answer"])
#     # Process the result
#   else:
#       print("Sorry, I don't understand that, please try again.")
#   answerQuestion()


# if __name__ == "__main__":
#   main()