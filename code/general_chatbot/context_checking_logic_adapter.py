import random

from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from chatterbot.storage import SQLStorageAdapter

from code.common_utils.types_of_conversation import TypeOfOperation


class ContextAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = SQLStorageAdapter(database_uri='sqlite:///resources/db.sqlite13')
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
        self.context.speaker_name = speaker_name

        name_response_to_update = statement_list[slice(len(statement_list) - 1)]
        name_response_to_update = ' '.join(name_response_to_update)

        # self.db.create(text=name_response_to_update + ' , a ' + get_proper_pronoun(name_response_to_update),
        #                conversation='name_response')

        name_conversation_end_responses = list(self.db.filter(conversation='name_response_end'))
        general_conversation_intro = list(self.db.filter(conversation='general_conversation_intro'))

        if len(name_conversation_end_responses) > 0 and len(general_conversation_intro) > 0:
            response_text = name_conversation_end_responses[
                                random.randint(0, len(name_conversation_end_responses) - 1)].text + ' '
            response_text += self.context.speaker_name + ' ,'
            response_text += general_conversation_intro[random.randint(0, len(general_conversation_intro) - 1)].text

            selected_statement = Statement(response_text)
            selected_statement.confidence = 0.4
            selected_statement.in_response_to = TypeOfOperation.CONTEXT_NAME.value
            return selected_statement
        return Statement("Nie znam odpowiedzi", 0)