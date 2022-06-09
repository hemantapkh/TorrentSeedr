from src.objs import *

from src.functions.bars import progressBar
from src.functions.convert import convertSize
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: View active torrents list
@bot.message_handler(commands=['active'])
def active(message, userLanguage=None, called=None):
    userId = message.from_user.id
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

        response = account.listContents()

        if 'error' not in response:
            if 'torrents' in response:
                #! If user has active torrents
                if response['torrents']:
                    text = ''
                    for i in response['torrents']:
                        text += f"<b>📂 {i['name']}</b>\n\n💾 {convertSize(i['size'])}, ⏰ {i['last_update']}\n\n"
                        text += f"{language['torrentQuality'][userLanguage]} {i['torrent_quality']}\n{language['connectedTo'][userLanguage]} {i['connected_to']}\n{language['downloadingFrom'][userLanguage]} {i['downloading_from']}\n{language['seeders'][userLanguage]} {i['seeders']}\n{language['leechers'][userLanguage]} {i['leechers']}\n{language['uploadingTo'][userLanguage]} {i['uploading_to']}\n"

                        #! Show warnings if any
                        # if i['warnings'] != '[]':
                        #     warnings = i['warnings'].strip('[]').replace('"','').split(',')
                        #     for warning in warnings:
                        #         text += f"\n⚠️ {warning.capitalize()}"

                        text += f"\n{progressBar(i['progress'])}\n\n{language['cancel'][userLanguage]} /cancel_{i['id']}\n\n"

                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text=language['refreshBtn'][userLanguage], callback_data='refreshActive'))

                    if called:
                        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.id, text=text, reply_markup=markup)

                    else:
                        bot.send_message(message.chat.id, text, reply_markup=markup)

                #! If user don't have any active torrents
                else:
                    if called:
                        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.id, text=language['noActiveTorrents'][userLanguage])

                    else:
                        bot.send_message(message.chat.id, language['noActiveTorrents'][userLanguage])

        else:
            exceptions(message, response, ac, userLanguage)

    #! If no accounts
    else:
        noAccount(message, userLanguage)
