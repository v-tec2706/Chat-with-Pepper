from configuration import Configuration
from src.common_utils.database.database_service import DatabaseProxy


def extract_keys(document, keys):
    return [document[key] for key in keys]


def parse_documents(documents, keys):
    result = []
    for document in documents:
        result.append(dict([(key, document[key]) for key in keys]))
    return result


database = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
docs = database.get_sorted_collection_elements(Configuration.RESPONSES_COLLECTION.value, 'confidence')
res = parse_documents(docs, ['confidence', 'response'])
