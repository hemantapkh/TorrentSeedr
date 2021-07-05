from src.objs import *
from src.functions.exceptions import exceptions, noAccount

#: Get download link of torrents
@bot.message_handler(func=lambda message: message.text and message.text[:9] == '/getLink_')
def getLink(message):
    userId = message.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')
    ac = dbSql.getDefaultAc(userId)

    #! If user has an account
    if ac:
        id = message.text[9:]
        account = Seedr(cookie=ac['cookie'])

        sent = bot.send_message(message.chat.id, language['fetchingLink'][userLanguage])
        response = account.createArchive(id).json()

        #! If download link found
        if 'archive_url' in response:
            text = f"🔗 {response['archive_url']}\n\n<b>🔥via @TorrentSeedrBot</b>"
            bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=sent.id)
        
        else:
            exceptions(message, response, userLanguage)
    
    #! If no accounts
    else:
        noAccount(message, userLanguage)