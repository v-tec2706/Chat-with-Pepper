from src.common_utils.database.database_service import DatabaseProxy
from src.main_chat.chatbot_manager import ChatbotManager


# from src.main_chat.response_continuation import initialize_db_with_continue_statements


def main():
    # to be run once at first use of this functionality to initialize database
    # initialize_db_with_continue_statements()

    chatbot_manager = ChatbotManager(intro_chatbot='Bolek', university_chatbot='Lolek',
                                     database=DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB'))
    while True:
        user_input = input('>>>')
        res = chatbot_manager.ask_chatbot(user_input)
        print('Answer = ', res)


if __name__ == '__main__':
    main()
