from src.objs import *
from src.functions.bars import spaceBar
from src.functions.convert import convertSize
from src.functions.exceptions import exceptions, noAccount

#: View account profile, add new accounts and remove existing accounts
@bot.message_handler(commands=['account'])
def account(message, userLanguage=None):
    userId = message.from_user.id
    userLanguage = userLanguage or dbSql.getSetting(userId, 'language')
    ac = dbSql.getDefaultAc(userId)

    #! If user has account
    if ac:
        account = Seedr(cookie=ac['cookie'])
        response = account.getSettings().json()

        #!? On success
        if response['result'] == True:
            text = f"<b>{language['accountBtn'][userLanguage]}</b>\n\n{language['username'][userLanguage]} {response['account']['username']}\n{language['email'][userLanguage]} {response['account']['email']}\n{language['totalBandwidthUsed'][userLanguage]} {convertSize(response['account']['bandwidth_used'])}\n{language['country'][userLanguage]} {response['country']}\n"
            text += f"{language['inviteLink'][userLanguage]} https://www.seedr.cc/?r={response['account']['user_id']} \n{language['inviteRemaining'][userLanguage]} {response['account']['invites']} / {response['account']['max_invites']}\n{language['inviteAccepted'][userLanguage]} {response['account']['invites_accepted']}"
            
            text += f"\n\n{convertSize(response['account']['space_used'])} / {convertSize(response['account']['space_max'])}"
            text += f"\n{spaceBar(totalSpace=response['account']['space_max'], spaceUsed=response['account']['space_used'])}"
            
            bot.send_message(message.chat.id, text, disable_web_page_preview=True)
                
        else:
            exceptions(message, response, userLanguage)
    
    #! If no accounts
    else:
        noAccount(message, userLanguage)