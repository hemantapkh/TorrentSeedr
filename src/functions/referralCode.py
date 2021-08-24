from src.objs import *

previousUser = None
def referralCode():
    global previousUser
    users = dbSql.getAllGhUsers()
    
    if users:
        index = 0 if not previousUser else users.index(previousUser) + 1 if (len(users)-1) > users.index(previousUser) else 0
        account = dbSql.getDefaultAc(users[index])
        
        previousUser = users[index]
        dbSql.setSetting(account['ownerId'], 'totalRefer', dbSql.getSetting(account['ownerId'], 'totalRefer')+1)

        return account['accountId'] if account else '921385'
    
    else:
        return '921385'