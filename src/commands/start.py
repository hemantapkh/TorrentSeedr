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

    if floodControl(message, userLanguage):
        if not params:
            bot.send_message(message.chat.id, text=language['greet'][userLanguage], reply_markup=mainReplyKeyboard(userId, userLanguage))

        #! If start paramater is passed
        if params:
            sent = bot.send_message(message.chat.id, text=language['processing'][userLanguage])

            #! Github oauth
            if params.startswith('oauth'):
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
 
            #! If add torrent paramater is passed
            elif params.startswith('addTorrent'):
                url = f'https://tinyurl.com/{params[11:]}'
                response = requests.get(url, allow_redirects=False)
                
                asyncio.run(addTorrent(message, userLanguage, magnetLink=response.headers['Location'], messageId=sent.id))

            #! Else, login token is passed
            else:
                data = requests.get(f"https://torrentseedrbot.herokuapp.com/getdata?key={config['databaseKey']}&id={params}")
                data = json.loads(data.content)

                if data['status'] == 'success':
                    data = json.loads(data['data'])
                    
                    #! Login new account
                    if data['type'] == 'login':
                        login(sent, userLanguage, data)
                    
                    elif data['type'] == 'refresh':
                        login(sent, userLanguage, data, refresh=True)
                
                else:
                    bot.edit_message_text(language['processFailed'][userLanguage], chat_id=sent.chat.id, message_id=sent.id)

#: Account login
def login(sent, userLanguage, data, refresh=False):
    userId = sent.chat.id
    bot.edit_message_text(language['refreshing'][userLanguage] if refresh else language['loggingIn'][userLanguage], chat_id=sent.chat.id, message_id=sent.id)
    
    if refresh:
        ac = dbSql.getDefaultAc(userId)
        if ac:
            email = ac['email']
            password = ac['password']
            response = seedrAc.login(email, password, data['captchaResponse'])
        else:
            response = None
            bot.edit_message_text(language['noAccount'][userLanguage] if refresh else language['loggingIn'][userLanguage], chat_id=sent.chat.id, message_id=sent.id)
    else:
        email = data['email']
        password = data['password']
        response = seedrAc.login(email, password, data['captchaResponse'])
    
    if response:
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        response = response.json()

        #! If account logged in successfully
        if 'remember' in cookies:
            dbSql.setAccount(userId, accountId=response['user_id'], userName=response['username'], email=email, password=password, cookie=f"remember={cookies['remember']}")
            bot.delete_message(chat_id=sent.chat.id, message_id=sent.id)
            bot.send_message(chat_id=sent.chat.id, text=language['refreshed'][userLanguage].format(response['username']) if refresh else language['loggedInAs'][userLanguage].format(response['username']), reply_markup=mainReplyKeyboard(userId, userLanguage))
        
        else:
            #! Captcha failed
            if response['error'] == 'RECAPTCHA_FAILED':
                bot.edit_message_text(language['captchaFailled'][userLanguage], chat_id=sent.chat.id, message_id=sent.id)
            
            #! Wrong username or password
            elif response['error'] == 'INCORRECT_PASSWORD':
                if refresh:
                    dbSql.deleteAccount(userId, ac['id'])
                    bot.delete_message(chat_id=sent.chat.id, message_id=sent.id)
                    bot.send_message(text=language['incorrectPassword'][userLanguage], chat_id=sent.chat.id, reply_markup=mainReplyKeyboard(userId, userLanguage))

                else:
                    bot.edit_message_text(language['incorrectPassword'][userLanguage], chat_id=sent.chat.id, message_id=sent.id)
            
            #! Unknown error
            else:
                bot.edit_message_text(language['unknownError'][userLanguage].format(response.text), chat_id=sent.chat.id, message_id=sent.id)