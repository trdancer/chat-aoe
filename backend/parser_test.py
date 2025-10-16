from flaskr.routes.chat.chat_parser import ChatParserService
import pprint
c = ChatParserService()

(match_m, ss) = c.parseString("How much does Heavy Camel archer cost in castle age for the armenians?")
d = c.resolveMatchMatrix(ss,match_m)
# pprint.pprint(d)
# pprint.pprint(match_m)