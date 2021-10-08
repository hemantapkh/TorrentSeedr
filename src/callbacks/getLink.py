from src.objs import *
from src.commands.getLink import getLink

@bot.callback_query_handler(func=lambda call: True and call.data[:8] == 'getLink_')
def getLinkCb(call):
    getLink(call, called=True)