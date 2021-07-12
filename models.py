import sqlite3
from datetime import datetime

class dbQuery():
    def __init__(self, db):
        self.db = db
    
    #: Add the user into the database if not registered
    def setUser(self, userId):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        isRegistered = cur.execute(f'SELECT * FROM users WHERE userId={userId}').fetchone()
        con.commit()

        isRegistered = True if isRegistered else False

        if not isRegistered:
            cur.execute(f"Insert into users (userId, date) values ({userId}, \"{datetime.today().strftime('%Y-%m-%d')}\")")
            cur.execute(f'Insert into settings (ownerId) values ({userId})')
            cur.execute(f'Insert into flood (ownerId) values ({userId})')
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
        
        users = cur.execute(f'SELECT ownerId FROM settings WHERE language="{language}"').fetchall()
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
        
        setting = cur.execute(f'SELECT {var} FROM {table} WHERE ownerId={userId} limit 1').fetchone()
        print(setting)
        con.commit()

        return setting[0] if setting else None

    #: Set the user's settings    
    def setSetting(self, userId, var, value, table='settings'):
        self.setUser(userId)
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        #!? If value is None, put value as NULL else "{string}"
        value = f'"{value}"' if value else 'NULL'
        cur.execute(f'INSERT OR IGNORE INTO {table} (ownerId, {var}) VALUES ({userId}, {value})')
        cur.execute(f'UPDATE {table} SET {var}={value} WHERE ownerId={userId}')
        con.commit()

    #: Add account in the user's accounts table
    def setAccount(self, userId, accountId, userName, email, password, cookie):
        self.setUser(userId)
        con = sqlite3.connect(self.db)
        cursor = con.cursor()
            
        #!? If the seedrId not on the table, insert new
        if cursor.execute(f'SELECT * FROM accounts WHERE ownerId={userId} AND accountId="{accountId}"').fetchone() == None:
            id = cursor.execute(f'INSERT INTO accounts (accountId, ownerId, userName, email, password, cookie) VALUES ({accountId},{userId},"{userName}","{email}", "{password}", "{cookie}")').lastrowid
            con.commit()

        #!? If the accountId is already on the table, update the cookie
        else:
            cursor.execute(f'UPDATE accounts SET cookie="{cookie}" WHERE ownerId={userId} AND accountId={accountId}')
            id = cursor.execute(f'SELECT id FROM accounts WHERE ownerID={userId} AND accountId="{accountId}"').fetchone()[0]
            con.commit()

        #!? Set the added account as the default account
        self.setDefaultAc(userId, id)
    
    #: Delete a user's account
    def deleteAccount(self, userId, accountId):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        defaultAcId = self.getSetting(userId, 'defaultAcId')
        cur.execute(f'DELETE FROM accounts WHERE ownerId={userId} AND id={accountId}')
        con.commit()

        #!? If the deleted account is the default account, set another account as a default account
        if str(accountId) == str(defaultAcId):
            lastAccountId = self.getAccounts(userId)
            
            #!? If any accounts is left, make the last account as a default account. Else, make default account empty.
            if lastAccountId:
                lastAccountId = lastAccountId[-1][0]
                self.setSetting(userId, 'defaultAcId', lastAccountId)
            #!? If no account left, make the default account NULL
            else:
                self.setSetting(userId, 'defaultAcId', None)

    #: Gel all accounts of certain user
    def getAccounts(self, userId):
        con = sqlite3.connect(self.db)
        con.row_factory = dict_factory
        cur = con.cursor()
        accounts = cur.execute(f'SELECT * FROM accounts WHERE ownerId={userId}').fetchall()
        con.commit()

        return accounts if accounts else None

    #: Gel certain account of a user
    def getAccount(self, userId, accountId):
        con = sqlite3.connect(self.db)
        con.row_factory = dict_factory
        cur = con.cursor()
        accounts = cur.execute(f'SELECT * FROM accounts WHERE ownerId={userId} and id={accountId}').fetchone()
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
            account = cur.execute(f'SELECT * FROM accounts WHERE ownerId={userId} AND id={defaultAcId}').fetchone()
            con.commit()

            return account      
        else:
            return None

    #: Set a user's default account
    def setDefaultAc(self, userId, accountId):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(f'INSERT OR IGNORE INTO settings (ownerId, defaultAcId) VALUES ({userId}, {accountId})')
        cur.execute(f'UPDATE settings SET defaultAcId={accountId} WHERE ownerId={userId}')
        con.commit()

#: Return query as dictionary
#! https://stackoverflow.com/a/3300514/13987868
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d