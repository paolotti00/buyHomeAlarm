# classes
from bson import ObjectId


def common_init(self, d=None):
    if d is not None:
        for key, value in d.items():
            # print("key --> " + key + " " + "value --> " + str(value))
            if isinstance(value, list) and isinstance(value[0], dict):
                for item in value:
                    common_init(getattr(type(self), key)[0], dict(item))
            if isinstance(value, list):
                if isinstance(value[0], dict):
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
    query_urls: [str]
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
    searches: [Search] = [Search()]


# telegram bot

class Job:
    def __init__(self, d=None):
        common_init(self, d)

    _id: ObjectId = None
    searches_id: [ObjectId]
    target_emails: [str]
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
    jobs_id: [ObjectId]
    homes_found_id: [ObjectId]

    @property
    def id_mongo(self):
        return self._id
