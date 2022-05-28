from os import remove
from pathlib import Path

import xspf_lib as xspf

from src.objs import *
from src.functions.urlEncode import urlEncode
from src.functions.exceptions import noAccount

@bot.callback_query_handler(func=lambda call: True and call.data[:12] == 'getPlaylist_')
def getPlaylist(call):
    ac = dbSql.getDefaultAc(call.from_user.id)
    userLanguage = dbSql.getSetting(call.from_user.id, 'language')

    if ac:        
        account = Seedr(
                token = ac['token'],
                callbackFunc = lambda token: dbSql.updateAccount(
                    token, call.from_user.id, ac['accountId']
                )
            )

        playlistType = call.data[12:15]
        callBacked = True

        #! If playlist type 000, get the type from database
        if playlistType == '000':
            playlistType = dbSql.getSetting(call.from_user.id, 'playlist')
            callBacked = False

        elif playlistType in ['m3u', 'vlc', 'xpf']:
            dbSql.setSetting(call.from_user.id, 'playlist', playlistType)

        #! If playlist type is not supported, set it to default
        else:
            playlistType = 'm3u'

        #! Create playlist file for media
        if call.data[16:20] == 'file':
            mediaType = 'file'
            id = call.data[21:]
            playlist = mediaToPlaylist(account, id, playlistType)

        #! Create playlist for folder
        else:
            mediaType = 'folder'
            id = call.data[23:]
            playlist = folderToPlaylist(account, id, playlistType, [])

        if playlist:
            bot.answer_callback_query(call.id)
            if not callBacked:
                bot.send_chat_action(call.message.chat.id, 'upload_document')

            thumb = open(f'images/{playlistType}.jpg', 'rb')

            bot.send_document(call.message.chat.id, open(playlist, 'rb'), thumb=thumb, reply_markup=playListButtons(userLanguage, mediaType, id, playlistType), caption=language['openInMediaCaption'][userLanguage])    
            remove(playlist)

        else:
            bot.answer_callback_query(call.id, language['noPlayableMedia'][userLanguage], show_alert=True)

    else:
        noAccount(call, userLanguage, called=True)

#: Generate playlist file for media
def mediaToPlaylist(account, fileId, playlistType):
    response = account.fetchFile(fileId)

    if 'url' in response:
        if playlistType == 'xpf':
            track = xspf.Track(location=urlEncode(response['url']), title=response['name'])

            playlist = xspf.Playlist(title=response['name'].replace('.',' '), trackList=[track])

            Path(f"/tmp/TorrentSeedr/{fileId}").mkdir(parents=True, exist_ok=True)
            playlistFile = f"/tmp/TorrentSeedr/{fileId}/{response['name'].replace('.',' ')}.xspf"
            open(playlistFile, 'wb').write(playlist.xml_string().encode())

        # For M3U and VLC
        else:
            track = f"#EXTM3U\n#EXTINF:1, {response['name']}\n{urlEncode(response['url'])}"

            Path(f"/tmp/TorrentSeedr/{fileId}").mkdir(parents=True, exist_ok=True)
            playlistFile = f"/tmp/TorrentSeedr/{fileId}/{response['name'].replace('.',' ')}.{playlistType}"
            open(playlistFile, 'wb').write(track.encode())

        return playlistFile

    else:
        return None

#: Generate playlist file for folder
def folderToPlaylist(account, folderId, playlistType, trackList):
    response = account.listContents(folderId=folderId)

    #! If success
    if 'name' in response:
        files = sorted(response['files'], key=lambda k: k['name']) 

        for file in files:
            if file['play_video'] == True or file['play_audio'] == True:
                fileUrl = account.fetchFile(file['folder_file_id'])

                if playlistType == 'xpf':
                    trackList+=[xspf.Track(location=urlEncode(fileUrl['url']), title=fileUrl['name'])]
                else:
                    trackList+=f"\n\n#EXTINF:1, {fileUrl['name']}\n{urlEncode(fileUrl['url'])}"

        #!? sort the list of files by its name
        folders = sorted(response['folders'], key=lambda k: k['name']) 

        #!? If the folder contains another folder, recall the function
        for folder in folders:
            folderToPlaylist(account, folder['id'], playlistType, trackList=trackList)

        #!? Create a playlist file if the folder contains tracks
        if trackList:
            if playlistType== 'xpf':
                playlist = xspf.Playlist(title=response['name'].replace('.',' '), trackList=trackList)

                Path(f"/tmp/TorrentSeedr/{folderId}").mkdir(parents=True, exist_ok=True)

                playlistFile = f"/tmp/TorrentSeedr/{folderId}/{response['name'].replace('.',' ')}.xspf"
                open(playlistFile, 'wb').write(playlist.xml_string().encode())

            # For M3U and VLC
            else:
                Path(f"/tmp/TorrentSeedr/{folderId}").mkdir(parents=True, exist_ok=True)

                playlistFile = f"/tmp/TorrentSeedr/{folderId}/{response['name'].replace('.',' ')}.{playlistType}"
                open(playlistFile, 'wb').write(('#EXTM3U\n'+''.join(trackList)).encode())

            return playlistFile

    return None

def playListButtons(userLanguage, mediaType, id, playlistType):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text=('✅ ' if playlistType=='vlc' else '')+ language['vlcBtn'][userLanguage], callback_data=f'getPlaylist_vlc_{mediaType}_{id}'),
               telebot.types.InlineKeyboardButton(text=('✅ ' if playlistType=='m3u' else '')+ language['m3uBtn'][userLanguage], callback_data=f'getPlaylist_m3u_{mediaType}_{id}'),
               telebot.types.InlineKeyboardButton(text=('✅ ' if playlistType=='xpf' else '')+language['xspfBtn'][userLanguage], callback_data=f'getPlaylist_xpf_{mediaType}_{id}'),
    )

    return markup
