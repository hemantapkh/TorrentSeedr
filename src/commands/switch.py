from src.objs import *
from src.functions.exceptions import noAccount
from src.functions.floodControl import floodControl
from src.functions.keyboard import mainReplyKeyboard


#: Instantly login as another account
@bot.message_handler(commands=['switch'])
def switch(message, userLanguage=None):
    userLanguage = userLanguage or dbSql.getSetting(message.from_user.id, 'language')

    if floodControl(message, userLanguage):
        accounts = dbSql.getAccounts(message.from_user.id)

        if accounts:
            if len(accounts) > 1:
                defaultAcID = dbSql.getSetting(message.from_user.id, 'defaultAcId')

                #!? Get the index of current default account
                for i,j in enumerate(accounts):
                    if j['id'] == defaultAcID:
                        defaultAcIndex = i

                #!? If (condition), more accounts should be there ahead of that index
                ## Make defaultAcIndex+1 as the default account
                if len(accounts) > defaultAcIndex+1:
                    accountId = accounts[defaultAcIndex+1]['id']
                    username = accounts[defaultAcIndex+1]['userName']
                    dbSql.setSetting(message.from_user.id, 'defaultAcId', accountId)

                #!? If no accounts ahead, make the first account as the default account
                else:
                    accountId = accounts[0]['id']
                    username = accounts[0]['userName']
                    dbSql.setSetting(message.from_user.id, 'defaultAcId', accountId)

                bot.send_message(message.chat.id, language['loggedInAs'][userLanguage].format(username), reply_markup=mainReplyKeyboard(message.from_user.id, userLanguage))

            else:
                bot.send_message(message.chat.id, language['noMultipleAccounts'][userLanguage])

        else:
            noAccount(message, userLanguage)
