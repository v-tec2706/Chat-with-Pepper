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
    REQUESTS_IN_ROW_THRESH = 5

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
    RESPONSES_COLLECTION = 'responses'
    QUESTION_COLLECTION_CAPPED = 'question'
    NUMBER_OF_SUGGESTED_RESPONSES = 5
    MAIN_COLLECTION = 'main_collection'
    PHRASES_COLLECTION = 'phrases'
