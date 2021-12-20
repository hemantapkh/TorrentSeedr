from src.objs import *
from src.callbacks.authorize import authorize
from src.functions.keyboard import mainReplyKeyboard

def exceptions(message, response, ac, userLanguage, called=False):
    chatId = message.message.chat.id if called else message.chat.id

    if response['error'] in ['expired_token', 'invalid_token']:
        authorize(message, ac['id'], ac['deviceCode'], userLanguage, refreshMode=True)
    
    else:
        bot.send_message(chatId, language['unknownError'][userLanguage], reply_markup=mainReplyKeyboard(userId=chatId, userLanguage=userLanguage))

def noAccount(message, userLanguage, called=False):
    chatId = message.message.chat.id if called else message.chat.id
    bot.send_message(chatId, language['noAccount'][userLanguage], reply_markup=mainReplyKeyboard(userId=message.from_user.id, userLanguage=userLanguage))