import sqlite3
from time import time
from datetime import datetime


class dbQuery():
    def __init__(self, db, mdb):
        self.db = db
        self.mdb = mdb

    #: Add the user into the database if not registered
    def setUser(self, userId):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        isRegistered = cur.execute(f'SELECT * FROM users WHERE userId=?', (userId,)).fetchone()
        con.commit()

        isRegistered = True if isRegistered else False

        if not isRegistered:
            cur.execute('Insert into users (userId, date) values (?, ?)', (userId, datetime.today().strftime('%Y-%m-%d')))
            cur.execute('Insert into settings (ownerId) values (?)', (userId,))
            cur.execute('Insert into flood (ownerId) values (?)', (userId,))
            con.commit()

        return isRegistered

    #: Get all the registered users
    def getAllUsers(self):
        con = sqlite3.connect(self.db)
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()

        users = cur.execute(f'SELECT userId FROM users').fetchall()
        con.commit()

        return users if users else None

    #: Get all user's with GitHub oauth
    def getAllGhUsers(self):
        con = sqlite3.connect(self.db)
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()

        users = cur.execute(f'SELECT DISTINCT settings.ownerId FROM settings INNER JOIN accounts ON accounts.id = settings.defaultAcId WHERE githubId != 0 and accounts.invitesRemaining != 0').fetchall()
        con.commit()

        return users if users else None

    #: Get all the users with date
    def getAllUsersDate(self):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        users = cur.execute(f'SELECT * FROM users').fetchall()
        con.commit()

        return users if users else None

    #: Get users of particular language
    def getUsers(self, language):
        con = sqlite3.connect(self.db)
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()

        users = cur.execute(f'SELECT ownerId FROM settings WHERE language=?', (language,)).fetchall()
        con.commit()

        return users if users else None

    #: Get all users exclude certain languages
    #: languages must be of list type
    def getUsersExcept(self, languages):
        con = sqlite3.connect(self.db)
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()

        users = cur.execute(f'SELECT * FROM users WHERE userId NOT NULL').fetchall()
        con.commit()

        for language in languages:
            users = [item for item in users if item not in self.getUsers(language)] if self.getUsers(language) else users

        return users if users else None

    #: Get the user's settings
    def getSetting(self, userId, var, table='settings'):
        self.setUser(userId)
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        setting = cur.execute(f'SELECT {var} FROM {table} WHERE ownerId=?', (userId,)).fetchone()
        con.commit()

        return setting[0] if setting else None

    #: Set the user's settings
    def setSetting(self, userId, var, value, table='settings'):
        self.setUser(userId)
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        cur.execute(f'INSERT OR IGNORE INTO {table} (ownerId, {var}) VALUES (?, ?)', (userId, value))
        cur.execute(f'UPDATE {table} SET {var}=? WHERE ownerId=?' , (value, userId))
        con.commit()

    #: Add account in the user's accounts table
    def setAccount(self, userId, accountId, userName, token, isPremium, invitesRemaining, email=None, password=None):
        self.setUser(userId)
        con = sqlite3.connect(self.db)
        cursor = con.cursor()

        #!? If the seedrId not on the table, insert new
        if cursor.execute(f'SELECT * FROM accounts WHERE ownerId=? AND accountId=?', (userId, accountId)).fetchone() == None:
            id = cursor.execute('INSERT INTO accounts (accountId, ownerId, userName, token, email, password, isPremium, invitesRemaining, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',(accountId, userId, userName , token, email, password, isPremium, invitesRemaining, int(time()))).lastrowid
            con.commit()

        #!? If the accountId is already on the table, update the token
        else:
            cursor.execute('UPDATE accounts SET token=?, email=?, password=?, isPremium=?, invitesRemaining=?, timestamp=? WHERE ownerId=? AND accountId=?', (token, email, password, isPremium, invitesRemaining, int(time()), userId, accountId))
            id = cursor.execute('SELECT id FROM accounts WHERE ownerID=? AND accountId=?', (userId, accountId)).fetchone()[0]
            con.commit()

        #!? Set the added account as the default account
        self.setDefaultAc(userId, id)

    #: Update the account's token
    def updateAccount(self, token, userId, accountId):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        cur.execute(f'UPDATE accounts SET token=? WHERE ownerId=? AND accountId=?', (token, userId, accountId))
        con.commit()

    #: Update certain column of accounts
    def updateAcColumn(self, userId, accountId, variable, value):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        cur.execute(f'UPDATE accounts SET {variable}=? WHERE ownerId=? AND accountId=?', (value, userId, accountId ))
        con.commit()

    #: Delete a user's account
    def deleteAccount(self, userId, accountId):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        defaultAcId = self.getSetting(userId, 'defaultAcId')
        cur.execute('DELETE FROM accounts WHERE ownerId=? AND id=?' , (userId, accountId))
        con.commit()

        #!? If the deleted account is the default account, set another account as a default account
        if str(accountId) == str(defaultAcId):
            accounts = self.getAccounts(userId)

            #!? If any accounts is left, make the last account as a default account. Else, make default account empty.
            if accounts:
                lastAccountId = accounts[-1]['id']
                self.setSetting(userId, 'defaultAcId', lastAccountId)

            #!? If no account left, make the default account NULL
            else:
                self.setSetting(userId, 'defaultAcId', None)

    #: Gel all accounts of certain user
    def getAccounts(self, userId):
        con = sqlite3.connect(self.db)
        con.row_factory = dict_factory
        cur = con.cursor()
        accounts = cur.execute('SELECT * FROM accounts WHERE ownerId=?', (userId,)).fetchall()
        con.commit()

        return accounts if accounts else None

    #: Gel certain account of a user
    def getAccount(self, userId, accountId):
        con = sqlite3.connect(self.db)
        con.row_factory = dict_factory
        cur = con.cursor()
        accounts = cur.execute('SELECT * FROM accounts WHERE ownerId=? and id=?', (userId, accountId)).fetchone()
        con.commit()

        return accounts if accounts else None

    #: Get the default account of the user
    def getDefaultAc(self, userId):
        con = sqlite3.connect(self.db)
        con.row_factory = dict_factory
        cur = con.cursor()
        defaultAcId = self.getSetting(userId, 'defaultAcId')

        #!? If defaultAcId, return the account
        if defaultAcId:
            account = cur.execute('SELECT * FROM accounts WHERE ownerId=? AND id=?', (userId, defaultAcId)).fetchone()
            con.commit()

            return account
        else:
            return None

    #: Set a user's default account
    def setDefaultAc(self, userId, accountId):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute('INSERT OR IGNORE INTO settings (ownerId, defaultAcId) VALUES (?, ?)', (userId, accountId))
        cur.execute('UPDATE settings SET defaultAcId=? WHERE ownerId=?', (accountId, userId))
        con.commit()


    #: Get the magnet link from the database
    def getMagnet(self, key):
        con = sqlite3.connect(self.mdb)
        cur = con.cursor()

        magnetLink = cur.execute('SELECT magnetLink FROM data WHERE hash=?', (key,)).fetchone()
        con.commit()

        return magnetLink[0] if magnetLink else None

    #: Get the wish list from the database
    def getWishList(self, userId, wishlistId):
        con = sqlite3.connect(self.mdb)
        cur = con.cursor()

        magnetKey = cur.execute('SELECT hash FROM wishlist WHERE ownerId=? AND wishlistId=?', (userId, wishlistId)).fetchone()
        con.commit()

        if magnetKey:
            magnetLink = self.getMagnet(magnetKey[0])
            return magnetLink if magnetLink else None

    #: Get all wish list from the database
    def getWishLists(self, userId):
        con = sqlite3.connect(self.mdb)
        con.row_factory = dict_factory
        cur = con.cursor()

        wishlists = cur.execute('SELECT wishlistId, data.title FROM wishlist INNER JOIN data on wishlist.hash=data.hash WHERE ownerId=?', (userId,)).fetchall()
        con.commit()

        return wishlists

    #: Remove wishlist from the database
    def removeWishList(self, userId, wishlistId):
        con = sqlite3.connect(self.mdb)
        cur = con.cursor()

        cur.execute(f'DELETE FROM wishlist WHERE ownerId=? AND wishlistId=?', (userId, wishlistId))
        con.commit()

#: Return query as dictionary
#! https://stackoverflow.com/a/3300514/13987868
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
