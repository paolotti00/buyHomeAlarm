from telegram import Update
from telegram.ext import CallbackQueryHandler, CallbackContext

from constant.constant_telegram_bot import IT_PHRASE_END_CONV, SUP_BTN_KEY_MNY_STUFF_CALC
from service.telegram_bot_conversation_service import conv_handler,get_func_by_conversation_trigger_button_pressed,get_func_by_normal_button_pressed
from service.telegram_bot_service import  \
    add_handler, end_conversation, cancel_conversation


def conversation_button_pressed_handler(update: Update, context) -> None:
    return get_func_by_conversation_trigger_button_pressed(update, context)


def normal_button_pressed_handler(update: Update, context) -> None:
    return get_func_by_normal_button_pressed(update, context)


async def cancel_conversation_handler(update: Update, context: CallbackContext):
    return cancel_conversation(Update, context)


def initialize_handler():  # TODO
    # add_handler(CommandHandler("start", start_handler))
    # add_handler(CommandHandler("menu", send_menu_handler))
    # add_handler(CommandHandler("cancel", cancel_handler))
    add_handler(CallbackQueryHandler(normal_button_pressed_handler))
    add_handler(conv_handler)
    return None
