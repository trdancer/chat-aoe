from flask import Flask, request
from flask_cors import CORS
from chatbot import AOEChatBot

from constants import API_PREFIX, API_VERSION
# import logging


def create_app(string_filename="data/strings.json", data_filename="data/data.json"):
   
  # logging.basicConfig(filename="logs/queries.log", level=logging.DEBUG)
  app = Flask(__name__)
  CORS(app)

  aoeChatBot = AOEChatBot(string_filename, data_filename)
  
  @app.route(f'/{API_PREFIX}/{API_VERSION}/chat', methods=["GET"])
  def chat():
    query = request.args.get("q")
    if not query:
      return {"message": "query parameter is required"}, 400
    return aoeChatBot.answerQuestion(query)

  @app.route(f'/{API_PREFIX}/{API_VERSION}/help')
  def help():
      return "Help"
  
  return app

# if __name__ == "main":
#   create_server()