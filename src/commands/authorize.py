from src.objs import *
from src.functions.floodControl import floodControl


#: Login or signup seedr account
@bot.message_handler(commands=['authorize'])
def authorize(message, called=False, userLanguage=None):
    userId = message.from_user.id

    if floodControl(message, userLanguage):
        userLanguage = userLanguage or dbSql.getSetting(userId, 'language')
        response = Login().getDeviceCode()

        markup = telebot.types.InlineKeyboardMarkup()

        markup.add(telebot.types.InlineKeyboardButton(text=language['doneBtn'][userLanguage], callback_data=f"Authorize_{response['device_code']}"))

        if called:
            markup.add(telebot.types.InlineKeyboardButton(text=language['backBtn'][userLanguage], callback_data="addAccount"))
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.id, text= language['authorize'][userLanguage].format(response['user_code']), reply_markup=markup, disable_web_page_preview=True)

        else:
            bot.send_message(message.from_user.id, language['authorize'][userLanguage].format(response['user_code']), reply_markup=markup, disable_web_page_preview=True)
