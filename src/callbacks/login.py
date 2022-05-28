from src.objs import *
from src.commands.login import login


@bot.callback_query_handler(func=lambda call: True and call.data == 'login')
def loginCb(call):
    login(call, called=True)