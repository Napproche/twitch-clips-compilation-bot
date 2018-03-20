import requests
import os
import json
import requests
import urllib.request

import constants

def getTwitchClientID():
    secrets = json.load(open(constants.TWITCH_SECRETS_FILE))['client_id']
    return secrets

"""
    Fetch the amount of clips until we hit the limit.
"""
def getTwitchClips(period, game, limit):
    response = fetchTwitchClips(period, game, 100)

    clips = []
    counter = 0
    for clip in response['clips']:
        if counter < limit:
            if clip['broadcaster']['display_name'] not in constants.BLACKLISTED_CHANNELS:
                counter += 1
                clips.append({
                    'title': clip['title'],
                    'channel': clip['broadcaster']['display_name'],
                    'url': 'https://clips.twitch.tv/' + clip['slug'],
                    'slug': clip['slug'],
                    'game': clip['game'],
                    'date': clip['created_at'],
                    'views': clip['views'],
                    'duration': clip['duration'],
                })
    return clips 

def fetchTwitchClips(period, game, limit):
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': getTwitchClientID(),
    }

    params = (
        ('period', period),
        ('game', game),
        ('limit', limit),
        ('language', 'en')
    )

    response = requests.get('https://api.twitch.tv/kraken/clips/top', headers=headers, params=params)
    return response.json()

def downloadTwitchClip(basedir, clip):
    url = clip['url']
    channel = clip['channel']
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
