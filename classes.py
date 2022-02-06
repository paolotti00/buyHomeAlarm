# classes
from bson import ObjectId


def common_init(self, d=None):
    if d is not None:
        for key, value in d.items():
            print("key --> " + key + " " + "value --> " + str(value))
            if isinstance(value, list) and isinstance(value[0], dict):
                print("dentro if")
                for item in value:
                    common_init(getattr(type(self), key)[0], dict(item))
            print(type(value))
            print("---------- set attr key --> " + key + " value --> " + str(value))
            if isinstance(value,list):
                if isinstance(value[0],dict):
                    continue
            setattr(self, key, value)


class Home:
    def __init__(self, d=None):
        common_init(self, d)

    _id: ObjectId = None
    id_from_site = None
    title = None
    price = None
    zone = None
    mt2 = None
    floor = None
    n_rooms = None
    n_bath_rooms = None
    parking = None
    description = None
    description_short = None
    link_detail = None
    origin_site = None
    date = None

    @property
    def id_mongo(self):
        return self._id


class Site:
    def __init__(self, d=None):
        common_init(self, d)

    site_name: str
    base_url = None
    query_urls: [str] = [str]
    api_case_string = None


class Search:
    def __init__(self, d=None):
        common_init(self, d)

    _id: ObjectId = None
    title = None
    description = None
    sites: [Site] = [Site()]

    # chatId: str = None

    @property
    def id_mongo(self):
        return self._id


class Message:
    def __init__(self, d=None):
        common_init(self, d)

    is_sent = None
    sent_date = None
    creation_date = None
    zones: [Search] = None


# configuration file


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
    sender: Sender = None


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

    tech_conf: TechConf = None
    email: Email = None
    db: DB = None
    sites: [Site] = None
    supported_sites_conf: [Site] = None
    searches: [Search] = None


# telegram bot

class Job:
    def __init__(self, d=None):
        common_init(self, d)

    _id: ObjectId = None
    searches_id: [ObjectId] = None
    target_emails: [str] = None
    active: bool = None
    n_minutes_timer: int = None
    send_email: bool = None
    send_in_chat: bool = None
    chat_id: ObjectId = None

    @property
    def id_mongo(self):
        return self._id


class Chat:
    def __init__(self, d=None):
        common_init(self, d)

    _id = None
    telegram_id = None
    date_of_creation = None
    jobs_id: [ObjectId] = None
    homes_found_id: [ObjectId] = None

    @property
    def id_mongo(self):
        return self._id
