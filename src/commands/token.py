from src.objs import *

from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: View account profile, add new accounts and remove existing accounts
@bot.message_handler(commands=['token'])
def token(message, userLanguage=None):
    userId = message.from_user.id

    if floodControl(message, userLanguage):
        userLanguage = userLanguage or dbSql.getSetting(userId, 'language')
        ac = dbSql.getDefaultAc(userId)

        #! If user has an account
        if ac:
           bot.send_message(message.chat.id, language['token'][userLanguage].format(ac['userName'], ac['token']))

        #! If no accounts
        else:
            noAccount(message, userLanguage)
