from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from src.common_utils.language_utils.statement_utils import default_response, contains_synonym, UNIV_SYNONYMS
import src.popular_chatbot.choice_algorithm as choice_algorithm
from configuration import Configuration as config

class PopularQuestionsAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.collection_name = config.POPULAR_QUEST_COLLECTION.value
        self.sentence_filter = SentenceFilter()
        self.filtered_words = []
        self.documents_by_tags = []
        self.db_search_words = []

    def can_process(self, statement):
        self.filtered_words = self.sentence_filter.filter_sentence_complex(statement.text)
        if len(self.filtered_words) == 0:
            return False

        self.db_search_words = list(self.filtered_words)
        if contains_synonym(self.db_search_words):
            self.db_search_words.extend(UNIV_SYNONYMS)
            self.db_search_words = list(set(self.db_search_words))

        self.documents_by_tags = self.db.get_docs_from_collection_by_tags_list(self.collection_name, self.db_search_words)
        if len(self.documents_by_tags) == 0:
            return False
        return True

    def process(self, statement, additional_response_selection_parameters=None):
        result_text, max_conf = choice_algorithm.find_best_tags_response(self.documents_by_tags, self.filtered_words)
        if result_text is None:
            return default_response()
        res = Statement(result_text)
        res.confidence = config.POP_QUEST_BOT_CONST_CONF.value if max_conf >= config.POP_QUEST_BOT_CONF_THRESH.value\
                                                               else config.DEFAULT_CONF.value

        self.db.add_new_doc_to_collection(config.RESPONSES_COLLECTION.value,
                                          confidence=res.confidence,
                                          response=res.text)
        return res
