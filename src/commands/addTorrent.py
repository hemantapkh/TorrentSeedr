import requests
from time import time
import base64, asyncio

from src.objs import *
from src.commands.active import active
from src.functions.bars import progressBar
from src.functions.floodControl import floodControl
from src.functions.convert import convertSize, convertTime
from src.functions.exceptions import exceptions, noAccount


#: Add torrent into the user's account
async def addTorrent(message, userLanguage, magnetLink=None, torrentFile=None, wishlistId=None, messageId=None):
    userId = message.from_user.id

    if floodControl(message, userLanguage):
        ac = dbSql.getDefaultAc(userId)

        #! If user has an account
        if ac:
            #!? If torrent is added via start paramater
            if messageId:
                sent = bot.edit_message_text(text=language['collectingInfo'][userLanguage], chat_id=message.chat.id, message_id=messageId)

            else:
                sent = bot.send_message(message.chat.id, language['collectingInfo'][userLanguage])

            account = Seedr(
                token=ac['token'],
                callbackFunc=lambda token: dbSql.updateAccount(
                    token, userId, ac['accountId']
                )
            )

            response = account.addTorrent(
                magnetLink=magnetLink,
                torrentFile=torrentFile,
                wishlistId=wishlistId
            )

            if 'result' in response:
                #! If torrent added successfully
                if 'user_torrent_id' in response:
                    bot.delete_message(message.chat.id, sent.id)
                    active(message, userLanguage)

                #! If no enough space
                elif response['result'] in ['not_enough_space_added_to_wishlist', 'not_enough_space_wishlist_full']:
                    bot.edit_message_text(chat_id=message.chat.id, message_id=sent.id, text=language['noEnoughSpace'][userLanguage])

                #! Invalid magnet link
                elif response['result'] == 'parsing_error':
                    invalidMagnet(message, userLanguage, sent.id)

                #! If parallel downloads exceeds
                elif response['result'] == 'queue_full_added_to_wishlist':
                    bot.edit_message_text(chat_id=message.chat.id, message_id=sent.id, text=language['parallelDownloadExceed'][userLanguage])

                #! If the torrent is already downloading
                elif response == {'result': True}:
                    bot.edit_message_text(chat_id=message.chat.id, message_id=sent.id, text=language['alreadyDownloading'][userLanguage])

                #! If no torrent is passed
                elif 'error' in response and response['error'] == 'no_torrent_passed':
                    invalidMagnet(message, userLanguage, sent.id)

                else:
                    bot.edit_message_text(chat_id=message.chat.id, message_id=sent.id, text=language['unknownError'][userLanguage])

            else:
                exceptions(message, response, ac, userLanguage)

        #! If no accounts
        else:
            noAccount(message, userLanguage)

def invalidMagnet(message, userLanguage, message_id=None):
    markup = telebot.types.InlineKeyboardMarkup()

    url = f'https://t.me/torrenthuntbot?start={botUsername}'

    if not message_id:
        params = '_' + base64.b64encode(message.text.encode('utf-8')).decode('utf-8')

        if len(params)+len(botUsername) <= 64:
            url = url + params

    markup.add(telebot.types.InlineKeyboardButton('Torrent Hunt 🔎', url))

    #! If message_id, edit the message
    if message_id:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text=language['invalidMagnet'][userLanguage], reply_markup=markup)

    #! Else, send a new message
    else:
        bot.send_message(chat_id=message.chat.id, text=language['invalidMagnet'][userLanguage], reply_markup=markup)
