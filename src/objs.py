import json
from os import path

import telebot

from models import dbQuery
from seedr import Seedr, Account

#! Finding the absolute path of the config file
scriptPath = path.abspath(__file__)
dirPath = path.dirname(scriptPath)
configPath = path.join(dirPath,'config.json')

seedrAc = Account()
config = json.load(open(configPath))
language = json.load(open(config['language']))
dbSql = dbQuery(config['database'])
bot = telebot.TeleBot(config['botToken'], parse_mode='HTML')