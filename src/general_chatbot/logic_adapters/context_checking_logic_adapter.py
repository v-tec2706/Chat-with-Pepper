import random

from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from configuration import Configuration
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from src.common_utils.types_of_conversation import TypeOfOperation


class ContextAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.context = kwargs.get('conversation_context')
        self.type_of_request = None

    def can_process(self, statement):
        if self.context.is_name_request_processed and not self.context.is_after_name_response_reaction:
            self.type_of_request = TypeOfOperation.NAME
            return True
        return False

    def process(self, statement, additional_respones_parameters):

        if self.type_of_request == TypeOfOperation.NAME:
            return self.process_name_request(statement)

    def process_name_request(self, statement):

        statement_list = statement.text.split()
        speaker_name = statement_list[len(statement_list) - 1]
        polish_sentence_tokenizer = SentenceFilter()
        if polish_sentence_tokenizer.is_name(speaker_name):
            self.context.speaker_name = speaker_name

        name_conversation_end_responses = list(self.db.filter(conversation='name_response_end'))
        general_conversation_intro = list(self.db.filter(conversation='general_conversation_intro'))

        if len(name_conversation_end_responses) > 0 and len(general_conversation_intro) > 0:
            result = Statement(
                statement_utils.prepare_statement(
                    name_conversation_end_responses[random.randint(0, len(name_conversation_end_responses) - 1)].text,
                    self.context.speaker_name,
                    general_conversation_intro[random.randint(0, len(general_conversation_intro) - 1)].text),
                confidence=0.4,
                in_response_to=TypeOfOperation.CONTEXT_NAME.value)
            self.db.add_new_doc_to_collection(Configuration.RESPONSES_COLLECTION.value,
                                              confidence=result.confidence,
                                              response=result.text)
            return result
        return statement_utils.default_response()
