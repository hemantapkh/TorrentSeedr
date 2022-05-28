from src.objs import *
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: Delete folder
@bot.message_handler(func=lambda message: message.text and message.text[:8] == '/delete_')
def deleteFolder(message, called=False):
    userId = message.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')

    if floodControl(message, userLanguage):
        ac = dbSql.getDefaultAc(userId)

        #! If user has an account
        if ac:
            account = Seedr(
                token=ac['token'],
                callbackFunc=lambda token: dbSql.updateAccount(
                    token, userId, ac['accountId']
                )
            )

            id = message.data[7:] if called else message.text[8:]
            response = account.deleteFolder(id)

            if 'error' not in response:
                #! If folder is deleted successfully
                if response['result'] == True:
                    if called:
                        bot.answer_callback_query(message.id)
                        bot.edit_message_text(text=language['deletedSuccessfully'][userLanguage], chat_id=message.message.chat.id, message_id=message.message.id)
                    else:
                        bot.send_message(message.chat.id, language['deletedSuccessfully'][userLanguage])

            else:
                exceptions(message, response, ac, userLanguage, called)

        #! If no accounts
        else:
            noAccount(message, userLanguage)
