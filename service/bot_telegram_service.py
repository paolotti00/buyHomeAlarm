import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, Updater, CallbackQueryHandler, ApplicationBuilder, ContextTypes, \
    ConversationHandler, MessageHandler, CommandHandler, filters

from model.classes import Search, Button, UserConfig
from model.search_home_classes import Home, MoneyStuff
from service import config_service
from service.cash_service import get_money_stuffs
from service.repository_service import Repository

updater = None
TEST, TEST1, TEST2, TEST3 = range(4)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("ciao Denise")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Your Message")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry I can't recognize you , you said '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


async def send_text(msg, chat_telegram_id, disable_notification: bool):
    await app.bot.send_message(chat_id=chat_telegram_id, text=msg, disable_notification=disable_notification)


async def send_as_html(chat_telegram_id, text, disable_notification):
    await app.bot.send_message(chat_id=chat_telegram_id, parse_mode=ParseMode.HTML, text=text,
                               disable_notification=disable_notification)


async def send_as_html_with_buttons(chat_telegram_id, text, disable_notification, buttons: [Button]):
    keyboard_elements = []
    if len(buttons) > 0:
        inline_keyboard_buttons: [InlineKeyboardButton] = []
        for received_button in buttons:
            inline_keyboard_button = InlineKeyboardButton(text=str(received_button.text),
                                                          callback_data=str(
                                                              received_button.callback_function) + ":" + str(
                                                              received_button.parameters),
                                                          url=received_button.url if received_button.url is not None else None)
            inline_keyboard_buttons.append(inline_keyboard_button)
        keyboard_elements = [[element] for element in inline_keyboard_buttons]
    await app.bot.send_message(chat_id=chat_telegram_id, parse_mode=ParseMode.HTML, text=text,
                               disable_notification=disable_notification,
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_elements))


# buttons callbacks
async def do_money_stuff_calculation(query, parameters: str):
    # parameters
    repository = Repository()
    chat_telegram_id = parameters.split(",")[0]
    home_id_from_site = parameters.split(",")[1]
    home = repository.get_home_by_id_from_site(home_id_from_site)[0]
    money_stuff = get_money_stuffs(home, chat_telegram_id)
    await send_home(chat_telegram_id, False, home, None, money_stuff)


async def test(query, parameters: str):
    chat_telegram_id = parameters.split(",")[0]
    await send_text(
        'You pressed test.', chat_telegram_id, False
    )
    return TEST1


async def test1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(update.message.text)
    await update.message.reply_text(
        update.message.text
    )
    return ConversationHandler.END


async def test2(query, parameters: str):
    chat_telegram_id = parameters.split(",")[0]
    await send_text(
        'You pressed test2.', chat_telegram_id, False
    )
    return TEST3


async def test3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(update.message.text)
    await update.message.reply_text(
        update.message.text
    )
    return ConversationHandler.END


def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(update.message.text)


supported_buttons = {
    "money_stuff_calculations": do_money_stuff_calculation,
    "test": test,
    "test2": test2,

}


def button(update: Update, context) -> None:
    query = update.callback_query
    button_pressed = query.data.split(':')[0]
    parameters = query.data.split(':')[1]
    return supported_buttons.get(button_pressed)(query, parameters)


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
        button_mortgage_calculation.text = "test"
        button_mortgage_calculation.callback_function = "test"
        button_mortgage_calculation.parameters = chat_telegram_id + "," + home.id_from_site
        buttons.append(button_mortgage_calculation)

        button_mortgage_calculation1: Button = Button()
        button_mortgage_calculation1.text = "test2"
        button_mortgage_calculation1.callback_function = "test2"
        button_mortgage_calculation1.parameters = chat_telegram_id + "," + home.id_from_site
        buttons.append(button_mortgage_calculation1)
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
    await send_as_html_with_buttons(chat_telegram_id, disable_notification=disable_notification, text=text_to_send,
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


conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button)],
    states={
        TEST1: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), test1)],
        TEST3: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), test3)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    conversation_timeout=8
)


def start_bot():
    global app
    app = ApplicationBuilder().token(config_service.get_telegram_confing().bot.api_token).build()
    # app.add_handler(CallbackQueryHandler(button))
    app.add_handler(conv_handler)
    app.run_polling()
