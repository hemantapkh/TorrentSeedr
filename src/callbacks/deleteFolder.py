from src.objs import *
from src.commands.deleteFolder import deleteFolder

@bot.callback_query_handler(func=lambda call: True and call.data[:7] == 'delete_')
def deleteFolderCb(call):
    deleteFolder(call, called=True)