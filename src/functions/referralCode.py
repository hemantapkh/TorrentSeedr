from src.objs import *


previousUser = None
def referralCode():
    global previousUser
    users = dbSql.getAllGhUsers()

    if users:
        index = (users.index(previousUser)+1) % len(users) if previousUser else 0
        account = dbSql.getDefaultAc(users[index])

        previousUser = users[index]
        dbSql.setSetting(account['ownerId'], 'totalRefer', dbSql.getSetting(account['ownerId'], 'totalRefer')+1)

        return account['accountId']

    else:
        return 921385
