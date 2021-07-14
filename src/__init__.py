from src.objs import config, dbSql
from src.objs import bot, language

from src.commands.start import start
from src.commands.files import files
from src.commands.active import active
from src.commands.switch import switch
from src.commands.account import account
from src.commands.getLink import getLink
from src.commands.fileLink import fileLink
from src.commands.getFiles import getFiles
from src.commands.broadcast import broadcast
from src.commands.addAccount import addAccount
from src.commands.addTorrent import addTorrent
from src.commands.removeFile import removeFile
from src.commands.deleteFolder import deleteFolder
from src.commands.cancelDownload import cancelDownload


from src.callbacks.getPlaylist import getPlaylist
from src.callbacks.removeAccount import removeAccount
from src.callbacks.viewCredintials import viewCredintials