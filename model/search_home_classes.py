from bson import ObjectId

from service.classes_utility_service import common_init


class Price:
    def __init__(self, d=None):
        common_init(self, d)

    description: str
    value: float


# home
class HomeReference:
    def __init__(self, d=None):
        common_init(self, d)

        _id: ObjectId = None
        home_id: ObjectId = None
        home_id_from_site = None


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

    def get_price(self):
        return self.price


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
    base_price: float
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

    _id: ObjectId = None
    telegram_chat_id = None
    cash_held: int = None
    fixed_costs: FixedCost = FixedCost()
    cases: [MoneyStuffCase] = [MoneyStuffCase()]
    home_reference: HomeReference


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


class HomeMustHave:
    def __init__(self, d=None):
        common_init(self, d)

    balcony: bool = None
    excludeAuction: bool = None
    terrace: bool = None


class HomeUserSearch:
    def __init__(self, d=None):
        common_init(self, d)

    priceMin: int = None
    priceMax: int = None
    mt2Min: int = None
    mt2Max: int = None
    zones: [str]
    mustHave: HomeMustHave = HomeMustHave()
    floor: int = None
