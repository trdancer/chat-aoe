from backend.flaskr.constants.chat_constants import CHAT_UNSUCCESSFULL_MESSAGES
from backend.flaskr.utils.array import randElement


class ChatResponse:
    def __init__(self, response:str, entity_names=[], civilization_access=[], intent=-1, related_entities=[]):
        self.response = response
        self.entity_names = entity_names
        self.civilization_access = civilization_access
        self.intent = intent
        self.related_entities = related_entities
    
    def __iter__(self):
        yield 'response', self.response,
        yield 'entity_names', self.entity_names
        yield 'civilization_access', self.civilization_access
        yield 'intent', self.intent
        yield 'related_entities', self.related_entities


class AOEChatService:

    def __init__(self):
        pass

    def handleChat(self, query: str) -> ChatResponse:
        return self.build_failed_response()

    def build_failed_response(self) ->ChatResponse:
        message = randElement(CHAT_UNSUCCESSFULL_MESSAGES)
        return ChatResponse(message)