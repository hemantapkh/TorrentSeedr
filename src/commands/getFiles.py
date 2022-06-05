from src.objs import *
from src.functions.convert import convertSize
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount


#: Get the contents of a folder
@bot.message_handler(func=lambda message: message.text and message.text[:10] == '/getFiles_')
def getFiles(message, called=False):
    userId = message.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')

    if floodControl(message, userLanguage):
        ac = dbSql.getDefaultAc(userId)

        #! If user has an account
        if ac:
            id = message.data[9:] if called else message.text[10:]
            account = Seedr(
                token=ac['token'],
                callbackFunc=lambda token: dbSql.updateAccount(
                    token, userId, ac['accountId']
                )
            )

            response = account.listContents(folderId=id)

            if 'error' not in response:
                #! If success
                if 'name' in response:
                    text = f"<b>📁 {response['name']}</b>\n\n"
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(text=language['getLinkBtn'][userLanguage], callback_data=f'getLink_{id}'), telebot.types.InlineKeyboardButton(text=language['deleteBtn'][userLanguage], callback_data=f'delete_{id}'))

                    for folder in response['folders']:
                        text += f"🖿 {folder['name']} <b>[ {convertSize(folder['size'])}]</b>\n\n"
                        text += f"{language['files'][userLanguage]} /getFiles_{folder['id']}\n"
                        text += f"{language['link'][userLanguage]} /getLink_{folder['id']}\n"
                        text += f"{language['delete'][userLanguage]} /delete_{folder['id']}\n\n"

                    for file in response['files']:
                        text += f"<code>{'🎬' if file['play_video'] == True else '🎵' if file['play_audio'] == True else '📄'} {file['name']}</code> <b>[{convertSize(file['size'])}]</b>\n\n"
                        text += f"{language['link'][userLanguage]} /fileLink_{'v' if file['play_video'] == True else 'a' if file['play_audio'] == True else 'u'}{file['folder_file_id']}\n"
                        text += f"{language['delete'][userLanguage]} /remove_{file['folder_file_id']}\n\n"

                    markup.add(telebot.types.InlineKeyboardButton(text=language['openInPlayerBtn'][userLanguage], callback_data=f'getPlaylist_000_folder_{id}'))
                    markup.add(telebot.types.InlineKeyboardButton(text=language['joinChannelBtn'][userLanguage], url='t.me/h9youtube'), telebot.types.InlineKeyboardButton(text=language['joinDiscussionBtn'][userLanguage], url='https://t.me/+mxHaXtNFM1g5MzI1'))

                    if called:
                        bot.answer_callback_query(message.id)
                        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=text[:4000], reply_markup=markup)
                    else:
                        bot.send_message(message.chat.id, text[:4000], reply_markup=markup)

            else:
                exceptions(message, response, ac, userLanguage, called)

        #! If no accounts
        else:
            noAccount(message, userLanguage)
