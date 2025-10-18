from routes.chat.chat_classifier import ChatClassifierService
from routes.chat.chat_parser import ChatParserService
import pprint
parser = ChatParserService()
classifier = ChatClassifierService()

(match_m, ss) = parser.parseString("How much does Albatross cost?")
print(ss)
query_tokens, repl = parser.resolveMatchMatrix(ss,match_m)
pprint.pprint(query_tokens)
# pprint.pprint(repl)
r = classifier.classifyQuery(query_tokens, repl)
print(r)
# pprint.pprint(d)
# pprint.pprint(match_m)