from chatterbot import ChatBot

from configuration import Configuration


class UniversityBot:
    def __init__(self, name, db_proxy):
        self.name = name
        self._bot = self.initialize_chatbot(db_proxy)
        self._responses_in_row = 0

    def get_bot(self):
        return self._bot

    def check_was_requested_in_row_above_thresh(self):
        return self._responses_in_row >= Configuration.REQUESTS_IN_ROW_THRESH.value

    def inc_responses_in_row(self):
        self._responses_in_row += 1
        print('Responses_in_row = ', self._responses_in_row)

    def reset_responses_in_row(self):
        print('Responses_in_row reset = ', self._responses_in_row)
        self._responses_in_row = 0

    def initialize_chatbot(self, db_proxy):
        return ChatBot(
            self.name,
            logic_adapters=[
                {
                    'import_path': 'src.university_chatbot.university_conversation_logic_adapter'
                                   '.UniversityAdapter',
                    'database_proxy': db_proxy
                },
            ],
        )

    def get_bot_response(self, input):
        response = self._bot.get_response(input)
        return response
