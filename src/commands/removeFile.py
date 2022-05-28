from src.objs import *
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: Remove files
@bot.message_handler(func=lambda message: message.text and message.text[:8] == '/remove_')
def removeFile(message):
    userId = message.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')

    if floodControl(message, userLanguage):
        ac = dbSql.getDefaultAc(userId)

        #! If user has an account
        if ac:
            sent = bot.send_message(message.chat.id, language['removingFile'][userLanguage])
            id = message.text[8:]

            account = Seedr(
                token=ac['token'],
                callbackFunc=lambda token: dbSql.updateAccount(
                    token, userId, ac['accountId']
                )
            )

            response = account.deleteFile(id)

            if 'error' not in response:
                #! If file removed successfully
                if response['result'] == True:
                    bot.edit_message_text(text=language['removedSuccessfully'][userLanguage], chat_id=message.chat.id, message_id=sent.id)

            else:
                exceptions(message, response, ac, userLanguage)

        #! If no accounts
        else:
            noAccount(message, userLanguage)
