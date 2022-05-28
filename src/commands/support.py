from src.objs import *


#: Support menu
@bot.message_handler(commands=['support'])
def support(message, userLanguage=None):
    userLanguage = userLanguage or dbSql.getSetting(message.chat.id, 'language')

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text=language['joinChannelBtn'][userLanguage], url='t.me/h9youtube'), telebot.types.InlineKeyboardButton(text=language['joinDiscussionBtn'][userLanguage], url='https://t.me/+mxHaXtNFM1g5MzI1'))
    markup.add(telebot.types.InlineKeyboardButton(text=language['subscribeChannelBtn'][userLanguage], url='https://youtube.com/h9youtube'), telebot.types.InlineKeyboardButton(text=language['followOnGithubBtn'][userLanguage], url='https://github.com/hemantapkh'))
    markup.add(telebot.types.InlineKeyboardButton(text=language['donateBtn'][userLanguage], url=f"https://buymeacoffee.com/hemantapkh"))

    bot.send_message(message.chat.id, language['support'][userLanguage].format(language['supportBtn'][userLanguage]), reply_markup=markup, disable_web_page_preview=True)
