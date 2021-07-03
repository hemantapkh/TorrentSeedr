from src.objs import *

from src.functions.bars import progressBar
from src.functions.convert import convertSize
from src.functions.exceptions import exceptions, noAccount

# Active torrents list
@bot.message_handler(commands=['active'])
def active(message, userLanguage=None):
    userId = message.from_user.id
    userLanguage = userLanguage or dbSql.getSetting(userId, 'language')
    ac = dbSql.getDefaultAc(userId)

    #! If user has account
    if ac:
        account = Seedr(cookie=ac['cookie'])
        response = account.listContents().json()

        if 'torrents' in response:
            #!? User has active torrents
            if response['torrents']:
                text = ''
                for i in response['torrents']:
                    text += f"<b>📂 {i['name']}</b>\n\n💾 {convertSize(i['size'])}, ⏰ {i['last_update']}\n\n"
                    text += f"{language['torrentQuality'][userLanguage]} {i['torrent_quality']}\n{language['connectedTo'][userLanguage]} {i['connected_to']}\n{language['downloadingFrom'][userLanguage]} {i['downloading_from']}\n{language['seeders'][userLanguage]} {i['seeders']}\n{language['leechers'][userLanguage]} {i['leechers']}\n{language['uploadingTo'][userLanguage]} {i['uploading_to']}\n"
                
                    #! Show warnings
                    if i['warnings'] != '[]':
                        warnings = i['warnings'].strip('[]').replace('"','').split(',')
                        for warning in warnings:
                            text += f"\n⚠️ {warning.capitalize()}"
                    
                    text += f"\n{progressBar(i['progress'])}\n\nCancel: /cancel_{i['id']}\n\n"

                bot.send_message(message.chat.id, text)
    
            #!? User don't have any active torrents
            else:
                bot.send_message(message.chat.id, language['noActiveTorrents'][userLanguage])
        
        else:
            exceptions(message, response, userLanguage)
    
    #! If no accounts
    else:
        noAccount(message, userLanguage)