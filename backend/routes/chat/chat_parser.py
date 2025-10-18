from copy import deepcopy
import re
from typing import Dict, List, Set, Tuple, Any
from constants.aoe_constants import LANGUAGE_KEYWORDS, LANGUAGE_DICTIONARY
class ChatParserService():
    def __init__(self):
        pass

    def normalizeString(self, s: str) -> str:
        l = s.lower()
        noSpecialChars = re.sub(r'[.,?!@#$%^&*():"\'<>/+=_\-\\]', '', l)
        noExtraWhiteSpace = re.sub(r'[\t\n]+| {2,}', ' ', noSpecialChars)
        return noExtraWhiteSpace 
    
    def replaceValues(self, query: str):
        normalized_query = self.normalizeString(query)
        """
        {
            "start:end": List[str]
        }
        """
        replacements: Dict[str, List[str]] = {}

        # TODO if the same string or a substring of an existing match
        # matches to 2 or more entities of the same class, 
        # Only match the one with the highest match closeness
        # Example: "Heavy camel" matches to both "camel" and "heavy camel" units/upgrades
        # So it should only match heavy camel
        matches_by_language_part: Dict[str, List[Tuple[re.Match, Dict]]]= {}
        for l in LANGUAGE_KEYWORDS:
            aliases: List[str] = l['aliases']
            pattern = re.compile(f'\\s({"|".join(aliases)})\\s')
            matches_for_type = re.finditer(pattern, normalized_query)
            language_part = l['language_part']
            for m in matches_for_type:
                if m.start() >= 0:
                    existing_matches_for_type = matches_by_language_part.get(language_part, [])
                    existing_matches_for_type.append((m, l))
                    matches_by_language_part[language_part] = existing_matches_for_type
        """
        {
            "[PLACEHOLDER]": {
                original: "original query string",
                language_token: <LANGUAGE_TOKEN>,
            },
        }
        """
        substitutions = {}
        

        # filter out matches that are substring matches of an existing match
        filtered_matches: List[Tuple[re.Match, Any]] = []
        for language_part, matches_for_type in matches_by_language_part.items():
            for m, l in matches_for_type:
                match_start = m.start()
                match_end = m.end()
                is_match_shadowed = False
                for m2, l2 in matches_for_type:
                    if l2['value'] == l['value']:
                        continue
                    match2_start = m2.start()
                    match2_end = m2.end()
                    if match_start >= match2_start and match_end <= match2_end:
                        is_match_shadowed = True
                        break
                        # duplicate/substring match for an entity of the same type
                        # so do not add m to final match set
                if not is_match_shadowed:
                    filtered_matches.append((m, l))
        counters = {}
        
        for match_pair in filtered_matches:
            m, l = match_pair

            orginal_value = m.group()
            language_part = l['language_part']
            counter_value = counters.get(language_part, 0)
            placeholder = f'{language_part}_{counter_value}'
            key = f'{m.start()}:{m.end()}'
            placeholders: List[str] = replacements.get(key, [])
            placeholders.append(placeholder)
            replacements[key] = placeholders
            counters[language_part] = counter_value + 1
            substitutions[placeholder] = {
                "orginal": orginal_value,
                "language_token": l['label']
            }
        pos = 0
        chunks: List[str] = []
        
        def sortKeys(item):
            k, _v = item
            return int(k.split(':')[0])
        
        sorted_items = sorted(list(replacements.items()), key=sortKeys)
        for k, v in sorted_items:
            rep_start, rep_end = [int(v) for v in k.split(':')]
            new_value = f'[{'|'.join(v)}]'
            temp_s = normalized_query[pos:rep_start]
            replaced_string = normalized_query[rep_start:rep_end]
            chunks.append(temp_s)
            chunks.append(new_value)
            pos = rep_end
            # split original string by each start:end value
            # for start:end [6:14, 16:19]
            # "quick brown fox jumps" -> ["quick", "brown fox", "ju", "mps"]
            # assoc 6:14 -> index 1, 16:19 -> index 3
            # replace item at index N with new value
            # Join array 
        end = normalized_query[pos:]
        chunks.append(end)
        final_string = " ".join(chunks)

        return final_string, substitutions

        
    def parseQuestion(self, query: str):
        replaced = self.replaceValues(query)
        # 1. replace all aliases in query with placeholder values into "replacedQuery"
        # How much does arb cost -> How much does [UNIT_0|UPGRADE_0] cost
        # What is the castle age unique tech of the burgundians -> What is the [AGE] [UT] of the [CIVILIZATION_0]
        # Does the Chinese get Heresy -> Does the [CIVILIZATION_0] get [TECHNOLOGY_0]
        # 2. Match replacedQuery string with regex question patterns
        # 3. Replace placeholders with resolved values from aliases
        # 4. 
        return replaced

    def matchLanguageElement(self, query_tokens: List[str], language_element: dict[str, Any]) -> int | None:
        alias: str = language_element['full_alias']
        tokenized_alias = alias.split(' ')
        query_index = 0
        for alias_token in tokenized_alias:
            if query_index >= len(query_tokens):
                return None
            query_token = query_tokens[query_index]
            if query_token == alias_token:
                query_index = query_index + 1
            else:
                break
        if query_index == len(tokenized_alias):
            return query_index
        else:
            return None
    
    def parseLanguageElements(self, idx: int, query_tokens: List[str], language_elements: List[dict[str, Any]], match_matrix: List[List[List]]):
        for language_element in language_elements:
            matchLength = self.matchLanguageElement(query_tokens, language_element)
            if matchLength is None or matchLength == 0:
                continue
            match_start = idx
            match_end = idx + matchLength
            matches_in_range = match_matrix[match_start][match_end - 1]
            keep_match = True
            for match in matches_in_range:
                existing_match_start = match['start']
                existing_match_end = match['end']
                if existing_match_start == match_start and existing_match_end == match_end:

                    break
                    # keep since its a direct overlap
                is_match_subset = (existing_match_start <= match_start and existing_match_end <= match_end) or (existing_match_end >= match_end and existing_match_start >= match_start)
                
                if is_match_subset:
                    keep_match = False
                    break
            if (keep_match):
                # populate match_matrix with this match
                for i in range(match_start, match_end):
                    for j in range(i, match_end):
                        matches_at_index = match_matrix[i][j]
                        match_obj = {
                            "start": match_start,
                            "end": match_end,
                            "language_element": language_element
                        }
                        matches_at_index.append(match_obj)

    def parseString(self, query:str):
        normalized_query = self.normalizeString(query)
        split_query = normalized_query.split(' ')
        i = 0
        match_matrix = [[[] for j in split_query] for i in split_query ]
        while i < len(split_query):
            token = split_query[i]

            maybeAliasStarts = LANGUAGE_DICTIONARY.get(token)
            if maybeAliasStarts is not None:
                remaining_tokens = split_query[i:]
                self.parseLanguageElements(i, remaining_tokens, maybeAliasStarts, match_matrix)

            i = i + 1
        return match_matrix, split_query

    def resolveMatchMatrix(self, query_tokens: List[str], match_matrix: List[List[List]]):
        
        unique_matches_by_position = {}
        replacement_dict = {}
        replacement_tokens = [[] for _ in query_tokens]
        for i in range(len(query_tokens)):
            row = match_matrix[i]
            for position in row:
                for match in position:
                    match_start = match['start']
                    match_end = match['end']
                    match_value = match['language_element']['value']
                    match_part = match['language_element']['language_part']
                    key = f'{match_start}:{match_end}:{match_value}:{match_part}'
                    unique_matches_by_position[key] = match
        for m in unique_matches_by_position.values():
            match_start = m['start']
            match_end = m['end']
            language_element = m['language_element']
            replacement_key = f'{language_element['value']}:{language_element['language_part']}'
            original_tokens = []
            for i in range(match_start, match_end):
                original_tokens.append(query_tokens[i])
                replacement_tokens[i].append(replacement_key)
            original_token = " ".join(original_tokens)
            replacement_dict[replacement_key] = {
                "original_token": original_token, 
                "language_element": language_element,
                "start": match_start,
                "end": match_end
            }

        i = 0
        final_tokens: List[List[str]] = []
        while i < len(query_tokens):
            original_token = query_tokens[i]
            all_consecutive_replacements = set()
            this_replacements = deepcopy(replacement_tokens[i])
            match_end_max = 0
            queue = this_replacements
            seen : Set[str] = set()
            while len(queue) > 0:
                r = queue[0]
                if r not in seen:
                    replacement_value = replacement_dict[r]
                    replacement_start = replacement_value['start']
                    replacement_end = replacement_value['end']
                    seen.add(r)
                    if (replacement_end > match_end_max):
                        match_end_max = replacement_end
                    for k in range(replacement_start + 1, replacement_end):
                        for rr in replacement_tokens[k]:
                            if rr not in seen and rr not in queue:
                                queue.append(rr)
                queue.remove(r)
            for j in range(i, match_end_max):
                reps = replacement_tokens[j]
                for r in reps:
                    all_consecutive_replacements.add(r)
            if len(all_consecutive_replacements) > 0:
                final_tokens.append(list(all_consecutive_replacements))
                i = match_end_max
            else:
                final_tokens.append([original_token])
                i = i + 1
        
        return final_tokens, replacement_dict

