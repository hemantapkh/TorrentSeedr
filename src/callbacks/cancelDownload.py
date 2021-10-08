from src.objs import *
from src.commands.cancelDownload import cancelDownload

@bot.callback_query_handler(func=lambda call: True and call.data[:7] == 'cancel_')
def cancelDownloadCb(call):
    cancelDownload(call, called=True)