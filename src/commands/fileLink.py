from src.objs import *
from src.functions.urlEncode import urlEncode
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
            account = Seedr(
                token=ac['token'],
                callbackFunc=lambda token: dbSql.updateAccount(
                    token, userId, ac['accountId']
                )
            )

            sent = bot.send_message(message.chat.id, language['fetchingLink'][userLanguage])
            response = account.fetchFile(id[1:])

            if 'error' not in response:
                #! If download link found
                if 'url' in response:
                    encodedUrl = urlEncode(response['url'])
                    text = f"🖹 <b>{response['name']}</b>\n\n"
                    text += f"🔗 <code>{encodedUrl}</code>\n\n<b>🔥via @TorrentSeedrBot</b>"

                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text=language['openInBrowserBtn'][userLanguage], url=encodedUrl))

                    if id[0] != 'u':
                        markup.add(telebot.types.InlineKeyboardButton(text=language['openInPlayerBtn'][userLanguage], callback_data=f'getPlaylist_000_file_{id[1:]}'))

                    markup.add(telebot.types.InlineKeyboardButton(text=language['joinChannelBtn'][userLanguage], url='t.me/h9youtube'), telebot.types.InlineKeyboardButton(text=language['joinDiscussionBtn'][userLanguage], url='https://t.me/+mxHaXtNFM1g5MzI1'))

                    bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=sent.id, reply_markup=markup)

            else:
                exceptions(message, response, ac, userLanguage)

        #! If no accounts
        else:
            noAccount(message, userLanguage)
