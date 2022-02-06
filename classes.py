# classes
class Home:
    id = None
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


class Site:
    site_name = None
    base_url = None
    query_urls: [str] = None
    api_case_string = None


class Search:
    title = None
    description = None
    sites: [Site] = None
    homes: [Home] = None
    # chatId: str = None


class Message:
    is_sent = None
    sent_date = None
    creation_date = None
    zones: [Search] = None


# configuration file


class Sender:
    email = None
    password = None
    domain_name = None
    port = None


class Email:
    subject = None
    sender: Sender = None


class DB:
    connection_string: str = None


class TechConf:
    date_pattern = None
    scheduler_time_minutes = None


class Config:
    tech_conf: TechConf = None
    email: Email = None
    db: DB = None
    sites: [Site] = None
    supported_sites_conf: [Site] = None
    searches: [Search] = None


# telegram bot

class Job:
    id = None
    searchesId: [str] = None
    target_emails: [str] = None
    active: bool = None
    n_minutes_timer: int = None
    send_email: bool = None
    send_in_chat: bool = None
    chatId: int = None


class Chat:
    id = None
    date_of_creation = None
    schedulersId: [str] = None
