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


class Message:
    is_sent = None
    sent_date = None
    creation_date = None
    homes: [Home] = None


# configuration file

class Site:
    site_name = None
    base_url = None
    query_urls: [] = None


class Sender:
    email = None
    password = None
    domain_name = None
    port = None


class Email:
    subject = None
    sender: Sender = None


class Conf:
    date_pattern = None


class Config:
    conf: Conf = None
    email: Email = None
    sites: [Site] = None
