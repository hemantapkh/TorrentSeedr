from src.objs import *
from src.functions.keyboard import mainReplyKeyboard

def exceptions(message, response, userLanguage, called=False):
    chatId = message.message.chat.id if called else message.chat.id
    if 'result' in response:
        if response['result'] == 'login_required':
            markup = telebot.types.InlineKeyboardMarkup()
            ac = dbSql.getDefaultAc(message.from_user.id)

            markup.add(telebot.types.InlineKeyboardButton(text=language['loginBtn'][userLanguage], url='https://torrentseedrbot.herokuapp.com/login'), telebot.types.InlineKeyboardButton(text=language['signupBtn'][userLanguage], url='https://www.seedr.cc/?r=921385'))
            markup.add(telebot.types.InlineKeyboardButton(text=language['removeAccountBtn'][userLanguage], callback_data=f"removeAccount_{ac['id']}"))
            markup.add(telebot.types.InlineKeyboardButton(text=language['refreshBtn'][userLanguage], url='https://torrentseedrbot.herokuapp.com/refresh'))
            
            bot.send_message(chatId, language['loginRequired'][userLanguage].format(ac['userName']), reply_markup=markup)
    
    else:
        print(response)

def noAccount(message, userLanguage, called=False):
    chatId = message.message.chat.id if called else message.chat.id
    bot.send_message(chatId, language['noAccount'][userLanguage], reply_markup=mainReplyKeyboard(userId=message.from_user.id, userLanguage=userLanguage))