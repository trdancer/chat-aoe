import pprint
from typing import Any, List
from constants.chat_constants import QUESTION_DICT, QUESTIONS

class ChatClassifierService:

    def __init__(self):
        pass

    def matchQueryTokenToQuestionToken(self, query_token: str, question_element: dict[str, Any], replacement_lookup: dict[str, Any]):
        replacementValue = replacement_lookup.get(query_token)
        matchesToken = query_token == question_element['token']
        if replacementValue is None:
            return matchesToken
        matches_language_part = replacementValue['language_element']['language_part'] == question_element['token']
        matched_token_value = replacementValue['language_element']['value']
        allowedTokenValues: List[str] | None = question_element.get('allowedTokenValues', [matched_token_value])
        isAllowedTokenValue = matched_token_value in allowedTokenValues
        return matches_language_part and isAllowedTokenValue
    
    def matchTokensToQuestionToken(self, query_tokens: List[str], question_element: dict[str, Any], replacement_lookup: dict[str, Any]):
        for parsed_token in query_tokens:
            tokenMatchesQuestionToken = self.matchQueryTokenToQuestionToken(parsed_token, question_element, replacement_lookup)
            if tokenMatchesQuestionToken:
                return True    
        return False
    
    # determines if a given question matches the pattern of a question
    def matchQueryToQuestion(self, parsed_query: List[List[str]], replacement_lookup: dict[str, Any], question_pattern: dict[str, Any]):
        question_index = 0
        i = 0
        pattern = question_pattern['pattern']
        doesMatch = True
        while doesMatch and i < len(parsed_query) and question_index < len(pattern):
            parsed_tokens = parsed_query[i]
            tokensMatchesQuestionToken = False
            question_pattern_element = pattern[question_index]
            # attempt to match the current query token with the current question token
            tokensMatchesQuestionToken = self.matchTokensToQuestionToken(parsed_tokens, question_pattern_element, replacement_lookup)
            print(f'tokens=[{parsed_tokens}] match question_token=[{question_pattern_element['token']}]? {tokensMatchesQuestionToken}')
            #  if match:
            #   consume current query token and current question token
            #   continue to next query and question tokens
            if tokensMatchesQuestionToken:
                doesMatch = doesMatch and True
                question_index = question_index + 1
                i = i + 1
                continue
            #  no match
            #    if question token is required:
            #       halt: no question match
            print(f'no tokens match this question token: {question_pattern_element['token']}')
            if question_pattern_element['required']:
                doesMatch = False
                question_index = question_index + 1
                i = i + 1
                break
            # not required:
                # continue with next question token
                # keep current query token
            question_index = question_index + 1

                #   consume question token and move to next question token
                # require current query token to match current question token

        return doesMatch         
        

    def classifyQuery(self, parsed_query: List[List[str]], replacement_lookup: dict[str, Any]):
        # Get all matching question patterns that could match based on first token
        first_tokens = parsed_query[0]
        matched_questions = []
        for query_token in first_tokens:
            matching_questions = QUESTION_DICT.get(query_token, [])
            # pprint.pprint(matching_questions)
            for question_starting_token in matching_questions:
                question = question_starting_token['question']
                query_matches_pattern = self.matchQueryToQuestion(parsed_query, replacement_lookup, question)
                if query_matches_pattern:
                    matched_questions.append(question)
        return [x['value'] for x in matched_questions]