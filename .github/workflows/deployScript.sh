# Due to a bug in appleboy/ssh-action@master, some commands shows error and fails to execute.
# So, running a bash file instead of commands

echo $1 > /opt/TorrentSeedr/TorrentSeedr/src/config.json ; source /opt/TorrentSeedr/venv/bin/activate && cd /opt/TorrentSeedr/TorrentSeedr && pip install -r requirements.txt && pm2 restart TorrentSeedr