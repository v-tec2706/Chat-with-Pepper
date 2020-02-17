from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from configuration import Configuration
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter

class UniversityAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.sentence_filter = SentenceFilter()

    def can_process(self, statement):
        return True

    def process(self, statement, additional_responses_parameters):
        tags = self.create_tags(statement)
        docs_main_collection = self.db.get_docs_from_collection_by_tags_list(Configuration.MAIN_COLLECTION.value, tags)
        docs_phrases_collection = self.db.get_docs_from_collection_by_tags_list(Configuration.PHRASES_COLLECTION.value, tags)
        result_main_collection = ('', 0.0)
        result_phrases_collection = ('', 0.0)
        if len(docs_main_collection) > 0:
            result_main_collection = self.find_best_tags_coverage(docs_main_collection, tags)
        if len(docs_phrases_collection) > 0:
            result_phrases_collection = self.find_best_tags_coverage(docs_phrases_collection, tags)
        return self.prepare_correct_answer(result_main_collection, result_phrases_collection)

    def create_tags(self, statement):
        tags = list(self.sentence_filter.extract_complex_lemmas_and_filter_stopwords(statement.text))
        single_tags, complex_tags = self.sentence_filter.split_to_single_and_complex_lemmas(tags)
        if len(complex_tags) != 0:
            tags = self.create_combinated_tags_list(single_tags, complex_tags)
        return tags

    def create_combinated_tags_list(self, single_tag, complex_tag):
        single_tags_from_complex_tags = self.sentence_filter.generate_single_lemmas_list(complex_tag)
        tags_list = []
        tags_list.extend(single_tag)
        tags_list.extend(complex_tag)
        tags_list.extend(single_tags_from_complex_tags)
        return tags_list

    def find_best_tags_coverage(self, documents, tags):
        id_of_best_cov_doc = -1
        max_conf_from_covered_docs = 0.0
        should_accept_first = True
        for document in documents:
            tags_from_document = document['tags']
            coverage = statement_utils.complex_intersection(set(tags), set(tags_from_document))
            confidence, was_accepted = self.is_accepted(coverage, len(set(tags_from_document)), tags)
            if (was_accepted and confidence >= max_conf_from_covered_docs) or should_accept_first:
                id_of_best_cov_doc = document['_id']
                max_conf_from_covered_docs = confidence
                should_accept_first = False
            self.db.add_new_doc_to_collection(Configuration.RESPONSES_COLLECTION.value,
                                          confidence=confidence,
                                          response=document['text'])
        result_list = list(filter(lambda obj: obj['_id'] == id_of_best_cov_doc, documents))
        if len(result_list) > 0:
            return (result_list[0]['text'], max_conf_from_covered_docs)
        else:
            return (None, 0.0)

    def is_accepted(self, coverage, doc_tags_length, tags):
        confidence = (coverage / len(tags))
        if confidence > 0:
            confidence -= (1 / len(tags)) * (doc_tags_length / (doc_tags_length + 1))
        if confidence >= Configuration.GOOD_ANSWER_CONFIDENCE.value:
            return confidence, True
        else:
            return (confidence, False)

    def prepare_correct_answer(self, result_main_collection, result_phrases_collection):
        result_document_main_collection = result_main_collection[0]
        confidence_main_collection = float(result_main_collection[1])
        result_document_phrases_collection = result_phrases_collection[0]
        confidence_phrases_collection = float(result_phrases_collection[1])
        if confidence_main_collection >= Configuration.GOOD_ANSWER_CONFIDENCE.value \
                or confidence_phrases_collection >= Configuration.GOOD_ANSWER_CONFIDENCE.value:
            if confidence_main_collection >= confidence_phrases_collection:
                res = Statement(
                    statement_utils.prepare_shortened_statement(result_document_main_collection))
                res.confidence = confidence_main_collection
                return res
            else:
                res = Statement(
                    statement_utils.prepare_shortened_statement(result_document_phrases_collection))
                res.confidence = confidence_phrases_collection
                return res
        return statement_utils.default_response()
