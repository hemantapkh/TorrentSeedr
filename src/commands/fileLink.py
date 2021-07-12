from src.objs import *
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount

#: Get download link of files
@bot.message_handler(func=lambda message: message.text and message.text[:10] == '/fileLink_')
def fileLink(message):
    userId = message.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')

    if floodControl(message, userLanguage):
        ac = dbSql.getDefaultAc(userId)

        #! If user has an account
        if ac:
            id = message.text[10:]
            account = Seedr(cookie=ac['cookie'])

            sent = bot.send_message(message.chat.id, language['fetchingLink'][userLanguage])
            response = account.fetchFile(id).json()

            #! If download link found
            if 'url' in response:
                text = f"🖹 <b>{response['name']}</b>\n\n"
                text += f"🔗 {response['url']}\n\n<b>🔥via @TorrentSeedrBot</b>"
                bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=sent.id)
            
            else:
                exceptions(message, response, userLanguage)
        
        #! If no accounts
        else:
            noAccount(message, userLanguage)