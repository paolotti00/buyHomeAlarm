import logging
from classes import Home, UserConfig, Price, MoneyStuff, FixedCost, MoneyStuffCase
from fuctions_utility import clean_price_and_convert_to_int


def calculate_prices(advertisement_price: str) -> [Price]:
    prices = []
    advertisement_price = clean_price_and_convert_to_int(advertisement_price)
    # advertisement_price
    advertisement_price_ob: Price = Price()
    advertisement_price_ob.description = "advertisement price"
    advertisement_price_ob.value = advertisement_price
    prices.append(advertisement_price_ob)
    # calculate estimate price
    estimated_price: Price = Price()
    estimated_price.description = "estimate price - 20% off"  # todo maybe put description in constant
    estimated_price_discount = advertisement_price * 20 / 100  # todo put 20% in config object
    estimated_price.value = advertisement_price - estimated_price_discount
    prices.append(estimated_price)
    return prices


def add_money_stuffs_calculation(home: Home, user_chat_config: UserConfig) -> Home:
    logging.info("start to rich home %s", home.id_from_site)
    # this function care of money stuff calculation like mortgage ecc
    money_stuff = MoneyStuff()
    # fixed costs
    fixed_cost = FixedCost()
    fixed_cost.bank = user_chat_config.fixed_costs_bank
    fixed_cost.notary = user_chat_config.fixed_costs_notary
    money_stuff.fixed_costs = fixed_cost
    money_stuff.cash_held = user_chat_config.cash_held
    # money stuff cases
    money_stuff_cases = []

    prices: [Price] = calculate_prices(home.price)
    for price in prices:
        for mortgage_percentage in user_chat_config.mortgage_percentages:
            money_stuff_case: MoneyStuffCase = MoneyStuffCase()
            # mortgage calculation
            money_stuff_case.total_cash_needed = 0
            money_stuff_case.description = price.description + " " + str(mortgage_percentage)
            money_stuff_case.mortgage_percentage = mortgage_percentage
            money_stuff_case.mortgage_cash_needed = (price.value * (100 - mortgage_percentage)) / 100
            money_stuff_case.mortgage_money_to_be_requested = price.value - money_stuff_case.mortgage_cash_needed
            # agency cost calculation
            agency_commission_without_vat = ((price.value * user_chat_config.agency_percentage) / 100)
            agency_commission = agency_commission_without_vat + (
                    (agency_commission_without_vat * user_chat_config.agency_percentage_vat_percentage) / 100)
            # totals
            money_stuff_case.total_cash_needed = money_stuff_case.mortgage_cash_needed + agency_commission
            money_stuff_case.total_cash_needed = money_stuff_case.total_cash_needed + user_chat_config.fixed_costs_bank
            money_stuff_case.total_cash_needed = money_stuff_case.total_cash_needed + user_chat_config.fixed_costs_notary
            money_stuff_case.total_cash_left = user_chat_config.cash_held - money_stuff_case.total_cash_needed

            money_stuff_case.calculation_result = money_stuff_case
            money_stuff_cases.append(money_stuff_case)
    money_stuff.cases = money_stuff_cases
    home.money_stuff = money_stuff
    logging.info("finished to rich home %s", home.id_from_site)
    return home
