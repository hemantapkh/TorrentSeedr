import urllib.parse as urlparse

def urlEncode(url):
    return urlparse.quote(url, safe='/:&?=%')