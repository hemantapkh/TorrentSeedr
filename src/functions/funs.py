from src.objs import *
from src.functions.keyboard import notSubscribedMarkup


# Check if the user is subscribed or not, returns True if subscribed
def isSubscribed(message, userLanguage=None, sendMessage=True):
    telegramId = message.from_user.id
    subscribed = True

    try:
        status = bot.get_chat_member('-1001270853324', telegramId)
        if status.status == 'left':
            subscribed = False
        else:
            return True

    except Exception:
        subscribed = True

    if not subscribed:
        # Send the links if sendMessage is True
        if sendMessage:
            bot.send_message(message.chat.id, text=language['notSubscribed'][userLanguage], reply_markup=notSubscribedMarkup(userLanguage))
        
        return False
