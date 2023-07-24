from flask import Flask, request
from flask_cors import CORS
from chatbot import AOEChatBot
import re
from constants import API_PREFIX, API_VERSION, DEFAULT_RESPONSE
# import logging


def create_app(string_filename="data/patch_85208_strings.json", data_filename="data/patch_85208.json", armor_datafilename="data/armor.json"):
  # TODO wrap app in WSGI server like waitress
  # TODO implement API key authentication
  # Prod mode:
  # - Production database
  # - debug level: error
  # - debugging: off
  # - testing: off
  # - secret key: set
  # Dev mode:
  # - dev database
  # - debug level: debug
  # - debugging: on
  # - testing: on

  # logging.basicConfig(filename="logs/queries.log", level=logging.DEBUG)
  app = Flask(__name__)
  CORS(app)

  # In the future data would be attached with a patch version so you could see historical patch info
  aoeChatBot = AOEChatBot(string_filename, data_filename, armor_datafilename)
  
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

  @app.route(f'/{API_PREFIX}/{API_VERSION}/info')
  def info():
      return {
         "patch": "85208",
         "api": "v1"
      }
  
  return app

# if __name__ == "main":
#   create_server()