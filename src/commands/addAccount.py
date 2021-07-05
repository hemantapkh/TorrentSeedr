from src.objs import *

#: Login or signup seedr account
@bot.message_handler(commands=['add'])
def addAccount(message, userLanguage=None):
    userId = message.from_user.id
    userLanguage = userLanguage or dbSql.getSetting(userId, 'language')

    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.add(telebot.types.InlineKeyboardButton(text=language['login'][userLanguage], url='https://torrentseedrbot.herokuapp.com/login'),
        telebot.types.InlineKeyboardButton(text=language['signup'][userLanguage], url='https://torrentseedrbot.herokuapp.com/signup'))

    bot.send_message(message.from_user.id, language['addAccount'][userLanguage], reply_markup=markup, disable_web_page_preview=True)