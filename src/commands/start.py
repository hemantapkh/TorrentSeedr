import requests, json
from src.objs import *
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
            data = requests.get(f"https://torrentseedrbot.herokuapp.com/getdata?key={config['databaseKey']}&id={params}")
            data = json.loads(data.content)

            if data['status'] == 'success':
                data = json.loads(data['data'])
                
                #! Login new account
                if data['type'] == 'login':
                    login(sent, userLanguage, data)
            
            else:
                print(data)

#: Account login
def login(sent, userLanguage, data):
    userId = sent.chat.id
    bot.edit_message_text(language['loggingIn'][userLanguage], chat_id=sent.chat.id, message_id=sent.id)
    
    response = seedrAc.login(data['email'], data['password'], data['captchaResponse'])
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    response = response.json()

    #! If account logged in successfully
    if 'remember' in cookies:
        dbSql.setAccount(userId, accountId=response['user_id'], userName=response['username'], email=data['email'], password=data['password'], cookie=f"remember={cookies['remember']}")
        bot.delete_message(chat_id=sent.chat.id, message_id=sent.id)
        bot.send_message(chat_id=sent.chat.id, text=language['loggedInAs'][userLanguage].format(response['username']), reply_markup=mainReplyKeyboard(userId, userLanguage))
    
    else:
        #! Captcha failed
        if response['error'] == 'RECAPTCHA_FAILED':
            bot.edit_message_text(language['captchaFailled'][userLanguage], chat_id=sent.chat.id, message_id=sent.id)
        
        #! Wrong username or password
        elif response['error'] == 'INCORRECT_PASSWORD':
             bot.edit_message_text(language['incorrectPassword'][userLanguage], chat_id=sent.chat.id, message_id=sent.id)
        
        #! Unknown error
        else:
            bot.edit_message_text(language['unknownError'][userLanguage].format(response.text), chat_id=sent.chat.id, message_id=sent.id)