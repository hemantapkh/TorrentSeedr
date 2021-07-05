from src.objs import *
from src.functions.exceptions import exceptions, noAccount

#: Delete folder
@bot.message_handler(func=lambda message: message.text and message.text[:8] == '/delete_')
def deleteFolder(message):
    userId = message.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')
    ac = dbSql.getDefaultAc(userId)

    #! If user has account
    if ac:
        account = Seedr(cookie=ac['cookie'])

        sent = bot.send_message(message.chat.id, language['deletingFolder'][userLanguage])
        id = message.text[8:]
        response = account.deleteFolder(id).json()

        #! If folder is deleted successfully
        if response['result'] == True:
            bot.edit_message_text(text=language['deletedSuccessfully'][userLanguage], chat_id=message.chat.id, message_id=sent.id)

        else:
            exceptions(message, response, userLanguage)
        
    #! If no accounts
    else:
        noAccount(message, userLanguage)