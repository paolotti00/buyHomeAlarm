from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, Updater, CallbackQueryHandler, ApplicationBuilder, ContextTypes

from constant.constant_telegram_bot import SUP_BTN_KEY_MNY_STUFF_CALC_C_OFF
from model.classes import Search, Button, UserConfig
from model.search_home_classes import Home, MoneyStuff
from service.cash_service import get_money_stuffs, do_money_stuffs_calculation_from_custom_offer
from service.repository_service import Repository

# buttons callbacks
from service.telegram_bot_service import send_text_with_buttons


async def do_money_stuff_calculation(query, parameters: str):
    # parameters
    repository = Repository()
    chat_telegram_id = parameters.split(",")[0]
    home_id_from_site = parameters.split(",")[1]
    home = repository.get_home_by_id_from_site(home_id_from_site)[0]
    money_stuff = get_money_stuffs(home, chat_telegram_id)
    await send_home(chat_telegram_id, False, home, None, money_stuff)


supported_buttons_functions = {
    "money_stuff_calculations": do_money_stuff_calculation
}


# conversation callbacks
async def do_money_stuff_calculation_from_custom_offer(update, context: CallbackContext):
    repository = Repository()
    # todo move parameters in an dict to set on user_data
    parameters = context.user_data.get(SUP_BTN_KEY_MNY_STUFF_CALC_C_OFF)
    chat_telegram_id = parameters.split(",")[0]
    home_id_from_site = parameters.split(",")[1]
    user_offer = parameters.split(",")[2]
    home = repository.get_home_by_id_from_site(home_id_from_site)[0]
    money_stuff = do_money_stuffs_calculation_from_custom_offer(home, chat_telegram_id, user_offer)
    await send_home(chat_telegram_id, False, home, None, money_stuff)


# no callback functions:

async def send_home(chat_telegram_id, disable_notification, home: Home, search: Search, money_stuff: MoneyStuff):
    hashtags = ""
    if search is not None:
        try:
            for hashtag in search.keywords:
                hashtags = hashtags + " " + "#" + hashtag
        except AttributeError:
            # todo fixme find the way to avoid : AttributeError: 'types.SimpleNamespace' object has no attribute 'keywords'
            pass
    # add buttons
    buttons = []
    url_button: Button = Button()
    url_button.url = home.link_detail
    url_button.text = "vai a vederlo!"
    buttons.append(url_button)

    if money_stuff is None:
        # button mortgage
        button_mortgage_calculation: Button = Button()
        button_mortgage_calculation.text = "fammi i calcoli"
        button_mortgage_calculation.callback_function = "money_stuff_calculations"
        button_mortgage_calculation.parameters = chat_telegram_id + "," + home.id_from_site
        buttons.append(button_mortgage_calculation)
    text_to_send = "<b>da: </b> {origin_site} | <b>ricerca:</b> {search_title} \n \n" + \
                   "<b>{title}</b> \n" + \
                   "<b>Descrizione: breve </b> {description_short} \n" + \
                   "<b>prezzo:</b> {price} \n" + \
                   "<b>mt2:</b> {mt2} | <b>zona:</b> {zone} \n" + \
                   "<b>piano:</b> {floor} | <b>locali:</b> {n_rooms} \n" + \
                   "<b>bagni:</b> {n_bath_rooms} | <b>data annuncio:</b> {date} \n" + \
                   "\n" + \
                   " {description}" + \
                   "\n" + \
                   ("\n" + get_money_stuff_as_html(money_stuff) if money_stuff else "") + "\n" + \
                   "- \n" + \
                   hashtags + \
                   "\n" + \
                   "- \n" + \
                   "<a href='{link_detail}'> link </a>" + \
                   " \n"
    text_to_send = text_to_send.format(origin_site=home.origin_site,
                                       search_title=search.title if search else "",
                                       title=home.title,
                                       description_short=home.description_short,
                                       price=home.price,
                                       mt2=home.mt2,
                                       zone=home.zone,
                                       floor=home.floor,
                                       n_rooms=home.n_rooms,
                                       n_bath_rooms=home.n_bath_rooms,
                                       date=home.date,
                                       description=home.description,
                                       link_detail=home.link_detail)
    await send_text_with_buttons(chat_telegram_id, text=text_to_send, parse_mode=ParseMode.HTML,
                                 disable_notification=disable_notification,
                                 buttons=buttons)


def get_money_stuff_as_html(money_stuff) -> str:
    repository = Repository()
    user_chat_config: UserConfig = repository.get_user_config_by_id_telegram_chat_id(money_stuff.telegram_chat_id)
    to_return: str = "--------------------------------------- \n" + \
                     "--------------------------------------- \n" + \
                     "\n" + \
                     "\n" + \
                     "CALCOLI MONETARI: \n" + \
                     "<b>contanti posseduti:</b>" + str(user_chat_config.cash_held) + "\n" + \
                     "--------------------------------------- \n"
    for money_stuff_case in money_stuff.cases:
        test = "<b>Descrizione:  </b> {money_stuff_case_description} \n" + \
               "\n" + \
               "<b>prezzo partenza: </b> {base_price} \n" + \
               "<b>agenzia - commissione  4%: </b> {agency_commission_needed} \n" + \
               "<b>mutuo - percentuale mutuo: </b> {mortgage_percentage} \n" + \
               "<b>mutuo - soldi da richiedere:</b> {mortgage_money_to_be_requested} \n" + \
               "<b>mutuo - contanti necessari: </b> {mortgage_cash_needed} \n" + \
               "<b>costi fissi forfettari: </b> {fixed_costs} \n" + \
               "\n" + \
               "<b>contanti necessari in totale: </b> {total_cash_needed} \n" + \
               "<b>contanti che rimangono: </b> {total_cash_left} \n" + \
               "--------------------------------------- \n"
        to_return = to_return + test.format(
            base_price=money_stuff_case.base_price,
            money_stuff_case_description=money_stuff_case.description.capitalize(),
            agency_commission_needed=money_stuff_case.agency_commission,
            mortgage_percentage=money_stuff_case.mortgage_percentage,
            mortgage_money_to_be_requested=money_stuff_case.mortgage_money_to_be_requested,
            mortgage_cash_needed=money_stuff_case.mortgage_cash_needed,
            fixed_costs=money_stuff_case.fixed_costs_notary + money_stuff_case.fixed_costs_bank,
            total_cash_needed=money_stuff_case.total_cash_needed,
            total_cash_left=money_stuff_case.total_cash_left
        )
    return to_return
