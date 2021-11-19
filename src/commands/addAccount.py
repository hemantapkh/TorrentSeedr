from src.objs import *
from src.functions.referralCode import referralCode
from src.functions.floodControl import floodControl

#: Login or signup seedr account
@bot.message_handler(commands=['login'])
def addAccount(message, called=False, userLanguage=None):
    userId = message.from_user.id

    if floodControl(message, userLanguage):
        userLanguage = userLanguage or dbSql.getSetting(userId, 'language')
        response = getDeviceCode()

        markup = telebot.types.InlineKeyboardMarkup()
        
        markup.add(telebot.types.InlineKeyboardButton(text=language['signupBtn'][userLanguage], url=f'https://www.seedr.cc/?r={referralCode()}'))
        markup.add(telebot.types.InlineKeyboardButton(text=language['doneBtn'][userLanguage], callback_data=f"authorize_{response['device_code']}"))
        
        if called:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.id, text= language['addAccount'][userLanguage].format(response['user_code']), reply_markup=markup, disable_web_page_preview=True)
        
        else:
            bot.send_message(message.from_user.id, language['addAccount'][userLanguage].format(response['user_code']), reply_markup=markup, disable_web_page_preview=True)