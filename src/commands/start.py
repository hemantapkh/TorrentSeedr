import asyncio
import requests, json
from src.objs import *
from src.commands.addTorrent import addTorrent
from src.functions.floodControl import floodControl
from src.functions.keyboard import mainReplyKeyboard

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

            #! If add torrent paramater is passed
            if params.startswith('addTorrent'):
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
            response = seedrAc.login(ac['email'], ac['password'], data['captchaResponse'])
        else:
            response = None
            bot.edit_message_text(language['noAccount'][userLanguage] if refresh else language['loggingIn'][userLanguage], chat_id=sent.chat.id, message_id=sent.id)
    else:
        response = seedrAc.login(data['email'], data['password'], data['captchaResponse'])
    
    if response:
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        response = response.json()

        #! If account logged in successfully
        if 'remember' in cookies:
            dbSql.setAccount(userId, accountId=response['user_id'], userName=response['username'], email=data['email'], password=data['password'], cookie=f"remember={cookies['remember']}")
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