from src.objs import *
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: Remove wishlist item
@bot.message_handler(func=lambda message: message.text and message.text.startswith('/removeWL_'))
def removeWishlist(message, userLanguage=None):
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

            wishlistId = message.text[11:]
            wishlistType = message.text[10]

            if wishlistType == '0':
                response = account.deleteWishlist(wishlistId)

                if 'error' not in response:
                    #! If wishlist is deleted successfully
                    if response['result'] == True:
                        bot.send_message(message.chat.id, language['deletedSuccessfully'][userLanguage])

                else:
                    exceptions(message, response, ac, userLanguage)

            else:
                dbSql.removeWishList(message.from_user.id, wishlistId)
                bot.send_message(message.chat.id, language['deletedSuccessfully'][userLanguage])

        #! If no accounts
        else:
            noAccount(message, userLanguage)
