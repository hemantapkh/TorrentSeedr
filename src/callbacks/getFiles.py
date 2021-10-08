from src.objs import *
from src.commands.getFiles import getFiles

@bot.callback_query_handler(func=lambda call: True and call.data[:9] == 'getFiles_')
def getFilesCb(call):
    getFiles(call, called=True)