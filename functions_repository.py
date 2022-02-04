import pymongo
from classes import Message
import logging


def save_many(collection, list_data: []):
    for data in list_data:
        collection.insert_one(vars(data))
    # print(collection.count_documents({}))
    # print(list(collection.find({})))


class Repository:
    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://buyhomealarm_app_pi_dev:AcCyAZyX6H9H3EJ@cluster0.oh329.mongodb.net/buyhomealarm_db?retryWrites=true&w=majority")
        mydb = client.buyhomealarm_db
        self.messages_collection = mydb["messages"]
        self.homes_collection = mydb["home"]

    def save_many_homes(self, list_of_data: []):
        logging.info("saving many homes: %s homes", len(list_of_data))
        save_many(self.homes_collection, list_of_data)

    def save_many_messages(self, list_of_data: []):
        logging.info("saving many homes: %s homes", len(list_of_data))
        save_many(self.messages_collection, list_of_data)

    def save_message(self, data):
        list_of_data: [Message] = []
        list_of_data.append(data)
        self.save_many_messages(list_of_data)

    def get_home(self, home_id):
        result = self.homes_collection.find({'id': {'$eq': home_id}})
        return list(result)
