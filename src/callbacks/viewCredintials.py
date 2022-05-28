from src.objs import *


@bot.callback_query_handler(func=lambda call: True and call.data[:16] == 'viewCredintials_')
def viewCredintials(call):
    userId = call.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')
    accountId = call.data[16:]
    credintals = dbSql.getAccount(userId, accountId)

    if credintals:
        bot.answer_callback_query(call.id, text=f"{language['credentialsBtn'][userLanguage]}\n\n{language['email'][userLanguage]} {credintals['email']}\n\nPassword: {credintals['password']}", show_alert=True)

    else:
        bot.edit_message_text(language['credentialsNotFound'][userLanguage], chat_id=call.message.chat.id, message_id=call.message.id)