from src.objs import *
from src.functions.exceptions import exceptions, noAccount

#: Cancel active downloads
@bot.message_handler(func=lambda message: message.text and message.text[:8] == '/cancel_')
def cancelDownload(message):
    userId = message.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')
    ac = dbSql.getDefaultAc(userId)

    #! If user has an account
    if ac:
        account = Seedr(cookie=ac['cookie'])

        sent = bot.send_message(message.chat.id, language['cancellingDownload'][userLanguage])
        id = message.text[8:]
        response = account.deleteTorrent(id).json()

        #! If torrent cancelled successfully
        if response['result'] == True:
            bot.edit_message_text(text=language['cancelledSuccessfully'][userLanguage], chat_id=message.chat.id, message_id=sent.id)

        else:
            exceptions(message, response, userLanguage)
        
    #! If no accounts
    else:
        noAccount(message, userLanguage)