"""
language element: an identifier or alias of something like one word 'arbalester'
    multiple 'heavy camel'/'castle age'
for each token:
is known start of a language_element?
    no:
        continue
    yes:
        consume the next token
        is it a valid next part of any language_element?
        no:
            have we consumed every element of this language_element?
            yes:
                match the consumed tokens with this language_element
                continue
            no:
                discard the consumed tokens for this language_element
                continue
        yes:
            consume this token into this language element
            continue to next token
if there are 2 matched language_elements starting or ending at the same token, the match with the greatest number of tokens
should be kept

e.g "castle age" matches AGE.castle_age and BUILDING.castle, 
but the AGE.castle_age consumes both "castle" and "age"
so AGE.castle should be kept and BUILDING.castle should be discarded
HOWEVER "castle" matches AGE.castle_age and BUILDING.castle
but they both consume only "castle" and therefore should both be matched

e.g. "heavy camel" matches UNIT.heavy_camel_rider, UPGRADE.heavy_camel_rider, and UNIT.camel_rider
but UNIT.heavy_camel_rider and UPGRADE.heavy_camel_rider matches both "heavy" and "camel"
so UNIT.heavy_camel_rider and UPGRADE.heavy_camel_rider should be kept
and UNIT.camel_rider should be discarded
both UNIT/UPGRADE.heavy_camel_rider are kept since they match the same tokens
"""