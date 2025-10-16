import random
from flask import Response, current_app, make_response, request, g
from backend.flaskr.routes.chat.chat_service import AOEChatService
from backend.flaskr.utils.array import randElement
from backend.flaskr.constants.chat_constants import CHAT_UNSUCCESSFULL_MESSAGES

def filter_response(query: str) -> int:
    for token in query.split():
        if token in g.naughty_words:
            return -1
    return 0
   
@current_app.route(f'/chat', methods=["POST"])
def chat():
  chatService = AOEChatService()

  body = request.get_json()
  query = str(body.get("query"))
  if not query:
    return {"error": "body parameter 'query' is required"}, 400
  chatResponse = None
  filterResult = filter_response(query)
  if filterResult < 0:
    chatResponse = chatService.build_failed_response()
  else:
    chatResponse = chatService.handleChat(query)
  return make_response(dict(chatResponse))