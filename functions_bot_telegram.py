from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import logging

import functions_config
from classes import Home, Search, MoneyStuff, MoneyStuffCase, Button, Chat, UserConfig
from functions_cash import get_money_stuffs
from functions_repository import Repository

updater = Updater(functions_config.get_telegram_confing().bot.api_token, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("ciao Denise")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Your Message")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry I can't recognize you , you said '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


def send_text(msg, chat_telegram_id):
    updater.bot.send_message(chat_id=chat_telegram_id, text=msg)


def send_as_html(chat_telegram_id, text, disable_notification):
    updater.bot.send_message(chat_id=chat_telegram_id, parse_mode=ParseMode.HTML, text=text,
                             disable_notification=disable_notification)


def send_as_html_with_buttons(chat_telegram_id, text, disable_notification, buttons: [Button]):
    keyboard_elements = []
    if len(buttons) > 0:
        inline_keyboard_buttons: [InlineKeyboardButton] = []
        for received_button in buttons:
            inline_keyboard_button = InlineKeyboardButton(text=received_button.text,
                                                          callback_data=received_button.callback_function + ":" + received_button.parameters)
            inline_keyboard_buttons.append(inline_keyboard_button)
        keyboard_elements = [[element] for element in inline_keyboard_buttons]
    updater.bot.send_message(chat_id=chat_telegram_id, parse_mode=ParseMode.HTML, text=text,
                             disable_notification=disable_notification,
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_elements))


# buttons callbacks
def do_money_stuff_calculation(query, parameters: str):
    # parameters
    repository = Repository()
    chat_telegram_id = parameters.split(",")[0]
    home_id_from_site = parameters.split(",")[1]
    home = repository.get_home_by_id_from_site(home_id_from_site)[0]
    money_stuff = get_money_stuffs(home, chat_telegram_id)
    send_home(chat_telegram_id, False, home, None, money_stuff)


supported_buttons = {
    "money_stuff_calculations": do_money_stuff_calculation

}


def button(update: Update, context) -> None:
    query = update.callback_query
    button_pressed = query.data.split(':')[0]
    parameters = query.data.split(':')[1]
    return supported_buttons.get(button_pressed)(query, parameters)


# no callback functions:

def send_home(chat_telegram_id, disable_notification, home: Home, search: Search, money_stuff: MoneyStuff):
    hashtags = ""
    if search is not None:
        try:
            for hashtag in search.keywords:
                hashtags = hashtags + " " + "#" + hashtag
        except AttributeError:
            # todo fixme find the way to avoid : AttributeError: 'types.SimpleNamespace' object has no attribute 'keywords'
            pass
    buttons = []
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
                   "\n" + (get_money_stuff_as_html(money_stuff) if money_stuff else "") + "\n" + \
                   "\n" + \
                   "<a href='{link_detail}'> vai a vederlo!</a>" + \
                   "\n" + \
                   "- \n" + \
                   hashtags + \
                   "\n" + \
                   "- \n" + \
                   "- \n"
    try:
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
                                           # todo mortgage
                                           # cash_held=home.money_stuff.cash_held,
                                           link_detail=home.link_detail)
    except AttributeError:
        pass
    send_as_html_with_buttons(chat_telegram_id, disable_notification=disable_notification, text=text_to_send,
                              buttons=buttons)


def get_money_stuff_as_html(money_stuff) -> str:
    repository = Repository()
    user_chat_config: UserConfig = repository.get_user_config_by_id_telegram_chat_id(money_stuff.telegram_chat_id)
    to_return: str = "dati monetari: \n"
    for money_stuff_case in money_stuff.cases:
        test = "<b>contanti posseduti:</b> {cash_held} \n" + \
               "<b>Descrizione:  </b> {money_stuff_case_description} \n" + \
               "<b>commissione agenzia 4%: </b> {agency_commission_needed} \n" + \
               "<b>percentuale mutuo: </b> {mortgage_percentage} \n" + \
               "<b>soldi da richiedere:</b> {mortgage_money_to_be_requested} \n" + \
               "<b>contanti necessari per mutuo: </b> {mortgage_cash_needed} \n" + \
               "<b>costi fissi forfettari: </b> {fixed_costs} \n" + \
               "<b>contanti necessari in totale: </b> {total_cash_needed} \n" + \
               "<b>contanti che rimangono: </b> {total_cash_left} \n" + \
               "--------------------------------------- \n"
        to_return = to_return + test.format(
            cash_held=user_chat_config.cash_held,
            money_stuff_case_description=money_stuff_case.description,
            agency_commission_needed=money_stuff_case.agency_commission,
            mortgage_percentage=money_stuff_case.mortgage_percentage,
            mortgage_money_to_be_requested=money_stuff_case.mortgage_money_to_be_requested,
            mortgage_cash_needed=money_stuff_case.mortgage_cash_needed,
            fixed_costs=money_stuff_case.fixed_costs_notary + money_stuff_case.fixed_costs_bank,
            total_cash_needed=money_stuff_case.total_cash_needed,
            total_cash_left=money_stuff_case.total_cash_left
        )
    return to_return


# updater.dispatcher.add_handler(CommandHandler('start', start))


# updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
# Filters out unknown commands
# updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
# Filters out unknown messages.
# updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


def start_bot():
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
