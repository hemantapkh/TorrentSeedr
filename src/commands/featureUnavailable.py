from src.objs import *
from src.functions.keyboard import githubAuthKeyboard

def featureUnavailable(message, userLanguage):
    bot.send_message(message.chat.id, language['featureNotAvailable'][userLanguage]+'\n\n'+language['getFreeSpace'][userLanguage], reply_markup=githubAuthKeyboard(userLanguage))