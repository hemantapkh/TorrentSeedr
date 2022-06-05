from src.objs import *
from src.functions.floodControl import floodControl
from src.functions.convert import convertSize
from src.functions.exceptions import exceptions, noAccount

#: File manager
@bot.message_handler(commands=['files'])
def files(message, userLanguage=None):
    userId = message.from_user.id
    userLanguage = userLanguage or dbSql.getSetting(userId, 'language')

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

            response = account.listContents()

            if 'error' not in response:
                #! If user has files
                if response['folders']:
                    text = ''

                    for i in response['folders']:
                        text += f"<b>📂 {i['fullname']}</b>\n\n💾 {convertSize(i['size'])}B, ⏰ {i['last_update']}"
                        text += f"\n\n{language['files'][userLanguage]} /getFiles_{i['id']}\n{language['link'][userLanguage]} /getLink_{i['id']}\n{language['delete'][userLanguage]} /delete_{i['id']}\n\n"

                    bot.send_message(message.chat.id, text[:4000])

                #! If user has no files
                else:
                    bot.send_message(message.chat.id, language['noFiles'][userLanguage])
            else:
                exceptions(message, response, ac, userLanguage)

        #! If no accounts
        else:
            noAccount(message, userLanguage)
