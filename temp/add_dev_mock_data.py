from munch import Munch
import ssl
from datetime import datetime

import pymongo
from bson import ObjectId

# from temp.classes import Job, Search, Site, Chat
from classes import Job, Search, Site, Chat

client = pymongo.MongoClient(
    "mongodb+srv://buyhomealarm_app_pi_dev:AcCyAZyX6H9H3EJ@cluster0.oh329.mongodb.net/buyhomealarm_db?retryWrites=true&w=majority",
    ssl_cert_reqs=ssl.CERT_NONE)
mydb = client.buyhomealarm_db
mydb.chat_collection = mydb["chat"]
mydb.homes_collection = mydb["home"]
mydb.jobs_collection = mydb["job"]
mydb.searches_collection = mydb["search"]


# # ---- job
# job: Job = Job()
# job.n_minutes_timer = 10
# job.active = True
# job.chat_id = ObjectId("61ffbd67bbd4538b9296f299")
# job.send_email= True
# job.send_in_chat = True
# job.target_emails=["email@email.it","email2@email.it"]
# job.searchesId=[ObjectId("61ffb907eade4ba62c2612c3")]
#
# mydb.jobs_collection.insert_one(vars(job))

# # ---- search
# search: Search = Search()
# search.title = "cassia, tomba di nerone, due ponti"
# site: Site = Site()
# site.site_name = "immobiliare"
# site.query_urls = ["https://www.immobiliare.it/vendita-case/roma/con-piani-intermedi/?criterio=rilevanza&prezzoMassimo=300000&superficieMinima=80&fasciaPiano[]=30&idMZona[]=10160&idQuartiere[]=10835&idQuartiere[]=10836&idQuartiere[]=12743"]
# search.sites = []
# search.sites.append(vars(site))
# test = vars(search)
# mydb.searches_collection.insert_one(vars(search))

# # ---- chat
# chat: Chat = Chat()
# chat.date_of_creation = datetime.now()
# chat.telegram_id = 1
# chat.jobs_id = [ObjectId("61ffb907eade4ba62c2612c3")]
# mydb.chat_collection.insert_one(vars(chat))

# # --- utility
# class DictToObject(object):
#
#     def __init__(self, dictionary):
#         def _traverse(key, element):
#             if isinstance(element, dict):
#                 return key, DictToObject(element)
#             else:
#                 return key, element
#
#         objd = dict(_traverse(k, v) for k, v in dictionary.iteritems())
#         self.__dict__.update(objd)


# -- test
job_id = ObjectId("61ffbba60197ad010b27f91a")
result = mydb.searches_collection.find_one({'_id': {'$eq': job_id}})
job = Search(result)

print(job.sites[0].site_name)
