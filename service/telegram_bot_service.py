from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ConversationHandler, CallbackContext

from constant.constant_telegram_bot import IT_PHRASE_END_CONV, IN_CONVERSATION
from model.classes import Button
from service import config_service


async def cancel_conversation(update: Update, context: CallbackContext):
    await update.message.reply_text(IT_PHRASE_END_CONV + " " + update.message.from_user.name)
    await end_conversation(update, context)


async def send_text(chat_telegram_id, text, disable_notification: bool = False, parse_mode=None):
    await app.bot.send_message(chat_id=chat_telegram_id,
                               text=text,
                               parse_mode=parse_mode if parse_mode is not None else None,
                               disable_notification=disable_notification)


async def end_conversation(update, context: CallbackContext):
    context.user_data[IN_CONVERSATION] = False
    return ConversationHandler.END


async def reply_to_message(update, msg_to_send):
    await update.message.reply_text(
        msg_to_send
    )


async def send_text_with_buttons(chat_telegram_id, text, parse_mode, disable_notification, buttons: [Button]):
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
    await app.bot.send_message(chat_id=chat_telegram_id, parse_mode=parse_mode, text=text,
                               disable_notification=disable_notification,
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_elements))


def create_bot():
    global app
    app = ApplicationBuilder().token(config_service.get_telegram_confing().bot.api_token).build()


def add_handler(handler):
    app.add_handler(handler)


def start_bot():
    app.run_polling()
