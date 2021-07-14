from src.objs import *
from src.functions.keyboard import mainReplyKeyboard

def exceptions(message, response, userLanguage, called=False):
    chatId = message.message.chat.id if called else message.chat.id
    if 'result' in response:
        if response['result'] == 'login_required':
            bot.send_message(chatId, language['loginRequired'][userLanguage])
    
    else:
        print(response)

def noAccount(message, userLanguage, called=False):
    chatId = message.message.chat.id if called else message.chat.id
    bot.send_message(chatId, language['noAccount'][userLanguage], reply_markup=mainReplyKeyboard(userId=message.from_user.id, userLanguage=userLanguage))