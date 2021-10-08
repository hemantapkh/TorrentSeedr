from src.objs import *
from src.commands.addAccount import addAccount

@bot.callback_query_handler(func=lambda call: True and call.data == 'addAccount')
def addAccountCb(call):
    addAccount(call, called=True)