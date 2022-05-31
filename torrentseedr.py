import ssl
import requests

import validators
import telebot, asyncio
from aiohttp import web

from src import *

#: Configuration for webhook
webhookBaseUrl = f"https://{config['webhookOptions']['webhookHost']}:{config['webhookOptions']['webhookPort']}"
webhookUrlPath = f"/{config['botToken']}/"

app = web.Application()


#: Process webhook calls
async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

app.router.add_post('/{token}/', handle)

async def text(message):
    userLanguage = dbSql.getSetting(message.from_user.id, 'language')

    #! Add accounts
    if message.text == language['addAccountBtn'][userLanguage]:
        addAccount(message, called=False, userLanguage=userLanguage)

    #! File manager
    elif message.text == language['fileManagerBtn'][userLanguage]:
        files(message, userLanguage)

    #! Active torrents
    elif message.text == language['activeTorrentsBtn'][userLanguage]:
        active(message, userLanguage)

    #! Switch accounts
    elif message.text == language['switchBtn'][userLanguage]:
        switch(message, userLanguage)

    #! Wishlist
    elif message.text == language['wishlistBtn'][userLanguage]:
        wishlist(message, userLanguage)

    #! Account and profile
    elif message.text == language['accountBtn'][userLanguage]:
        account(message, userLanguage)

    #! Earn free space
    elif message.text == '🆓 Get free space':
        bot.send_message(message.chat.id, language['getFreeSpace'][userLanguage], reply_markup=githubAuthKeyboard(userLanguage))

    #! Support
    elif message.text == language['supportBtn'][userLanguage]:
        support(message, userLanguage)

    #! Cancel process
    elif message.text == language['cancelBtn'][userLanguage]:
        cancel(message, userLanguage)

    #! Adding torrent from wishlist
    elif message.text.startswith('/addTorrent'):
        wishlistId = message.text[13:]
        wishlistType = message.text[12]

        if wishlistType == '0':
            await asyncio.gather(addTorrent(message, userLanguage, wishlistId=wishlistId))

        else:
            magnetLink = dbSql.getWishList(message.from_user.id, wishlistId)

            if magnetLink:
                await asyncio.gather(addTorrent(message, userLanguage, magnetLink=magnetLink))

            else:
                bot.send_message(message.chat.id, language['wishlistNotFound'][userLanguage])

    #! Adding torrent from remote URL
    elif validators.url(message.text):
        await remoteTorrent(message)

    #! Adding torrents via magnet link
    elif 'magnet:?' in message.text:
        await asyncio.gather(addTorrent(message, userLanguage, magnetLink=message.text))

    else:
        invalidMagnet(message, userLanguage)


#: Text handler
@bot.message_handler(content_types=['text'])
def _text(message):
    asyncio.run(text(message))


#: Adding torrent from files
async def document(message):
    userLanguage = dbSql.getSetting(message.from_user.id, 'language')

    if message.document.mime_type == 'application/x-bittorrent':
        fileInfo = bot.get_file(message.document.file_id)
        torrentUrl = f'https://api.telegram.org/file/bot{bot.token}/{fileInfo.file_path}'

        await asyncio.gather(addTorrent(message, userLanguage, torrentFile=torrentUrl))

    else:
        bot.send_message(message.chat.id, language['wrongTorrentFile'][userLanguage])


@bot.message_handler(content_types=['document'])
def _document(message):
    asyncio.run(document(message))


#: Polling Bot
if config['connectionType'] == 'polling':
    #! Remove previous webhook if exists
    bot.remove_webhook()
    bot.polling(none_stop=True)

#: Webhook Bot
elif config['connectionType'] == 'webhook':
    #! Set webhook
    bot.set_webhook(url=webhookBaseUrl + webhookUrlPath,
                    certificate=open(config['webhookOptions']['sslCertificate'], 'r'))

    #! Build ssl context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(config['webhookOptions']['sslCertificate'], config['webhookOptions']['sslPrivatekey'])

    #! Start aiohttp server
    web.run_app(
        app,
        host=config['webhookOptions']['webhookListen'],
        port=config['webhookOptions']['webhookPort'],
        ssl_context=context,
    )
