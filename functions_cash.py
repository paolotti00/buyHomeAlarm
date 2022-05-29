from classes import Home, UserChatConfig, Price

def calculate_prices(advertisement_price) -> [Price]:
    prices = []
    # advertisement_price
    advertisement_price_ob: Price = Price()
    advertisement_price_ob.description = "advertisement price"
    advertisement_price_ob.value = advertisement_price
    prices.append(advertisement_price_ob)
    # calculate estimate price
    estimated_price : Price = Price()
    estimated_price.description = "estimate price - 20% off" # todo maybe put description in constant
    estimated_price_discount = advertisement_price * 20 /100 # todo put 20% in config object
    estimated_price.value = advertisement_price - estimated_price_discount
    prices.append(estimated_price)
    return prices

def add_money_stuffs_calculation(home: Home, user_chat_config: UserChatConfig):
    # this function care of money stuff calculation like mortgage ecc
    prices: [Price] = calculate_prices(home.price)
    for price in prices:
        for mortgage_percentage in UserChatConfig.mortgage_percentages:
            # todo calculate






