from src.objs import *
from src.commands.cancel import cancel
from src.functions.floodControl import floodControl
from src.functions.keyboard import cancelReplyKeyboard, mainReplyKeyboard, yesNoReplyKeyboard


#: Login or signup seedr account
@bot.message_handler(commands=['login'])
def login(message, called=False, userLanguage=None):
    userId = message.from_user.id

    if floodControl(message, userLanguage):
        userLanguage = userLanguage or dbSql.getSetting(userId, 'language')

        if called:
            bot.delete_message(message.message.chat.id, message.message.id)

        sent = bot.send_message(message.from_user.id, language['enterEmail'][userLanguage], reply_markup=cancelReplyKeyboard(userLanguage))

        bot.register_next_step_handler(sent, login2, userLanguage)


def login2(message, userLanguage):
    if message.text == language['cancelBtn'][userLanguage]:
        cancel(message, userLanguage)

    else:
        email = message.text

        sent = bot.send_message(message.from_user.id, language['enterPassword'][userLanguage])

        bot.register_next_step_handler(sent, login3, userLanguage, email)

def login3(message, userLanguage, email):
    if message.text == language['cancelBtn'][userLanguage]:
        cancel(message, userLanguage)

    else:
        password = message.text

        sent = bot.send_message(message.from_user.id, language['storePassword?'][userLanguage], reply_markup=yesNoReplyKeyboard(userLanguage))
        bot.register_next_step_handler(sent, login4, userLanguage, email, password)

def login4(message, userLanguage, email, password):
    if message.text == language['cancelBtn'][userLanguage]:
        cancel(message, userLanguage)

    else:
        storePassword = True if message.text == language['yesBtn'][userLanguage] else False

        seedr = Login(email, password)
        response = seedr.authorize()

        if seedr.token:
            ac = Seedr(
                    token = seedr.token,
                    callbackFunc = lambda token: dbSql.updateAccount(
                        token, message.from_user.id, ac['accountId']
                    )
            )
            acSettings = ac.getSettings()

            dbSql.setAccount(
                userId=message.from_user.id,
                accountId=acSettings['account']['user_id'],
                userName=acSettings['account']['username'],
                token=seedr.token,
                isPremium=acSettings['account']['premium'],
                invitesRemaining=acSettings['account']['invites'],
                email=acSettings['account']['email'],
                password=password if storePassword else None
            )

            bot.send_message(message.chat.id, language['loggedInAs'][userLanguage].format(acSettings['account']['username']), reply_markup=mainReplyKeyboard(message.from_user.id, userLanguage))

        elif response['error'] == 'invalid_grant':
            bot.send_message(message.chat.id, language['incorrectPassword'][userLanguage], reply_markup=mainReplyKeyboard(message.from_user.id, userLanguage))

        else:
            bot.send_message(message.chat.id, language['somethingWrong'][userLanguage], mainReplyKeyboard(message.from_user.id, userLanguage))
