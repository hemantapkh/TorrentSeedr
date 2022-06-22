from src.objs import config, dbSql
from src.objs import bot, language

from src.commands.start import start
from src.commands.login import login
from src.commands.stats import stats
from src.commands.files import files
from src.commands.token import token
from src.commands.cancel import cancel
from src.commands.active import active
from src.commands.switch import switch
from src.commands.account import account
from src.commands.support import support
from src.commands.getLink import getLink
from src.commands.password import password
from src.commands.fileLink import fileLink
from src.commands.getFiles import getFiles
from src.commands.wishlist import wishlist
from src.commands.authorize import authorize
from src.commands.broadcast import broadcast
from src.commands.addAccount import addAccount
from src.commands.addTorrent import addTorrent
from src.commands.removeFile import removeFile
from src.commands.deleteFolder import deleteFolder
from src.commands.remoteTorrent import remoteTorrent
from src.commands.cancelDownload import cancelDownload
from src.commands.removeWishlist import removeWishlist

from src.callbacks.login import login
from src.callbacks.getLink import getLink
from src.callbacks.getFiles import getFiles
from src.callbacks.authorize import authorize
from src.callbacks.addAccount import addAccount
from src.callbacks.getPlaylist import getPlaylist
from src.callbacks.deleteFolder import deleteFolder
from src.callbacks.refreshActive import refreshActive
from src.callbacks.removeAccount import removeAccount
from src.callbacks.cancelDownload import cancelDownload
from src.callbacks.viewCredintials import viewCredintials

from src.functions.keyboard import githubAuthKeyboard
from src.commands.addTorrent import invalidMagnet