# classes
from types import SimpleNamespace

from bson import ObjectId


# configuration file
from model.search_home_classes import Site, Search
from service.classes_utility_service import common_init


class Bot:
    def __init__(self, d=None):
        common_init(self, d)

    api_token = None


class Telegram:
    def __init__(self, d=None):
        common_init(self, d)

    bot: Bot()


class Sender:
    def __init__(self, d=None):
        common_init(self, d)

    email = None
    password = None
    domain_name = None
    port = None


class Email:
    def __init__(self, d=None):
        common_init(self, d)

    subject = None
    sender: Sender = Sender()


class DB:
    def __init__(self, d=None):
        common_init(self, d)

    connection_string: str = None


class TechConf:
    def __init__(self, d=None):
        common_init(self, d)

    date_pattern = None
    scheduler_time_minutes = None


class Config:
    def __init__(self, d=None):
        common_init(self, d)

    tech_conf: TechConf = TechConf()
    email: Email = Email()
    db: DB = DB()
    sites: [Site] = [Site()]
    supported_sites_conf: [Site] = [Site()]
    telegram: Telegram = Telegram()
    searches: [Search] = [Search()]


# telegram bot

class ActionSearchHome:  # todo create the collection
    def __init__(self, d=None):
        common_init(self, d)

    _id: ObjectId = None
    searches_ids: [ObjectId]
    target_emails: [str]
    send_email: bool = None
    send_in_chat: bool = None
    chat_id: ObjectId = None
    type: str  # example : ActionSearchHome ecc


class Job:
    def __init__(self, d=None):
        common_init(self, d)

    _id: ObjectId = None
    active: bool = None
    n_minutes_timer: int = None
    action_id: str = ObjectId


class UserConfig:
    def __init__(self, d=None):
        common_init(self, d)

    _id: ObjectId = None
    cash_held: int = None
    mortgage_percentages: [int]
    agency_percentage: int
    agency_percentage_vat_percentage: int
    fixed_costs_bank: int
    fixed_costs_notary: int


class Chat:
    def __init__(self, d=None):
        common_init(self, d)

    _id = None
    telegram_id = None
    date_of_creation = None
    jobs_id: [ObjectId]
    homes_found_id: [ObjectId]
    user_config_id: ObjectId = None


class Button:
    def __init__(self, d=None):
        common_init(self, d)

    text: str = None
    callback_function: str = None
    parameters: str = None
    url: str = None


# extend python class
class SimpleNamespaceCustom(SimpleNamespace):
    def __getattr__(self, name):
        return "Attribute '{}' doesnt exist".format(str(name))
