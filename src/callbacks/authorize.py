from src.objs import *
from src.functions.keyboard import mainReplyKeyboard

@bot.callback_query_handler(func=lambda call: True and call.data[:10] == 'authorize_')
def authorize(call, accountId=None, deviceCode=None, userLanguage=None, refreshMode=False):
    userLanguage = userLanguage or dbSql.getSetting(call.from_user.id, 'language')
    deviceCode = deviceCode or call.data[10:]
    
    response = getToken(deviceCode)

    if 'access_token' in response:
        ac = Seedr(response['access_token'])
        acSettings = ac.getSettings().json()
        
        dbSql.setAccount(userId=call.from_user.id, accountId=acSettings['account']['user_id'], userName=acSettings['account']['username'], token=response['access_token'], deviceCode=deviceCode, isPremium=acSettings['account']['premium'], invitesRemaining=acSettings['account']['invites'])
        
        if refreshMode:
            bot.send_message(call.from_user.id, language['refreshed'][userLanguage])
        
        else:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, language['loggedInAs'][userLanguage].format(acSettings['account']['username']), reply_markup=mainReplyKeyboard(call.from_user.id, userLanguage))

    else:
        if refreshMode:
            dbSql.deleteAccount(call.from_user.id, accountId)
            bot.send_message(call.from_user.id, language['tokenExpired'][userLanguage], reply_markup=mainReplyKeyboard(userId=call.from_user.id, userLanguage=userLanguage))

        else:
            bot.answer_callback_query(call.id, language['notAuthorized'][userLanguage], show_alert=True)