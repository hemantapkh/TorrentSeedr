import asyncio

from src.objs import *
from src.commands.addTorrent import addTorrent
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: Get Torrent info from remote source
async def remoteTorrent(message):
    userId = message.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')

    ac = dbSql.getDefaultAc(userId)

    #! If user has an account
    if ac:
        account = Seedr(
            token=ac['token'],
            callbackFunc=lambda token: dbSql.updateAccount(
                token, userId, ac['accountId']
            )
        )

        response = account.scanPage(message.text)

        if 'error' not in response:
            if response['torrents']:
                await asyncio.gather(addTorrent(message, userLanguage, magnetLink=response['torrents'][0]['magnet']))

            else:
                bot.send_message(message.chat.id, language["noTorrentInURL"][userLanguage])

        else:
            exceptions(message, response, ac, userLanguage)

    #! If no accounts
    else:
        noAccount(message, userLanguage)
