from src.objs import *
from src.commands.authorize import authorize
from src.functions.keyboard import mainReplyKeyboard


@bot.callback_query_handler(func=lambda call: True and call.data == 'authorize')
def authorizeCb(call):
    authorize(call, called=True)


@bot.callback_query_handler(func=lambda call: True and call.data[:10] == 'Authorize_')
def Authorize(call, accountId=None, deviceCode=None, userLanguage=None):
    userLanguage = userLanguage or dbSql.getSetting(call.from_user.id, 'language')
    deviceCode = deviceCode or call.data[10:]

    seedr = Login()
    response = seedr.authorize(deviceCode)

    if seedr.token:
        ac = Seedr(
                token = seedr.token,
                callbackFunc = lambda token: dbSql.updateAccount(
                    token, call.from_user.id, ac['accountId']
                )
        )
        acSettings = ac.getSettings()

        dbSql.setAccount(
            userId=call.from_user.id,
            accountId=acSettings['account']['user_id'],
            userName=acSettings['account']['username'],
            token=seedr.token,
            isPremium=acSettings['account']['premium'],
            invitesRemaining=acSettings['account']['invites'],
            email=acSettings['account']['email']
        )


        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, language['loggedInAs'][userLanguage].format(acSettings['account']['username']), reply_markup=mainReplyKeyboard(call.from_user.id, userLanguage))

    else:
        bot.answer_callback_query(call.id, language['notAuthorized'][userLanguage], show_alert=True)