from src.objs import *
from src.functions.keyboard import mainReplyKeyboard

def exceptions(message, response, userLanguage):
    if 'result' in response:
        if response['result'] == 'login_required':
            bot.send_message(message.chat.id, language['loginRequired'][userLanguage])
    
    else:
        print(response)

def noAccount(message, userLanguage):
    bot.send_message(message.chat.id, language['noAccount'][userLanguage], reply_markup=mainReplyKeyboard(userId=message.from_user.id, userLanguage=userLanguage))