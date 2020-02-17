from chatterbot import ChatBot


class IntroBot:
    def __init__(self, name, bot_context, db_proxy):
        self.name = name
        self._context = bot_context
        self._bot = self.initialize_chatbot(db_proxy)

    def get_bot(self):
        return self._bot

    def initialize_chatbot(self, db_proxy):
        return ChatBot(
            self.name,
            logic_adapters=[
                {
                    'import_path': 'src.general_chatbot.logic_adapters.greetings_logic_adapter.GreetingAdapter',
                    'conversation_context': self._context,
                    'database_proxy': db_proxy

                },
                {
                    'import_path': 'src.general_chatbot.logic_adapters.name_request_logic_adapter.NameRequestAdapter',
                    'conversation_context': self._context,
                    'database_proxy': db_proxy

                },
                {
                    'import_path': 'src.general_chatbot.logic_adapters.basic_question_logic_adapter'
                                   '.BasicQuestionAdapter',
                    'conversation_context': self._context,
                    'database_proxy': db_proxy
                },
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'Przepraszam ale nie rozumiem.',
                    'maximum_similarity_threshold': 0.40
                }
            ],
        )

    def context_update(self, type_of_conversation):
        self._context.context_update(type_of_conversation)

    def get_bot_response(self, input):
        response = self._bot.get_response(input)
        return response

    def check_is_bot_unemployed(self):
        return self._context.is_after_greeting and \
               self._context.is_after_introduction and \
               self._context.is_name_request_processed and \
               self._context.is_after_name_response_reaction
