import ssl
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
        addAccount(message, userLanguage)
    
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
        featureUnavailable(message, userLanguage)
    
    #! Account and profile
    elif message.text == language['accountBtn'][userLanguage]:
        account(message, userLanguage)
    
    #! Settings
    elif message.text == language['settingsBtn'][userLanguage]:
        featureUnavailable(message, userLanguage)
    
    #! Help
    elif message.text == language['helpBtn'][userLanguage]:
        featureUnavailable(message, userLanguage)

    #! Support
    elif message.text == language['supportBtn'][userLanguage]:
        featureUnavailable(message, userLanguage)
    
    #! Adding torrents
    else:
        #addTorrent(message, userLanguage)
        #asyncio.run(addTorrent(message, userLanguage))
        await asyncio.gather(addTorrent(message, userLanguage))

#: Text handler
@bot.message_handler(content_types=['text'])
def _text(message):
    asyncio.run(text(message))
    
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