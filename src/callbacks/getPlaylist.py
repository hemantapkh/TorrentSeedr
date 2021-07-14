import tempfile

import xspf_lib as xspf
from src.objs import *
from src.functions.exceptions import exceptions, noAccount

#: Removeing random name from file name
# -> https://stackoverflow.com/a/61282009/13987868
def gcn():
    return iter([" "])

tempfile._get_candidate_names = gcn

@bot.callback_query_handler(func=lambda call: True and call.data[:12] == 'getPlaylist_')
def getPlaylist(call):
    ac = dbSql.getDefaultAc(call.from_user.id)
    userLanguage = dbSql.getSetting(call.from_user.id, 'language')

    if ac:
        bot.answer_callback_query(call.id)
        account = Seedr(cookie=ac['cookie'])

        #! Create playlist file for media
        if call.data[12:16] == 'file':
            id = call.data[17:]
            
            try:
                response = account.fetchFile(id).json()

                if 'url' in response:
                    bot.send_chat_action(call.message.chat.id, 'upload_document')
                    track = xspf.Track(location=response['url'], title=response['name'])
                    
                    playlist = xspf.Playlist(title=response['name'].replace('.',' '), trackList=[track])

                    file = tempfile.NamedTemporaryFile(prefix=response['name'].replace('.',' '), suffix='.xspf')
                    file.write(playlist.xml_string().encode())
                    file.seek(0)

                    thumb = open('images/play.jpg', 'rb')
                    bot.send_document(call.message.chat.id, file, thumb=thumb)
                
                else:
                    exceptions(call, response, userLanguage, called=True)
            
            except json.JSONDecodeError:
                bot.edit_message_text(language['fileNotFound'][userLanguage], chat_id=call.message.chat.id, message_id=call.message.id)
    else:
        noAccount(call, userLanguage, called=True)