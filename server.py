from flask import Flask, request
from chatbot import AOEChatBot

from constants import API_PREFIX

def create_app(string_filename="strings.json", data_filename="data.json"):
   
  app = Flask(__name__)

  aoeChatBot = AOEChatBot(string_filename, data_filename)
  @app.route(f'/{API_PREFIX}/chat', methods=["GET"])
  def chat():
    query = request.args.get("q")
    if not query:
      return {"message": "query parameter is required"}, 400
    return aoeChatBot.answerQuestion(query)

  @app.route(f'/{API_PREFIX}/help')
  def help():
      return "Help"
  
  return app

# if __name__ == "main":
#   create_server()