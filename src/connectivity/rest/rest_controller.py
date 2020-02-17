import logging

from flask import Flask
from flask_jsonpify import jsonify
from flask_restful import Resource, Api

from configuration import Configuration as configuration
from src.common_utils.database.collection_utils import parse_documents
from src.common_utils.database.database_service import DatabaseProxy

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
api = Api(app)


class Responses(Resource):

    def __init__(self):
        self.db = DatabaseProxy(configuration.DATABASE_ADDRESS.value, configuration.DATABASE_NAME.value)

    def get(self):
        docs = self.db.get_sorted_collection_elements(configuration.RESPONSES_COLLECTION.value, 'confidence')
        result = parse_documents(docs, ['confidence', 'response'])
        return jsonify({'suggested responses': result})


class Ping(Resource):
    def get(self):
        return jsonify("I'm Pepper and I'm ready for questions! :) ")


class Question(Resource):
    def __init__(self):
        self.db = DatabaseProxy(configuration.DATABASE_ADDRESS.value, configuration.DATABASE_NAME.value)

    def get(self):
        result_collection = self.db.get_elements_of_capped_collection(configuration.QUESTION_COLLECTION_CAPPED.value,
                                                                      'question')
        return jsonify({'current question': result_collection})


api.add_resource(Responses, '/responses')
api.add_resource(Ping, '/ping')
api.add_resource(Question, '/question')

if __name__ == '__main__':
    app.run(port=configuration.REST_API_PORT.value)
