import ssl

import pymongo
import functions_config as func_conf
from classes import Job, Search, Home, Chat
import logging


def save_many(collection, list_data: []):
    for data in list_data:
        collection.insert_one(vars(data))
    # print(collection.count_documents({}))
    # print(list(collection.find({})))


def from_cursors_to_list_object(cursors, class_type):
    list_to_return: [] = []
    for cursor in cursors:
        list_to_return.append(class_type(cursor))
    return list_to_return


class Repository:
    def __init__(self):
        client = pymongo.MongoClient(func_conf.get_db_config().connection_string, ssl_cert_reqs=ssl.CERT_NONE)
        mydb = client.buyhomealarm_db
        self.chat_collection = mydb["chat"]
        self.homes_collection = mydb["home"]
        self.jobs_collection = mydb["job"]
        self.searches_collection = mydb["search"]

    def save_many_homes(self, list_of_data: []):
        logging.info("saving many homes: %s homes", len(list_of_data))
        save_many(self.homes_collection, list_of_data)

    def get_home(self, id_from_site) -> [Home]:
        result = self.homes_collection.find({'id_from_site': {'$eq': id_from_site}})
        return from_cursors_to_list_object(result, Home)

    def get_active_jobs(self) -> [Job]:
        result = self.jobs_collection.find({'active': {'$eq': True}})
        return from_cursors_to_list_object(result, Job)

    def get_job(self, job_id_mongo) -> Job:
        result = self.jobs_collection.find_one({'_id': {'$eq': job_id_mongo}})
        return Job(result)

    def get_search(self, search_id_mongo):
        result = self.searches_collection.find_one({'_id': {'$eq': search_id_mongo}})
        return Search(result)

    def get_searches_from_job_id(self, job_id) -> [Search]:
        searches: [Search] = []
        searches_ids = self.get_job(job_id).searches_id
        for searches_id_mongo in searches_ids:
            searches.append(self.get_search(searches_id_mongo))
        return searches

    def get_searches(self, searches_ids: []) -> [Search]:
        searches: [Search] = []
        for searches_id in searches_ids:
            searches.append(list(self.jobs_collection.find({'_id': {'$eq': searches_id}})))
        return from_cursors_to_list_object(searches, Search)

    def get_chat(self, chat_id_mongo) -> Chat:
        result = self.chat_collection.find_one({'_id': {'$eq': chat_id_mongo}})
        return Chat(result)
