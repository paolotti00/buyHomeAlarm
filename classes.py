# classes
from bson import ObjectId


# todo check if can delete this
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


# Money stuffs and cash calculation

class FixedCost:
    def __init__(self, d=None):
        common_init(self, d)

    bank: int = None
    notary: int = None


class MoneyStuffCase:
    def __init__(self, d=None):
        common_init(self, d)

    description: str
    mortgage_percentage: int
    mortgage_cash_needed: int
    mortgage_money_to_be_requested: int
    agency_commission: int
    fixed_costs_bank: int
    fixed_costs_notary: int
    fixed_costs_total: int
    total_cash_needed: int
    total_cash_left: int


class MoneyStuff:
    def __init__(self, d=None):
        common_init(self, d)

    cash_held: int = None
    fixed_costs: FixedCost = FixedCost()
    cases: [MoneyStuffCase] = [MoneyStuffCase()]


class Price:
    def __init__(self, d=None):
        common_init(self, d)

    description: str
    value: int


# home
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
    money_stuff: MoneyStuff = None

    def get_price(self):
        return self.price


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
    keywords: [str]

    # chatId: str = None


# configuration file
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
    user_config_id: ObjectId = None


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


class Button:
    def __init__(self, d=None):
        common_init(self, d)

    text: str = None
    callback_function: str = None
    parameters: str
