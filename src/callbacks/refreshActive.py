from src.objs import *
from src.commands.active import active

@bot.callback_query_handler(func=lambda call: True and call.data == 'refreshActive')
def refreshActive(call):
    active(call, called=True)