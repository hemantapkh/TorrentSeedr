import asyncio
import requests, json
from src.objs import *
from src.commands.addTorrent import addTorrent
from src.functions.floodControl import floodControl
from src.functions.referralCode import referralCode
from src.functions.keyboard import mainReplyKeyboard, githubAuthKeyboard

# Start handler
@bot.message_handler(commands=['start'])
def start(message):
    userId = message.from_user.id
    params = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    userLanguage = dbSql.getSetting(userId, 'language')

    if not params:
        bot.send_message(message.chat.id, text=language['greet'][userLanguage], reply_markup=mainReplyKeyboard(userId, userLanguage))

    #! If start paramater is passed
    if params:
        sent = bot.send_message(message.chat.id, text=language['processing'][userLanguage])

        #! If add torrent paramater is passed via database key
        if params.startswith('addTorrentDb'):
            key = params[13:]
            magnetLink = dbSql.getMagnet(key)

            asyncio.run(addTorrent(message, userLanguage, magnetLink, messageId=sent.id))
        
        #! If add torrent paramater is passed via URL
        elif params.startswith('addTorrentURL'):
            url = f'https://is.gd/{params[14:]}'
            response = requests.get(url, allow_redirects=False)
            magnetLink = response.headers['Location'] if 'Location' in response.headers else None
            
            asyncio.run(addTorrent(message, userLanguage, magnetLink, messageId=sent.id))

        #! Github oauth
        elif params.startswith('oauth'):
            code = params[6:]
            
            params = {'client_id': 'ba5e2296f2bbe59f5097', 'client_secret': config['githubSecret'], 'code':code}
            response = requests.get('https://github.com/login/oauth/access_token', params=params)
            
            #! Successfully authenticated
            if response.text[:13] == 'access_token=':
                accessToken = response.text[13:].split('&', 1)[0]

                headers = {'Authorization': f'token {accessToken}'}
                response = requests.get('https://api.github.com/user', headers=headers).json()

                if 'login' in response:
                    bot.edit_message_text(language['loggedInAs'][userLanguage].format(f"<a href='https://github.com/{response['login']}'>{response['login'].capitalize()}</a>"), chat_id=sent.chat.id, message_id=sent.id)

                    following = requests.get(f"https://api.github.com/users/{response['login']}/following").json()
                    
                    #! User is following
                    if any(dicT['login'] == 'hemantapkh' for dicT in following):
                        dbSql.setSetting(userId, 'githubId', response['id'])
                        bot.send_message(chat_id=message.chat.id, text=language['thanksGithub'][userLanguage])
                    
                    #! User is not following
                    else:
                        bot.send_message(chat_id=message.chat.id, text=language['ghNotFollowed'][userLanguage], reply_markup=githubAuthKeyboard(userLanguage))

            #! Error
            else:
                bot.edit_message_text(language['processFailed'][userLanguage], chat_id=sent.chat.id, message_id=sent.id)