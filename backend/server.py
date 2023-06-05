from flask import Flask, request
from flask_cors import CORS
from chatbot import AOEChatBot
import re
from constants import API_PREFIX, API_VERSION, DEFAULT_RESPONSE
# import logging


def create_app(string_filename="data/patch_85208_strings.json", data_filename="data/patch_85208.json"):
   
  # logging.basicConfig(filename="logs/queries.log", level=logging.DEBUG)
  app = Flask(__name__)
  CORS(app)

  aoeChatBot = AOEChatBot(string_filename, data_filename)
  
  # Put the spam filter at the API level in case we need it for other endpoints later

  words_file = open('data/naughty-words.txt')
  naughty_words = {re.sub("\n", "", w) for w in words_file.readlines()}
  words_file.close()
  
  @app.route(f'/{API_PREFIX}/{API_VERSION}/chat', methods=["GET"])
  def chat():
    query = str(request.args.get("q"))
    if not query:
      return {"message": "query parameter is required"}, 400
    for token in query.split():
       if token in naughty_words:
          return DEFAULT_RESPONSE
    return aoeChatBot.answerQuestion(query)

  @app.route(f'/{API_PREFIX}/{API_VERSION}/help')
  def help():
      return "Help"
  
  return app

# if __name__ == "main":
#   create_server()