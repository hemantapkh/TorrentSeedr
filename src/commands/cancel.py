from src.objs import *
from src.functions.keyboard import mainReplyKeyboard

def cancel(message, userLanguage=None):
    userLanguage = userLanguage or dbSql.getSetting(message.chat.id, 'language')
    bot.send_message(message.chat.id, language['cancelled'][userLanguage], reply_markup=mainReplyKeyboard(message.from_user.id, userLanguage))