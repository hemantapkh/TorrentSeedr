import json
import requests
import secrets

from src.objs import *
from src.functions.urlEncode import urlEncode
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: Get download link of torrents
@bot.message_handler(func=lambda message: message.text and message.text[:9] == '/getLink_')
def getLink(message, called=False):
    userId = message.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')

    if floodControl(message, userLanguage):
        ac = dbSql.getDefaultAc(userId)

        #! If user has an account
        if ac and ac['cookie']:
            folderId = message.data[8:] if called else message.text[9:]

            data = {
                'folder_id': folderId,
                'archive_arr[0][type]': 'folder',
                'archive_arr[0][id]': folderId,
            }

            cookies = json.loads((ac['cookie']))

            response = requests.put(f'https://www.seedr.cc/download/archive/init/2c94612b-ecc0-41f7-8892-{secrets.token_hex(6)}', cookies=cookies, data=data).json()

            #! If download link found
            if 'url' in response:
                encodedUrl = urlEncode(response['url'])
                text = f"🔗 <code>{encodedUrl}</code>\n\n<b>🔥via @TorrentSeedrBot</b>"

                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text=language['openInBrowserBtn'][userLanguage], url=encodedUrl))
                markup.add(telebot.types.InlineKeyboardButton(text=language['openInPlayerBtn'][userLanguage], callback_data=f'getPlaylist_000_folder_{folderId}'))
                markup.add(telebot.types.InlineKeyboardButton(text=language['showFilesBtn'][userLanguage], callback_data=f'getFiles_{folderId}'), telebot.types.InlineKeyboardButton(text=language['deleteBtn'][userLanguage], callback_data=f'delete_{id}'))
                markup.add(telebot.types.InlineKeyboardButton(text=language['joinChannelBtn'][userLanguage], url='t.me/h9youtube'), telebot.types.InlineKeyboardButton(text=language['joinDiscussionBtn'][userLanguage], url='https://t.me/+mxHaXtNFM1g5MzI1'))

                if called:
                    bot.answer_callback_query(message.id)
                    bot.edit_message_text(text=text, chat_id=message.message.chat.id, message_id=message.message.id, reply_markup=markup)
                else:
                    bot.send_message(text=text, chat_id=message.chat.id, reply_markup=markup)

            else:
                solveCaptcha(message, called)

        elif ac and ac['password']:
            solveCaptcha(message, called)

        elif ac:
            text = 'Due to an error in the seedr API, you need to login to seedr web to get the folder link. Click /password to store your password and try again.'

            if called:
               bot.edit_message_text(text=text, chat_id=message.message.chat.id, message_id=message.message.id) 

            else:
                bot.send_message(text=text, chat_id=message.chat.id)

        #! If no accounts
        else:
            noAccount(message, userLanguage)


def solveCaptcha(message, called):
    text = 'Please solve the captcha by clicking the button below and try again.'

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='✔️ Verify', web_app=telebot.types.WebAppInfo('https://hemantapokharel.com.np/seedr/refresh')))

    if called:
        bot.answer_callback_query(message.id)
        bot.edit_message_text(text=text, chat_id=message.message.chat.id, message_id=message.message.id, reply_markup=markup)

    else:
        bot.send_message(text=text, chat_id=message.chat.id, reply_markup=markup)
