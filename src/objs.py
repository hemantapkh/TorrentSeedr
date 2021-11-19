import json
from os import path

import telebot

from models import dbQuery
from seedr import *

config = json.load(open('src/config.json'))
language = json.load(open(config['language']))
dbSql = dbQuery(config['database'], config['magnetDatabase'])
bot = telebot.TeleBot(config['botToken'], parse_mode='HTML')
bot.worker_pool = telebot.util.ThreadPool(num_threads=4)