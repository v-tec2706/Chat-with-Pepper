import src.common_utils.language_utils.statement_utils as statement
from configuration import Configuration as configuration
from src.common_utils.database.collection_utils import parse_documents
from src.common_utils.language_utils.sentence_filter_utils import SentenceFilter


class ResponseContinuationHandler:
    def __init__(self, db_proxy):
        self.db = db_proxy
        self.sf = SentenceFilter()
        self.response_length = configuration.NUMBER_OF_SENTENCES_IN_RESPONSE.value
        self.current_response_offset = 0 + self.response_length

    def is_continuation_request_asked(self, input_statement):
        continuation_requests = set(self.db.get_responses_list_by_tags(tag="continue"))
        sliced_statement = set(map(lambda x: SentenceFilter.list_to_str_with_colons(self.sf.extract_lemma(x, True)),
                                                            input_statement.split(' ')))
        return statement.complex_intersection(sliced_statement, continuation_requests) > 1

    def return_next_part_of_response(self, question):
        if not self.is_continuation_request_asked(question):
            self.current_response_offset = 1 #0 + self.response_length
            return None
        full_response = self.db.get_sorted_collection_elements(configuration.RESPONSES_COLLECTION.value, 'confidence',
                                                               n=1)
        full_response = parse_documents(full_response, ['response'])
        offset = self.current_response_offset
        self.current_response_offset += self.response_length
        response = statement.prepare_shortened_statement(full_response[0]['response'], offset, self.response_length)
        if response is None:
            return self.db.get_random_response_by_tags(tag="cannot_say_more")
        return response
