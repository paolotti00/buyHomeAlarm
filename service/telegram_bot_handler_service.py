from telegram import Update
from telegram.ext import CallbackQueryHandler

from service.telegram_bot_service import get_func_by_conversation_trigger_button_pressed, \
    get_func_by_normal_button_pressed, add_handler


def conversation_button_pressed_handler(update: Update, context) -> None:
    return get_func_by_conversation_trigger_button_pressed(update, context)


def normal_button_pressed_handler(update: Update, context) -> None:
    return get_func_by_normal_button_pressed(update, context)


def initialize_handler():  # TODO
    # add_handler(CommandHandler("start", start_handler))
    # add_handler(CommandHandler("menu", send_menu_handler))
    # add_handler(CommandHandler("cancel", cancel_handler))
    add_handler(CallbackQueryHandler(normal_button_pressed_handler))
    add_handler(conv_handler)
    return None
