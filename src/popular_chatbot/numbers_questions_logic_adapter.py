from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

from src.common_utils.language_utils.statement_utils import default_response, contains_synonym, UNIV_SYNONYMS
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from src.common_utils.language_utils.statement_utils import default_response
import src.popular_chatbot.choice_algorithm as choice_algorithm
from configuration import Configuration as config

class NumbersQuestionsAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.collection_name = config.NUMBERS_QUEST_COLLECTION.value
        self.sentence_filter = SentenceFilter()

    def can_process(self, statement):
        return self.sentence_filter.is_sentence_about_numbers(statement.text)

    def process(self, statement, additional_response_selection_parameters=None):
        filtered_words = self.sentence_filter.filter_sentence_complex(statement.text)
        if len(filtered_words) == 0:
            return default_response()

        db_search_words = list(filtered_words)
        if contains_synonym(db_search_words):
            db_search_words.extend(UNIV_SYNONYMS)
            db_search_words = list(set(db_search_words))
        documents_by_tags = self.db.get_docs_from_collection_by_tags_list(self.collection_name, db_search_words)

        if len(documents_by_tags) == 0:
            return default_response()
        result_text, max_conf = choice_algorithm.find_best_tags_response(documents_by_tags, filtered_words)
        res = Statement(result_text)
        res.confidence = config.MAX_CONF.value  # 1.0
        self.db.add_new_doc_to_collection(config.RESPONSES_COLLECTION.value,
                                          confidence=res.confidence,
                                          response=res.text)
        return res


