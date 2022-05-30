from classes import Home, UserChatConfig, Price, CalculationResult


def calculate_prices(advertisement_price) -> [Price]:
    prices = []
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


def add_money_stuffs_calculation(home: Home, user_chat_config: UserChatConfig) -> [CalculationResult]:
    # this function care of money stuff calculation like mortgage ecc
    calculation_results = []
    prices: [Price] = calculate_prices(home.price)
    for price in prices:
        for mortgage_percentage in UserChatConfig.mortgage_percentages:
            calculation_result: CalculationResult = CalculationResult()
            # mortgage calculation
            calculation_result.total_cash_needed = 0
            calculation_result.description = price.description + " " + mortgage_percentage
            calculation_result.mortgage_cash_needed = price.value - ((price.value * (100 - mortgage_percentage)) / 100)
            calculation_result.mortgage_money_to_be_requested = price.value - calculation_result.mortgage_cash_needed
            # agency cost calculation
            agency_commission_without_vat = ((price.value * UserChatConfig.agency_percentage) / 100)
            agency_commission = agency_commission_without_vat + (
                        (agency_commission_without_vat * UserChatConfig.agency_percentage_vat_percentage) / 100)
            # totals
            calculation_result.total_cash_needed = calculation_result.mortgage_cash_needed + agency_commission
            calculation_result.total_cash_needed = UserChatConfig.fixed_costs_bank + UserChatConfig.fixed_costs_notary
            calculation_result.total_cash_left = UserChatConfig.cash_held - calculation_result.total_cash_needed
            # todo calculate
            calculation_results.append(calculation_result)
