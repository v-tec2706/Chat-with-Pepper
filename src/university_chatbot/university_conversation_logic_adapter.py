from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from src.common_utils.constants import GOOD_ANSWER_CONFIDENCE, RANDOM_CONF_THRESHOLD
import random


class UniversityAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.sentence_filter = SentenceFilter()

    def find_max_coverage(self, documents, tags):
        max_coverage = 0
        for doc in documents:
            tags_from_document = doc['tags']
            coverage = len(set(tags_from_document).intersection(set(tags)))
            max_coverage = max(max_coverage, coverage)
        return max_coverage

    def is_accepted(self, coverage, doc_tags_length, tags, document=None):
        text_coverage = 0.0
        if document is not None:
            text_from_doc = list(document['text'].split('.'))[0]
            filtered_tags_from_text = self.sentence_filter.extract_complex_lemmas_and_filter_stopwords(text_from_doc)
            text_coverage = len(set(filtered_tags_from_text).intersection(set(tags)))
            #print("FILTERED_TAGS_FROM_DOC:", filtered_tags_from_text, 'TEXT_COVERAGE:', text_coverage)
        #print("TEXT_COV:", text_coverage)
        conf_thresh = (coverage / doc_tags_length) * (1 - 1/(3*len(tags))) + 0.1 * text_coverage
        if conf_thresh >= GOOD_ANSWER_CONFIDENCE:
            return conf_thresh, True
        else:
            return (conf_thresh, True) if random.uniform(0, 1) > RANDOM_CONF_THRESHOLD else (0.0, False)


    def find_best_tags_coverage(self, documents, tags_combinations_dict, should_also_search_text):
        id_of_best_cov_doc = -1
        max_coverage = -1
        for tags in tags_combinations_dict.values():
            print("TAG:", tags)
            max_coverage = max(max_coverage, self.find_max_coverage(documents, tags))
        max_conf_from_covered_docs = 0
        was_one_selected = False
        for tags in tags_combinations_dict.values():
            for document in documents:
                tags_from_document = document['tags']
                coverage = len(set(tags_from_document).intersection(set(tags)))
                if max_coverage == coverage:
                    conf_thresh, was_accepted = self.is_accepted(coverage, len(set(tags_from_document)), tags, document) if should_also_search_text \
                                                else self.is_accepted(coverage, len(set(tags_from_document)), tags)
                    if not was_one_selected:
                        max_conf_from_covered_docs = conf_thresh
                        id_of_best_cov_doc = document['_id']
                        was_one_selected = True

                    if was_accepted and conf_thresh >= max_conf_from_covered_docs:
                        id_of_best_cov_doc = document['_id']
                        max_conf_from_covered_docs = conf_thresh
                        print("Max_coverage: tags:", tags_from_document, ", len:", coverage, ", max_conf:", max_conf_from_covered_docs, ", tags:", tags)

        result_list = list(filter(lambda obj: obj['_id'] == id_of_best_cov_doc, documents))
        if len(result_list) > 0:
            return result_list[0]['text'], max_conf_from_covered_docs
        else:
            return None

    def create_tags_combinations_dict(self, normal_lemmas, complex_lemmas):
        tags_combinations = {}
        lemmas_chosen_from_complex_list = self.sentence_filter.generate_filtered_words_lemmas_combinations(complex_lemmas)  # list(map(lambda lemma: lemma.split(':')[0], complex_lemmas))
        for l in lemmas_chosen_from_complex_list:
            n_lemmas_copy = list(normal_lemmas)
            n_lemmas_copy.extend(lemmas_chosen_from_complex_list[l])
            tags_combinations[l] = n_lemmas_copy

        return tags_combinations

    def can_process(self, statement):
        return True

    def delete_additional_info_after_colon(self, word):
        index = word.find(':')
        if index == -1:
            return word
        return word[:index]

    def set_to_str_with_colons(self, set):
        string = ''
        for elem in set:
            string += elem + ':'
        string = string[:-1]
        return string

    def process(self, statement, additional_responses_parameters):
        noun_tags = self.sentence_filter.extract_complex_lemmas_and_filter_stopwords(statement.text)
        noun_tags = list(noun_tags)
        print("TAGS FROM SENTENCE FILTER = ", noun_tags)
        normal_lemmas, complex_lemmas = self.sentence_filter.split_to_norm_and_complex_lemmas(noun_tags)
        print("COMPLEX LEMMAS = ", complex_lemmas)
        docs_by_tags = []
        docs_by_lemmas = []
        tags_combinations_dict = {}
        if len(complex_lemmas) != 0:
            tags_combinations_dict.update(self.create_tags_combinations_dict(normal_lemmas, complex_lemmas))
            for tags in tags_combinations_dict.values():
                tag_docs = self.db.get_docs_from_collection_by_tags_list('MAIN_COLLECTION', tags)
                lemma_docs = self.db.get_docs_from_collection_by_tags_list('PHRASES', tags)
                if tag_docs: docs_by_tags.extend(tag_docs)
                if lemma_docs: docs_by_lemmas.extend(lemma_docs)
        else:
            tags_combinations_dict[0] = noun_tags
            tag_docs = self.db.get_docs_from_collection_by_tags_list('MAIN_COLLECTION', noun_tags)
            lemma_docs = self.db.get_docs_from_collection_by_tags_list('PHRASES', noun_tags)
            if tag_docs: docs_by_tags.extend(tag_docs)
            if lemma_docs: docs_by_lemmas.extend(lemma_docs)

        confidence_by_tags = -1
        confidence_by_phrases = -1
        if len(docs_by_tags) > 0:  # matching tags exist
            result_document_tags, confidence_by_tags = self.find_best_tags_coverage(docs_by_tags, tags_combinations_dict, True)
        print("Extracted_lemmas:", noun_tags)
        #docs_by_lemmas = self.db.get_docs_from_collection_by_tags_list('PHRASES', noun_tags)
        if len(docs_by_lemmas) > 0:
            print("SEARCHING IN PHRASES STARTED")
            result_document_lemmas, confidence_by_lemmas = self.find_best_tags_coverage(docs_by_lemmas, tags_combinations_dict, False)
        if confidence_by_lemmas + confidence_by_tags > -2:
            if confidence_by_tags >= confidence_by_lemmas:
                res = Statement(
                    statement_utils.prepare_shortened_statement(result_document_tags))
                res.confidence = 1.0
                return res
            else:
                res = Statement(
                    statement_utils.prepare_shortened_statement(result_document_lemmas))
                res.confidence = 1.0
                return res
        else:
            return statement_utils.default_response()

