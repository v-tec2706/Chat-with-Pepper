from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from configuration import Configuration as configuration
from src.common_utils.types_of_conversation import TypeOfOperation


class BasicQuestionAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.context = kwargs.get('conversation_context')

    def can_process(self, statement):
        statement_elements_set = set()
        for x in statement.text.lower().split():
            statement_elements_set.add(x.lower())
        basic_requests = self.db.get_responses_list_by_tags(tag="basic_question_request")
        greeting_responses = self.db.get_responses_list_by_tags(tag="greeting_response")
        splitted_name_requests = set()

        splitted_name_requests = statement_utils.split_to_single_words(splitted_name_requests,
                                                                       map(lambda
                                                                               x: statement_utils.filter_unexpected_signs(
                                                                           x.lower(), '?'), basic_requests))
        splitted_name_requests = statement_utils.split_to_single_words(splitted_name_requests,
                                                                       map(lambda
                                                                               x: statement_utils.filter_unexpected_signs(
                                                                           x.lower(), '?'), greeting_responses))

        if len(statement_elements_set.intersection(splitted_name_requests)) > 1:
            return True
        return False

    def process(self, statement, additional_respones_parameters):
        basic_question_responses = self.db.get_random_response_by_tags(tag="basic_question_response")
        basic_question_responses_end = self.db.get_random_response_by_tags(tag="basic_question_response_end")

        if basic_question_responses is not None and basic_question_responses_end is not None:
            result = Statement(statement_utils.prepare_statement(
                basic_question_responses,
                basic_question_responses_end),
                in_response_to=TypeOfOperation.BASIC_QUESTION.value)
            result.confidence = 1.0
            self.db.add_new_doc_to_collection(configuration.RESPONSES_COLLECTION.value,
                                              confidence=result.confidence,
                                              response=result.text)
            return result
        return statement_utils.default_response()
