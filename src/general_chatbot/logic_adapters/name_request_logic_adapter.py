import random

from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter

import src.common_utils.language_utils.statement_utils as statement_utils
from configuration import Configuration
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter
from src.common_utils.types_of_conversation import TypeOfOperation


class NameRequestAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db = kwargs.get('database_proxy')
        self.context = kwargs.get('conversation_context')
        self.confidence = 0
        self.robot_name_request = False
        self.name_response = False
        self.polish_sentence_tokenizer = SentenceFilter()

    def can_process(self, statement):
        statement_elements_set = set()
        for x in statement.text.lower().split():
            statement_elements_set.add(x)
        name_requests = self.db.get_responses_list_by_tags(tag="name_request")
        name_responses = self.db.get_responses_list_by_tags(tag="name_response")
        splitted_name_requests = set()

        splitted_name_requests = statement_utils.split_to_single_words(splitted_name_requests,
                                                                       map(lambda
                                                                               x: statement_utils.filter_unexpected_signs(
                                                                           x.lower(), ','), name_requests))
        splitted_name_requests = statement_utils.split_to_single_words(splitted_name_requests,
                                                                       map(lambda
                                                                               x: statement_utils.filter_unexpected_signs(
                                                                           x.lower(), ','), name_responses))


        if len(statement_elements_set.intersection(
                splitted_name_requests)) >= 1:
            if self.context.is_name_request_processed and not self.context.is_after_name_response_reaction:
                self.name_response = True  # case when speaker introduced himself
                return True
            self.confidence = 0.6
            self.robot_name_request = True  # case when speaker asked about robot name
            return True
        if not self.context.is_after_introduction:
            self.confidence = 0.5  # case when there was no introduction, robot will response with its name,
            # and ask for speaker name
            return True
        if len(statement_elements_set) == 1 and self.context.is_name_request_processed \
                and not self.context.is_after_name_response_reaction:
            self.name_response = True
            return True
        return False

    def process_name_request(self, statement):
        name_responses = self.db.get_responses_list_by_tags(tag="name_response")
        if len(name_responses) > 0:
            name_responses_splitted = list()

            for name_response in name_responses:
                tmp = name_response.split(',')
                if len(tmp) == 2:
                    (request1, request2) = tmp
                    name_responses_splitted.append((request1, request2))

            my_name = self.db.get_first_response_by_tags(tag="my_name")
            (response_text1, response_text2) = name_responses_splitted[random.randint(0, len(name_responses) - 1)]

            response = []
            if not self.robot_name_request:
                response_text_buff = self.db.get_random_response_by_tags(tag="no_introduction_message")
                response.append(response_text_buff)

            response.append(response_text1)
            response.append(my_name)
            if not self.robot_name_request:
                response.append(response_text2)
            result = Statement(statement_utils.prepare_statement(
                response),
                in_response_to=TypeOfOperation.NAME.value)
            result.confidence = 0.3
            self.db.add_new_doc_to_collection(Configuration.RESPONSES_COLLECTION.value,
                                              confidence=result.confidence,
                                              response=result.text)
            return result
        return statement_utils.default_response()

    def process_name_response(self, statement):
        speaker_name = self.find_name(list(statement.text.split()))
        if speaker_name is None:
            return Statement("", in_response_to=TypeOfOperation.CONTEXT_NAME.value)
        if self.polish_sentence_tokenizer.is_name(speaker_name):
            self.context.speaker_name = speaker_name

        name_conversation_end_responses = self.db.get_random_response_by_tags(tag="name_response_end")
        general_conversation_intro = self.db.get_random_response_by_tags(tag="general_conversation_intro")

        if name_conversation_end_responses is not None and general_conversation_intro is not None:
            result = Statement(statement_utils.prepare_statement(
                name_conversation_end_responses,
                self.context.speaker_name,
                general_conversation_intro
            ), in_response_to=TypeOfOperation.CONTEXT_NAME.value)
            self.db.add_new_doc_to_collection(Configuration.RESPONSES_COLLECTION.value,
                                              confidence=result.confidence,
                                              response=result.text)
            result.confidence = 0.4
            return result
        return statement_utils.default_response()

    def process(self, statement, additional_respones_parameters):

        if self.name_response:
            return self.process_name_response(statement)
        else:
            return self.process_name_request(statement)

    def find_name(self, sentence):
        for word in sentence:
            if self.polish_sentence_tokenizer.is_name(word):
                return word
        return None
