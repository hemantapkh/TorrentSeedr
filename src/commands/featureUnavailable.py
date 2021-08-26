from src.objs import *
from src.functions.keyboard import githubAuthKeyboard

def featureUnavailable(message, userLanguage):
    userId = message.from_user.id
    if dbSql.getSetting(userId, 'githubId') == '0':
        bot.send_message(message.chat.id, language['featureNotAvailable'][userLanguage]+'\n\n'+language['getFreeSpace'][userLanguage], reply_markup=githubAuthKeyboard(userLanguage))
    else:
        bot.send_message(message.chat.id, language['featureNotAvailable'][userLanguage])