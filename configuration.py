from enum import Enum


class Configuration(Enum):
    NAME = 'imię'

    # -------  SCRAPPER CONFIGURATION ----------- #
    ITERS_NUM = 4000
    DATE = '191116'
    STARTING_URL = "https://www.agh.edu.pl"
    CHROME_DRIVER_PATH = r'C:\Users\User\chromedriver_win32\chromedriver.exe'

    # ----------  BOT CONFIGURATION  ------------ #
    NUMBER_OF_SENTENCES_IN_RESPONSE = 2
    REQUESTS_IN_ROW_THRESH = 3

    POP_QUEST_BOT_CONF_THRESH = 0.65
    POP_QUEST_BOT_CONST_CONF = 0.98
    DEFAULT_CONF = 0.0
    MAX_CONF = 1.0

    GOOD_ANSWER_CONFIDENCE = 0.03

    NUMBER_OF_SUGGESTED_RESPONSES = 5

    # ---------- PORTS AND ADDRESSES -------------#
    ROBOT_ADDRESS = '192.168.1.102'
    ROBOT_PORT = 9559
    ROBOT_SOCKET_PORT = 9999
    REST_API_PORT = 5007
    LOCALHOST = 'localhost'
    DATABASE_NAME = 'PepperChatDB'
    DATABASE_ADDRESS = 'mongodb://localhost:27017/'
    BOT_ADDRESS = 'localhost'

    # -------- MONGO COLLECTIONS NAMES -----------#
    # note: each enum name which refers to collections should contain
    # 'collection' key word - it allows for automatic collections creation, another key word is 'capped'
    RESPONSES_COLLECTION = 'responses'
    NUMBERS_QUEST_COLLECTION = 'numbers_collection'
    POPULAR_QUEST_COLLECTION = 'popular_collection'
    QUESTION_COLLECTION_CAPPED = 'question'
    MAIN_COLLECTION = 'main_collection'
    PHRASES_COLLECTION = 'phrases'
    POLISH_STOP_WORDS_COLLECTION = 'polish_stop_words'
    STATEMENTS_COLLECTION = 'statements'

