from src.objs import *
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: Cancel active downloads
@bot.message_handler(func=lambda message: message.text and message.text[:8] == '/cancel_')
def cancelDownload(message, called=False):
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

            if not called:
                sent = bot.send_message(message.chat.id, language['cancellingDownload'][userLanguage])
                id = message.text[8:]

            else:
                id = message.data[7:]

            response = account.deleteTorrent(id)

            if 'error' not in response:
                #! If torrent cancelled successfully
                if response['result'] == True:
                    bot.edit_message_text(text=language['cancelledSuccessfully'][userLanguage], chat_id=message.message.chat.id if called else message.chat.id, message_id=message.message.id if called else sent.id)

            else:
                exceptions(message, response, ac, userLanguage, called)

        #! If no accounts
        else:
            noAccount(message, userLanguage)
