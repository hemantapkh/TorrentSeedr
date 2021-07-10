from src.objs import *
from src.functions.keyboard import mainReplyKeyboard

@bot.callback_query_handler(func=lambda call: True and call.data[:14] == 'removeAccount_')
def removeAccount(call):
    userId = call.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')
    accountId = call.data[14:]

    dbSql.deleteAccount(userId, accountId)

    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    bot.send_message(text=language['accountRemoved'][userLanguage], chat_id=call.message.chat.id, reply_markup=mainReplyKeyboard(userId, userLanguage))