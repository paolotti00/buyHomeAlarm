import logging
from model.classes import UserConfig, Chat
from model.search_home_classes import Home, Price, MoneyStuff, FixedCost, MoneyStuffCase, HomeReference
from service.utility_service import clean_price_and_convert_to_int
from service.repository_service import Repository


def calculate_prices(advertisement_price: str) -> [Price]:
    prices = []
    advertisement_price = clean_price_and_convert_to_int(advertisement_price)
    # advertisement_price
    advertisement_price_ob: Price = Price()
    advertisement_price_ob.description = "prezzo annuncio"
    advertisement_price_ob.value = advertisement_price
    prices.append(advertisement_price_ob)
    # calculate estimate price
    estimated_price: Price = Price()
    estimated_price.description = "prezzo meno il 20%"  # todo maybe put description in constant
    estimated_price_discount = advertisement_price * 20 / 100  # todo put 20% in config object
    estimated_price.value = advertisement_price - estimated_price_discount
    prices.append(estimated_price)
    return prices


def do_money_stuffs_calculation_from_price(price, user_chat_config: UserConfig, money_stuff_cases) -> [MoneyStuffCase]:
    for mortgage_percentage in user_chat_config.mortgage_percentages:
        money_stuff_case: MoneyStuffCase = MoneyStuffCase()
        money_stuff_case.base_price = price.value
        # mortgage calculation
        money_stuff_case.total_cash_needed = 0
        money_stuff_case.description = price.description + " mutuo al " + str(mortgage_percentage) + "%"
        money_stuff_case.mortgage_percentage = mortgage_percentage
        money_stuff_case.mortgage_cash_needed = (price.value * (100 - mortgage_percentage)) / 100
        money_stuff_case.mortgage_money_to_be_requested = price.value - money_stuff_case.mortgage_cash_needed
        # agency cost calculation
        agency_commission_without_vat = ((price.value * user_chat_config.agency_percentage) / 100)
        money_stuff_case.agency_commission = agency_commission_without_vat + (
                (agency_commission_without_vat * user_chat_config.agency_percentage_vat_percentage) / 100)
        # fixed costs
        money_stuff_case.fixed_costs_bank = user_chat_config.fixed_costs_bank
        money_stuff_case.fixed_costs_notary = user_chat_config.fixed_costs_notary
        money_stuff_case.fixed_costs_total = user_chat_config.fixed_costs_bank + user_chat_config.fixed_costs_notary
        # totals
        money_stuff_case.total_cash_needed = money_stuff_case.mortgage_cash_needed + money_stuff_case.agency_commission
        money_stuff_case.total_cash_needed = money_stuff_case.total_cash_needed + money_stuff_case.fixed_costs_total
        money_stuff_case.total_cash_left = user_chat_config.cash_held - money_stuff_case.total_cash_needed

        money_stuff_case = money_stuff_case
        money_stuff_cases.append(money_stuff_case)
    return money_stuff_cases


def do_money_stuffs_calculation_from_prices(prices: [Price], user_chat_config: UserConfig) -> []:
    # money stuff cases
    money_stuff_cases = []
    for price in prices:
        money_stuff_cases = do_money_stuffs_calculation_from_price(price, user_chat_config, money_stuff_cases)
    return money_stuff_cases


def do_money_stuffs_calculation_from_home(home: Home, user_chat_config: UserConfig) -> MoneyStuff:
    logging.info("start to calculate money stuff for home %s", home.id_from_site)
    # this function care of money stuff calculation like mortgage ecc
    money_stuff = MoneyStuff()
    # fixed costs
    fixed_cost = FixedCost()
    fixed_cost.bank = user_chat_config.fixed_costs_bank
    fixed_cost.notary = user_chat_config.fixed_costs_notary
    money_stuff.fixed_costs = fixed_cost
    money_stuff.cash_held = user_chat_config.cash_held
    prices: [Price] = calculate_prices(home.price)
    money_stuff.cases = do_money_stuffs_calculation_from_prices(prices, user_chat_config)
    logging.info("finished to calculate money stuff for home %s", home.id_from_site)
    return money_stuff


def do_money_stuffs_calculation_from_custom_offer(home: Home, chat_telegram_id, offer) -> MoneyStuff:
    # retrieve the old one
    repository = Repository()
    chat: Chat = repository.get_chat_by_telegram_id(chat_telegram_id)
    user_chat_config = repository.get_user_config_by_id(chat.user_config_id)
    money_stuffs: MoneyStuff = get_money_stuffs(home, chat_telegram_id)
    # calculate the new one
    price = Price()
    price.value = offer
    price.description = "custom_offer"
    money_stuff_cases_to_add = do_money_stuffs_calculation_from_price(price, user_chat_config)
    # add to old ones
    money_stuffs.cases.append(money_stuff_cases_to_add)
    # save with new one case
    save_money_stuffs(home, chat_telegram_id, money_stuffs)
    return money_stuffs


def get_money_stuffs(home: Home, telegram_chat_id) -> MoneyStuff:
    logging.info("start to get money stuff for home %s", home.id_from_site)
    repository = Repository()
    # check if already exist on db
    money_stuffs = repository.get_money_stuff_by_home_id_from_site_and_chat_telegram_id(home.id_from_site,
                                                                                        telegram_chat_id)
    if money_stuffs is None:
        # not already exist on db - will be calculated and saved
        logging.info("not already exist on db - will be calculated and saved for home %s", home.id_from_site)
        chat: Chat = repository.get_chat_by_telegram_id(telegram_chat_id)
        user_chat_config = repository.get_user_config_by_id(chat.user_config_id)
        money_stuffs = do_money_stuffs_calculation_from_home(home, user_chat_config)
        # save it
        save_money_stuffs(home, telegram_chat_id, money_stuffs)
    else:
        logging.info("money stuff already exist for home %s", home.id_from_site)
    logging.info("money stuff for home %s calculated or retrieved successfully", home.id_from_site)
    return money_stuffs


def save_money_stuffs(home: Home, telegram_chat_id, money_stuffs: [MoneyStuff]):
    repository = Repository()
    # save it
    logging.info("saving money stuff for home %s", home.id_from_site)
    money_stuffs.telegram_chat_id = telegram_chat_id
    home_reference: HomeReference = HomeReference()
    home_reference.home_id = home._id
    home_reference.home_id_from_site = home.id_from_site
    money_stuffs.home_reference = home_reference
    repository.save_money_stuff(money_stuffs)
    logging.info("money stuff for home %s saved", home.id_from_site)
