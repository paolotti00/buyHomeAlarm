from mongita import MongitaClientDisk

from classes import Message


def save_many(collection, list_data: []):
    for data in list_data:
        collection.insert_one(vars(data))
    # print(collection.count_documents({}))
    print(list(collection.find({})))


class Repository:
    def __init__(self):
        self.client = MongitaClientDisk("./._db")
        self.db = self.client.db
        self.messages_collection = self.db.messages_collection
        self.homes_collection = self.db.homes_collection

    def save_many_homes(self, list_of_data: []):
        save_many(self.homes_collection, list_of_data)

    def save_many_messages(self, list_of_data: []):
        save_many(self.messages_collection, list_of_data)

    def save_message(self, data):
        list_of_data: [Message] = []
        list_of_data.append(data)
        self.save_many_messages(list_of_data)

    def get_home(self, home_id):
        result = self.homes_collection.find({'id': {'$eq': home_id}})
        return list(result)
