from src.objs import *
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: View account profile, add new accounts and remove existing accounts
@bot.message_handler(commands=['wishlist'])
def wishlist(message, userLanguage=None):
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

                text = ''

                # Torrent Hunt wishlist
                wishlistItems = dbSql.getWishLists(userId)
                if wishlistItems:
                    for item in wishlistItems:
                        text += f"🌟 <b>{item['title']}</b>\n\nAdd: /addTorrent_1{item['wishlistId']}\nRemove: /removeWL_1{item['wishlistId']}\n\n"

                # Seedr Wishlist
                if response['result'] is True:
                    if response['account']['wishlist']:
                        for wish in response['account']['wishlist']:
                            text += f"⭐ <b>{wish['title']}</b>\n\nAdd: /addTorrent_0{wish['id']}\nRemove: /removeWL_0{wish['id']}\n\n"

                if text:
                    bot.send_message(message.chat.id, text[:4000])

                else:
                    bot.send_message(message.chat.id, language["noWishlist"][userLanguage])

            else:
                exceptions(message, response, ac, userLanguage)

        #! If no accounts
        else:
            noAccount(message, userLanguage)
