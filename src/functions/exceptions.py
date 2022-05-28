from src.objs import *
from src.functions.keyboard import mainReplyKeyboard


def exceptions(message, response, ac, userLanguage, called=False):
    chatId = message.message.chat.id if called else message.chat.id

    if response['error'] == 'invalid_token':
        dbSql.deleteAccount(chatId, ac['id'])
        bot.send_message(chatId, language['tokenExpired'][userLanguage], reply_markup=mainReplyKeyboard(userId=chatId, userLanguage=userLanguage))

    else:
        bot.send_message(chatId, language['unknownError'][userLanguage], reply_markup=mainReplyKeyboard(userId=chatId, userLanguage=userLanguage))


def noAccount(message, userLanguage, called=False):
    chatId = message.message.chat.id if called else message.chat.id
    bot.send_message(chatId, language['noAccount'][userLanguage], reply_markup=mainReplyKeyboard(userId=message.from_user.id, userLanguage=userLanguage))
