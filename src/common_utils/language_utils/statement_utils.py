import operator
from functools import reduce

from chatterbot.conversation import Statement

DEFAULT_RESPONSE = "Przykro mi, nie znam odpowiedzi"
UNIV_SYNONYMS = ['agh', 'uczelnia', 'akademia']

def prepare_statement(*words):
    response = ""

    if any(type(word) is list for word in words):
        words = reduce(operator.concat, words)
    for word in words:
        response += word
        response += " "
    return filter_unexpected_signs(response)


def filter_unexpected_signs(sentence, signs=None):
    if signs is None:
        unexpected_signs = '[\''
    else:
        unexpected_signs = signs
    return ''.join(c for c in sentence if c not in unexpected_signs)


def split_to_single_words(words_set, words):
    for word in words:
        for y in word.split(' '):
            words_set.add(y)
    return words_set


def prepare_shortened_statement(many_sentence_response, first_index=0, length=1):
    if many_sentence_response is not None:
        while type(many_sentence_response) is list:
            if len(many_sentence_response) < 1:
                return default_response()
            many_sentence_response = many_sentence_response[0]
        splitted_to_sentences = many_sentence_response.split('.')

        if first_index >= len(splitted_to_sentences):
            return None
        elif first_index + length > len(splitted_to_sentences):
            length = len(splitted_to_sentences)
        return prepare_statement(splitted_to_sentences[first_index:first_index + length])
    return default_response()


def default_response():
    return Statement(DEFAULT_RESPONSE)


def complex_intersection(set1, set2, is_from_popular_bot=False):
    matched = 0
    for single_or_complex_tag in set1:
        single_tags = extract_single_tags(single_or_complex_tag)
        for single_tag in single_tags:
            if is_present_in_set(single_tag, set2):
                if is_from_popular_bot:
                    matched += 1
                elif single_tag in UNIV_SYNONYMS:
                    matched += 0.5
                else:
                    matched += 1
                break
    return matched


def extract_single_tags(single_or_complex_tag, separator=':'):
    return single_or_complex_tag.split(separator)



def is_present_in_set(single_tag, set):
    for single_or_complex_tag in set:
        single_tags = extract_single_tags(single_or_complex_tag)
        for tag in single_tags:
            if single_tag == tag:
                return True
            elif single_tag in UNIV_SYNONYMS and tag in UNIV_SYNONYMS:
                return True
    return False


def contains_synonym(words):
    return any(word in words for word in UNIV_SYNONYMS)
