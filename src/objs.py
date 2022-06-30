import json
from os import path

import telebot

from models import dbQuery
from seedrcc import Login, Seedr

config = json.load(open('src/config.json'))
language = json.load(open(config['language']))
dbSql = dbQuery(config['database'], config['magnetDatabase'])
bot = telebot.TeleBot(config['botToken'], parse_mode='HTML')
botUsername = bot.get_me().username