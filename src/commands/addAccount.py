from src.objs import *
from src.functions.referralCode import referralCode
from src.functions.floodControl import floodControl

#: Login or signup seedr account
@bot.message_handler(commands=['add'])
def addAccount(message, userLanguage=None):
    userId = message.from_user.id

    if floodControl(message, userLanguage):
        userLanguage = userLanguage or dbSql.getSetting(userId, 'language')

        markup = telebot.types.InlineKeyboardMarkup()
        
        markup.add(telebot.types.InlineKeyboardButton(text=language['loginBtn'][userLanguage], url='https://torrentseedrbot.herokuapp.com/login'),
            telebot.types.InlineKeyboardButton(text=language['signupBtn'][userLanguage], url=f'https://www.seedr.cc/?r={referralCode()}'))

        bot.send_message(message.from_user.id, language['addAccount'][userLanguage], reply_markup=markup, disable_web_page_preview=True)