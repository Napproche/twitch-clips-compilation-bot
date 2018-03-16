import requests
import os
import json
import requests
import urllib.request

TWITCH_SECRETS_FILE = 'secrets/twitch_secret.json'

def getTwitchClientID():
    secrets = json.load(open(TWITCH_SECRETS_FILE))['client_id']
    return secrets

def getTwitchClips(period, game, limit):
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': getTwitchClientID(),
    }

    params = (
        ('period', period),
        ('game', game),
        ('limit', limit)
    )

    response = requests.get('https://api.twitch.tv/kraken/clips/top', headers=headers, params=params)
    return response.json()

def downloadTwitchClip(basedir, clip):
    url = clip['url']
    channel = clip['broadcaster']['display_name']
    filename = clip['slug']
    
    outputpath = (basedir + channel + '/' + filename + '.mp4').replace('\n', '')

    # Create downloads directory if it doesn't exist already
    if not os.path.exists(basedir + channel + '/'):
        os.makedirs(basedir + channel + '/')

    # Get html content from url 
    html = str(urllib.request.urlopen(url).read())

    # Extract the mp4 url for source quality
    mp4url = html.split('source\":\"')[1].split('\"}')[0]
    mp4url = mp4url.split('"', 1)[0]

    # Download file to output path
    print('Downloading: ' + mp4url + ' --> ' + outputpath)
    r  = requests.get(mp4url)
    f = open(outputpath,'wb')
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()
