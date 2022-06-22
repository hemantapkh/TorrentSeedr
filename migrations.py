import sqlite3
import os, json

config = json.load(open('src/config.json'))
database = config['database']

if os.path.exists(database):
    confirm = input('Database already exists. Do you want to delete it and create a new one? (y/[N]): ')
    if confirm == 'y':
        os.remove(database)
        print('[-] Database already exists. Deleting it.')
    else:
        print('[-] Exiting.')
        exit()

conn = sqlite3.connect(database)
print('[+] Database opened successfully.')

conn.execute('''CREATE TABLE users
         (UserId       INTEGER PRIMARY KEY,
         date          STRING  NOT NULL
         );''')

print('[+] Table users created successfully.')

conn.execute('''CREATE TABLE settings
         (ownerId       INTEGER PRIMARY KEY,
         language       TEXT DEFAULT "english",
         playlist       TEXT DEFAULT "m3u",
         githubId       TEXT DEFAULT 0,
         totalRefer     INTEGER DEFAULT 0,
         defaultAcId    INTEGER
         );''')

print('[+] Table settings created successfully.')

conn.execute('''CREATE TABLE accounts
         (
         id         INTEGER PRIMARY KEY AUTOINCREMENT,
         accountId INTEGER  NOT NULL,
         ownerId    INTEGER NOT NULL,
         userName   TEXT    NOT NULL,
         token      TEXT    NOT NULL,
         email      TEXT,
         password   TEXT,
         cookie     TEXT,
         isPremium    INTEGERL,
         invitesRemaining INTEGER,
         timestamp  INTEGER
         );''')

print('[+] Table accounts created successfully.')

conn.execute('''CREATE TABLE flood
         (ownerId       INTEGER PRIMARY KEY,
         warned         INTEGER DEFAULT 0,
         lastMessage   INTEGER DEFAULT 0,
         blockTill     INTEGER DEFAULT 0
         );''')

print('[+] Table flood created successfully.')
