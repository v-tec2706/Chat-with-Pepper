import random

from chatterbot.storage import MongoDatabaseAdapter
from pymongo import MongoClient

from src.common_utils.custom_exceptions import CollectionAlreadyExistsInDatabaseError
from src.common_utils.custom_exceptions import CollectionNotExistsInDatabaseError
from src.common_utils.custom_exceptions import ResponseTextByTagsNotFoundError


def is_invalid_arg(arg):
    return arg is None


class DatabaseProxy:
    def __init__(self, connection_uri, database_name):
        self.database_uri = connection_uri + database_name
        self.stat_collection = MongoDatabaseAdapter(database_uri=self.database_uri)
        mongo_client = MongoClient(connection_uri)
        self.collections_db = mongo_client[database_name]

    def add_conversation(self, **tags):  # tags == kwargs
        """Method adds new conversation to database with specified tags
           Returns text of added conversation's statement"""
        try:
            tags.get('text')
        except KeyError:
            print("No \'text\' atribute in **tags in add_conversation()")
            return None
        created_statement = self.stat_collection.create(**tags)
        return created_statement.text

    def get_responses_list_by_tags(self, **tags):
        """Method returns list of statements text list which match given tags"""
        statement_results = list(self.stat_collection.filter(**tags))
        if len(statement_results) == 0:
            raise ResponseTextByTagsNotFoundError
        text_results = []
        for statement in statement_results:
            text_results.append(statement.text)
        return text_results

    def get_first_response_by_tags(self, **tags):
        """Method returns first statement's text which match given tags"""
        try:
            responses = self.get_responses_list_by_tags(**tags)
        except ResponseTextByTagsNotFoundError:
            print("No response text for given tags found")
            return None
        return responses[0]

    def get_random_response_by_tags(self, **tags):
        """Method returns random statement's text which match given tags"""
        try:
            responses = self.get_responses_list_by_tags(**tags)
        except ResponseTextByTagsNotFoundError:
            print("No response text for given tags found")
            return None
        num_of_responses = len(responses)
        index = random.randint(0, num_of_responses - 1)
        return responses[index]

    def remove_conversation(self, **tags):
        '''Method removes conversation specified with tags from database
           It returns text of statement which is removed'''
        conversation_to_remove = self.get_first_response_by_tags(**tags)
        if is_invalid_arg(conversation_to_remove):
            return None
        self.stat_collection.remove(conversation_to_remove)
        return conversation_to_remove

    def update_conversation_text(self, new_text, **tags):
        """Method updates text of statement in database with specified tags
           Returns updated statement's text"""
        matching_statements = list(self.stat_collection.filter(**tags))
        if len(matching_statements) == 0:
            raise ResponseTextByTagsNotFoundError
        updated_statements = []
        for matching_statement in matching_statements:
            matching_statement.text = new_text
            st = self.stat_collection.update(matching_statement)
            updated_statements.append(st.text)
        return updated_statements

    def get_count(self):
        """Method returns number of documents in database"""
        return self.stat_collection.count()

    def print_documents_by_tags(self, **tags):
        """Method prints documents from database with specified tags"""
        result_list = list(self.stat_collection.filter(**tags))
        if len(result_list) == 0:
            raise ResponseTextByTagsNotFoundError
        for result in result_list:
            print("Document nr ", result.id, ", text = ", result.text)

    def add_doc_with_tags_list(self, collection_name, tags_list, response_text):
        if isinstance(tags_list, list):
            res = self.add_new_doc_to_collection(collection_name, tags=tags_list, text=response_text)
            return res
        raise TypeError('Argument tags_list is not list')

    def get_docs_from_collection_by_tags_list(self, collection_name, tags_list):
        if isinstance(tags_list, list):
            search_doc = {'tags': {'$in': tags_list}}
            docs_found = self.get_docs_from_collection(collection_name, search_doc)
            return docs_found
        raise TypeError('Argument tags_list is not list')

    def get_one_doc_from_collection_by_tags_list(self, collection_name, tags_list):
        if isinstance(tags_list, list):
            docs_found = self.get_docs_from_collection_by_tags_list(collection_name, tags_list)
            for elem in docs_found:
                if set(elem['tags']) == set(tags_list):
                    return elem
        return None

    # part of code for collections other than statements
    def create_new_collection(self, collection_name):
        if collection_name not in self.collections_db.collection_names():
            self.collections_db.create_collection(name=collection_name)
            return True
        raise CollectionAlreadyExistsInDatabaseError

    def create_new_capped_collection(self, collection_name, max_size=1):
        if collection_name not in self.collections_db.collection_names():
            self.collections_db.create_collection(name=collection_name, capped=True,
                                                  size=max_size * 4096,
                                                  max=max_size)
            return True
        raise CollectionAlreadyExistsInDatabaseError

    def get_sorted_collection_elements(self, collection_name, field_to_sort_by, order=-1, n=5):
        """returns n elements of collection sorted in ascending(1) or descending(-1) order"""
        return self.collections_db[collection_name].find().sort(field_to_sort_by, order).limit(n)

    def get_elements_of_capped_collection(self, collection_name, dict_key, n=-1, m=-1):
        """ returns elements from n-th to m-th index of collection, for n,m = -1 returns all elements """
        try:
            responses = []
            for x in list(self.collections_db[collection_name].find())[::-1]:
                responses.append(x[dict_key])
            if n == -1 and m == -1:
                return responses
            else:
                return responses[n:m]
        except (IndexError, KeyError):
            return None

    def remove_collection(self, collection_name):
        if collection_name in self.collections_db.collection_names():
            self.collections_db.drop_collection(name_or_collection=collection_name)
            return True
        raise CollectionNotExistsInDatabaseError

    def clear_collection(self, collection_name):
        if collection_name in self.collections_db.collection_names():
            self.collections_db[collection_name].remove({})
            return True
        raise CollectionNotExistsInDatabaseError

    def add_new_doc_to_collection(self, collection_name, **doc):
        if collection_name in self.collections_db.collection_names():
            collection = self.collections_db[collection_name]
            collection.insert_one(doc)
            return True
        raise CollectionNotExistsInDatabaseError

    def add_many_new_docs_to_collection(self, collection_name, list_of_docs):
        if collection_name in self.collections_db.collection_names():
            collection = self.collections_db[collection_name]
            collection.insert_many(list_of_docs)
            return True
        raise CollectionNotExistsInDatabaseError

    def get_docs_from_collection(self, collection_name, doc_dict):
        if collection_name in self.collections_db.collection_names():
            collection = self.collections_db[collection_name]
            docs_found = list(collection.find(doc_dict))
            return docs_found
        raise CollectionNotExistsInDatabaseError

    def remove_doc_from_collection(self, collection_name, **doc):
        if collection_name in self.collections_db.collection_names():
            collection = self.collections_db[collection_name]
            collection.delete_one(doc)
            return True
        raise CollectionNotExistsInDatabaseError

    def update_doc_in_collection(self, collection_name, search_values_dict, new_values_dict):
        if collection_name in self.collections_db.collection_names():
            collection = self.collections_db[collection_name]
            values_to_update = {"$set": new_values_dict}
            collection.update_one(search_values_dict, values_to_update)  # no upsert
            return True
        raise CollectionNotExistsInDatabaseError

    def update_many_docs_in_collection(self, collection_name, search_values_dict, new_values_dict):
        if collection_name in self.collections_db.collection_names():
            collection = self.collections_db[collection_name]
            values_to_update = {"$set": new_values_dict}
            collection.update_many(search_values_dict, values_to_update)
            return True
        raise CollectionNotExistsInDatabaseError
