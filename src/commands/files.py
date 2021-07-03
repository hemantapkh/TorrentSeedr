from src.objs import *
from src.functions.convert import convertSize
from src.functions.exceptions import exceptions, noAccount

@bot.message_handler(commands=['files'])
def files(message, userLanguage=None):
    userId = message.from_user.id
    userLanguage = userLanguage or dbSql.getSetting(userId, 'language')
    ac = dbSql.getDefaultAc(userId)

    #! If user has account
    if ac:
        account = Seedr(cookie=ac['cookie'])
        response = account.listContents().json()
        
        if 'result' not in response:
            #! If user has files
            if response['folders']:
                text = ''

                for i in response['folders']:
                    text += f"<b>📂 {i['fullname']}</b>\n\n💾 {convertSize(i['size'])}B, ⏰ {i['last_update']}"
                    text += f"\n\n{language['files'][userLanguage]} /getFiles_{i['id']}\n{language['link'][userLanguage]} /getLink_{i['id']}\n{language['delete'][userLanguage]} /delete_{i['id']}\n\n"

                bot.send_message(message.chat.id, text)
            
            #! If user has no files
            else:
                bot.send_message(message.chat.id, language['noFiles'][userLanguage])
        else:
            exceptions(message, response, userLanguage)
    
    #! If no accounts
    else:
        noAccount(message, userLanguage)