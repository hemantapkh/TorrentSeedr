from src.objs import *
from src.functions.bars import spaceBar
from src.functions.convert import convertSize
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: View account profile, add new accounts and remove existing accounts
@bot.message_handler(commands=['account'])
def account(message, userLanguage=None):
    userId = message.from_user.id

    if floodControl(message, userLanguage):
        userLanguage = userLanguage or dbSql.getSetting(userId, 'language')
        ac = dbSql.getDefaultAc(userId)

        #! If user has an account
        if ac:
            account = Seedr(
                token=ac['token'],
                callbackFunc=lambda token: dbSql.updateAccount(
                    token, userId, ac['accountId']
                )
            )

            response = account.getSettings()

            #! On success
            if 'error' not in response:
                if response['result'] == True:
                    text = f"<b>{language['accountBtn'][userLanguage]}</b>\n\n{language['username'][userLanguage]} {response['account']['username']}\n{language['totalBandwidthUsed'][userLanguage]} {convertSize(response['account']['bandwidth_used'])}\n{language['country'][userLanguage]} {response['country']}\n"
                    text += f"{language['inviteLink'][userLanguage]} seedr.cc/?r={response['account']['user_id']} \n{language['inviteRemaining'][userLanguage]} {response['account']['invites']} / {response['account']['max_invites']}\n{language['inviteAccepted'][userLanguage]} {response['account']['invites_accepted']} / {dbSql.getSetting(userId, 'totalRefer')}"

                    text += f"\n\n{convertSize(response['account']['space_used'])} / {convertSize(response['account']['space_max'])}"
                    text += f"\n{spaceBar(totalSpace=response['account']['space_max'], spaceUsed=response['account']['space_used'])}"

                    markup = telebot.types.InlineKeyboardMarkup()

                    #markup.add(telebot.types.InlineKeyboardButton(text=language['credentialsBtn'][userLanguage], callback_data=f"viewCredintials_{ac['id']}"))
                    markup.add(telebot.types.InlineKeyboardButton(text=language['removeAccountBtn'][userLanguage], callback_data=f"removeAccount_{ac['id']}"))
                    markup.add(telebot.types.InlineKeyboardButton(text=language['addAccountBtn'][userLanguage], callback_data='addAccount'))

                    bot.send_message(message.chat.id, text, disable_web_page_preview=True, reply_markup=markup)

            else:
                exceptions(message, response, ac, userLanguage)

        #! If no accounts
        else:
            noAccount(message, userLanguage)
