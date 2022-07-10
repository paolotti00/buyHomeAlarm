import ssl

import pymongo
from bson import ObjectId

import service.config_service as func_conf
from model.classes import Job, Search,  Chat, UserConfig, SimpleNamespaceCustom
from model.search_home_classes import Home,  MoneyStuff
import logging
import json

from service.utility_service import convert2serialize


def save_many(collection, list_data: []):
    for data in list_data:
        collection.insert_one(vars(data))
    # print(collection.count_documents({}))
    # print(list(collection.find({})))


def save_one(collection, data):
    collection.insert_one(convert2serialize(data))


def from_cursors_to_list_object(cursors, class_type):
    list_to_return: [] = []
    for cursor in cursors:
        list_to_return.append(from_dict_to_object(cursor))
    return list_to_return


def from_dict_to_object(d: dict):
    # to SimpleNamespace :/
    return json.loads(json.dumps(d, default=str), object_hook=lambda d: SimpleNamespaceCustom(**d))


class Repository:
    def __init__(self):
        client = pymongo.MongoClient(func_conf.get_db_config().connection_string, ssl_cert_reqs=ssl.CERT_NONE)
        mydb = client.buyhomealarm_db
        self.chat_collection = mydb["chat"]
        self.homes_collection = mydb["home"]
        self.home_money_stuff_collection = mydb["homeMoneyStuff"]
        self.jobs_collection = mydb["job"]
        self.action_collection = mydb["action"]  # todo create the collection
        self.searches_collection = mydb["search"]
        self.user_config = mydb["userChatConfig"]

    def save_many_homes(self, list_of_data: []):
        logging.info("saving many homes: %s homes", len(list_of_data))
        save_many(self.homes_collection, list_of_data)

    def get_home_by_id_from_site(self, id_from_site) -> [Home]:
        result = self.homes_collection.find({'id_from_site': {'$eq': id_from_site}})
        return from_cursors_to_list_object(result, Home)

    def get_active_jobs(self) -> [Job]:
        result = self.jobs_collection.find({'active': {'$eq': True}})
        return from_cursors_to_list_object(result, Job)

    def get_job(self, job_id_mongo) -> Job:
        result = self.jobs_collection.find_one({'_id': {'$eq': ObjectId(job_id_mongo)}})
        return from_dict_to_object(result)

    def get_search(self, search_id_mongo):
        result = self.searches_collection.find_one({'_id': {'$eq': ObjectId(search_id_mongo)}})
        return from_dict_to_object(result)

    def get_searches(self, searches_ids: []) -> [Search]:
        searches: [Search] = []
        for searches_id in searches_ids:
            searches.append(self.get_search(searches_id))
        return searches

    def get_chat(self, chat_id_mongo) -> Chat:
        result = self.chat_collection.find_one({'_id': {'$eq': ObjectId(chat_id_mongo)}})
        return from_dict_to_object(result)

    def get_chat_by_telegram_id(self, chat_id_telegram) -> Chat:
        result = self.chat_collection.find_one({'telegram_id': {'$eq': chat_id_telegram}})
        return from_dict_to_object(result)

    def get_user_config_by_id(self, user_config_id_mongo) -> UserConfig:
        result = self.user_config.find_one({'_id': {'$eq': ObjectId(user_config_id_mongo)}})
        return from_dict_to_object(result)

    def get_user_config_by_id_telegram_chat_id(self, telegram_chat_id) -> UserConfig:
        result = self.user_config.find_one({'telegram_chat_id': {'$eq': telegram_chat_id}})
        return from_dict_to_object(result)

    def get_money_stuff_by_home_id_from_site_and_chat_telegram_id(self, home_id_from_site,
                                                                  chat_telegram_id) -> MoneyStuff:
        result = self.home_money_stuff_collection.find_one(
            {'telegram_chat_id': chat_telegram_id, 'home_reference.home_id_from_site': home_id_from_site})
        return from_dict_to_object(result)

    def save_money_stuff(self, money_stuff: MoneyStuff):
        save_one(self.home_money_stuff_collection, money_stuff)

    def get_action(self, action_id):
        result = self.action_collection.find_one({'_id': {'$eq': ObjectId(action_id)}})
        return from_dict_to_object(result)
