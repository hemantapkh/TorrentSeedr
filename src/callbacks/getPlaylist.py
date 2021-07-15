import tempfile

import xspf_lib as xspf
from src.objs import *
from src.functions.urlEncode import urlEncode
from src.functions.exceptions import exceptions, noAccount

#: Removing random name from file name
# -> https://stackoverflow.com/a/61282009/13987868
# def gcn():
#     return iter([" "])

# tempfile._get_candidate_names = gcn

@bot.callback_query_handler(func=lambda call: True and call.data[:12] == 'getPlaylist_')
def getPlaylist(call):
    ac = dbSql.getDefaultAc(call.from_user.id)
    userLanguage = dbSql.getSetting(call.from_user.id, 'language')

    if ac:        
        account = Seedr(cookie=ac['cookie'])

        #! Create playlist file for media
        if call.data[12:16] == 'file':
            id = call.data[17:]
            
            try:
                response = account.fetchFile(id).json()

                if 'url' in response:
                    bot.send_chat_action(call.message.chat.id, 'upload_document')
                    track = xspf.Track(location=urlEncode(response['url']), title=response['name'])
                    
                    playlist = xspf.Playlist(title=response['name'].replace('.',' '), trackList=[track])

                    file = tempfile.NamedTemporaryFile(prefix=response['name'].replace('.',' '), suffix='.xspf')
                    file.write(playlist.xml_string().encode())
                    file.seek(0)

                    thumb = open('images/play.jpg', 'rb')
                    bot.send_document(call.message.chat.id, file, thumb=thumb)
                
                else:
                    exceptions(call, response, userLanguage, called=True)
            
            except json.JSONDecodeError:
                bot.answer_callback_query(call.id, language['fileNotFound'][userLanguage], show_alert=True)
        
        #! Create playlist for folder
        else:
            id = call.data[19:]

            playlist = folderToPlaylist(account, id, [])
            
            if playlist:
                bot.answer_callback_query(call.id)
                bot.send_chat_action(call.message.chat.id, 'upload_document')
                thumb = open('images/play.jpg', 'rb')
                bot.send_document(call.message.chat.id, playlist, thumb=thumb)
            
            else:
                bot.answer_callback_query(call.id, language['noPlayableMedia'][userLanguage], show_alert=True)
                
    else:
        noAccount(call, userLanguage, called=True)

#: Generate list of tracks from a folder
def folderToPlaylist(account, folderId, trackList):
    response = account.listContents(folderId=folderId).json()

    #! If success
    if 'name' in response:
        #!? sort the list of files by its name
        files = sorted(response['files'], key=lambda k: k['name']) 
        
        for file in files:
            if file['play_video'] == True or file['play_audio'] == True:
                fileUrl = account.fetchFile(file['folder_file_id']).json()
                trackList.append(xspf.Track(location=urlEncode(fileUrl['url']), title=fileUrl['name']))

        #!? sort the list of files by its name
        folders = sorted(response['folders'], key=lambda k: k['name']) 
        
        #!? If the folder contains another folder, recall the function
        for folder in folders:
            folderToPlaylist(account, folder['id'], trackList)

        #!? Create a playlist file if the folder contains tracks
        if trackList:
            playlist = xspf.Playlist(title=response['name'].replace('.',' '), trackList=trackList)

            playListFile = tempfile.NamedTemporaryFile(prefix=response['name'].replace('.',' '), suffix='.xspf')
            playListFile.write(playlist.xml_string().encode())
            playListFile.seek(0)

            return playListFile
    
    return None