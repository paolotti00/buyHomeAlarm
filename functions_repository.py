import pymongo
import functions_config as func_conf
from classes import Message, Job, Search
import logging


def save_many(collection, list_data: []):
    for data in list_data:
        collection.insert_one(vars(data))
    # print(collection.count_documents({}))
    # print(list(collection.find({})))


class Repository:
    def __init__(self):
        client = pymongo.MongoClient(func_conf.get_db_config().connection_string)
        mydb = client.buyhomealarm_db
        self.messages_collection = mydb["messages"]
        self.homes_collection = mydb["home"]
        self.jobs_collection = mydb["job"]
        self.searches_collection = mydb["search"]

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

    def get_active_jobs(self) -> [Job]:
        result = self.jobs_collection.find({'active': {'$eq': 'true'}})
        return list(result)

    def get_job(self, job_id):
        result = self.jobs_collection.find({'id': {'$eq': job_id}})
        return list(result)

    def get_searches_from_job_id(self, job_id) -> [Search]:
        searches: [Search] = []
        searches_ids = self.jobs_collection.find({'_id': {'$eq': job_id}}).get['searchesId']
        for searches_id in searches_ids:
            searches.append(list(self.jobs_collection.find({'_id': {'$eq': searches_id}})))
        return searches

    def get_searches(self, searches_ids: []) -> [Search]:
        searches: [Search] = []
        for searches_id in searches_ids:
            searches.append(list(self.jobs_collection.find({'_id': {'$eq': searches_id}})))
        return searches
