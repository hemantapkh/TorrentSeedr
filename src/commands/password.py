import requests

from src.objs import *
from src.commands.cancel import cancel
from src.functions.floodControl import floodControl
from src.functions.keyboard import cancelReplyKeyboard, mainReplyKeyboard

@bot.message_handler(commands=['password'])
def password(message):
    userId = message.from_user.id

    ac = dbSql.getDefaultAc(userId)

    if ac:
        userLanguage = dbSql.getSetting(userId, 'language')

        sent = bot.send_message(message.from_user.id, language['enterPasswordFor'][userLanguage].format(ac['email']), reply_markup=cancelReplyKeyboard(userLanguage))

        bot.register_next_step_handler(sent, password1, userLanguage, ac['accountId'])

    else:
        bot.send_message(message.chat.id, 'Please use /add to login your account first.')

def password1(message, userLanguage, accountId):
    if message.text == language['cancelBtn'][userLanguage]:
        cancel(message, userLanguage)

    else:
        password = message.text
        dbSql.updateAcColumn(message.from_user.id, accountId, 'password', password)
        bot.send_message(message.chat.id, '🔑 Account password stored successfully in the database.', reply_markup=mainReplyKeyboard(message.from_user.id, userLanguage))
