from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from src.common_utils.language_utils.statement_utils import default_response
import src.popular_chatbot.choice_algorithm as choice_algorithm
from configuration import Configuration as conf

class PopularQuestionsAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.collection_name = conf.POPULAR_QUEST_COLLECTION.value
        self.sentence_filter = SentenceFilter()

    def can_process(self, statement):
        return True

    def process(self, statement, additional_response_selection_parameters=None):
        filtered_words = self.sentence_filter.filter_sentence(statement.text, ['noun'])
        print("FILTERED WORDS IN POPULAR BOT       = ", filtered_words)
        if len(filtered_words) == 0:
            return default_response()

        documents_by_tags = self.db.get_docs_from_collection_by_tags_list(self.collection_name, filtered_words)

        if len(documents_by_tags) == 0:
            return default_response()
        result_text, max_conf = choice_algorithm.find_best_tags_response(documents_by_tags, filtered_words)
        res = Statement(result_text)
        res.confidence = 0.98 if max_conf >= 0.8 else 0.0
        return res