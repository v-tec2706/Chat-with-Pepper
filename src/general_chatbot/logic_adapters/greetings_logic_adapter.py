from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from configuration import Configuration
from src.common_utils.types_of_conversation import TypeOfOperation


class GreetingAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.context = kwargs.get('conversation_context')

    def can_process(self, statement):
        statement.text = statement.text.lower()
        words = self.db.get_responses_list_by_tags(tag="greeting")
        for w in words:
            if w == statement.text:
                return True
        return False

    def process(self, statement, additional_respones_parameters):

        greetings = self.db.get_random_response_by_tags(tag="greeting")
        greetings_request = self.db.get_random_response_by_tags(tag="greeting_response")
        if greetings_request is not None and greetings is not None:
            result = Statement(
                statement_utils.prepare_statement(
                    greetings,
                    greetings_request),
                in_response_to=TypeOfOperation.GREETING.value)
            result.confidence = 1.0
            self.db.add_new_doc_to_collection(Configuration.RESPONSES_COLLECTION.value,
                                              confidence=result.confidence,
                                              response=result.text)
            return result
        return statement_utils.default_response()
