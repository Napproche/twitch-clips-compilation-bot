import requests
import urllib.request
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, TextClip

from secrets import TWITCH_CLIENT_ID

BLACKLISTED_CHANNELS = ["DisguisedToastHS"]

def getTwitchClips(period, game, limit):
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': TWITCH_CLIENT_ID,
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

    # create downloads dir if it doesn't exist already
    if not os.path.exists(basedir + channel + '/'):
        os.makedirs(basedir + channel + '/')

    # get html content from url 
    html = str(urllib.request.urlopen(url).read())

    # extract the mp4 url for source quality
    mp4url = html.split('source\":\"')[1].split('\"}')[0]
    mp4url = mp4url.split('"', 1)[0]

    # download file to output path
    print('Downloading: ' + mp4url + ' --> ' + outputpath)
    # urllib.request.urlretrieve(mp4url, outputpath)

    # urllib is blocked so bypass using requests
    r  = requests.get(mp4url)
    f = open(outputpath,'wb')
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

# https://zulko.github.io/moviepy/examples/ukulele_concerto.html
def createVideoOfListOfClips(clips):
    final_clips = []

    for clip in clips:
        video = VideoFileClip("downloads/" + clip['channel'] + '/' + clip['slug'] + '.mp4')
        title = TextClip(clip['channel'] + ': ' + clip['title'], font='Amiri-regular', color='white', fontsize=50).set_duration(8)
        title_mov = title.set_pos((0.1,0.9), relative=True)

        # Create video object with text
        final_clip = CompositeVideoClip([video, title_mov])
        final_clips.append(final_clip)

    # Add clips together
    finished = concatenate_videoclips(final_clips, method='compose')

    # Render video
    finished.write_videofile("result.mp4", fps=30)

def uploadVideoToYouTube():
    print('test')

if __name__ == "__main__":
    # savedClips = []
    
    # response = getTwitchClips('day', 'Fortnite', 10)
    
    # for clip in response['clips']:
    #     # Check if channel isn't blacklisted
    #     if clip['broadcaster']['display_name'] not in BLACKLISTED_CHANNELS:
    #         # Save clip data. TODO: Save to database
    #         savedClips.append({
    #             'title': clip['title'],
    #             'channel': clip['broadcaster']['display_name'],
    #             'slug': clip['slug'],
    #             'game': clip['game'],
    #             'date': clip['created_at'],
    #             'views': clip['views'],
    #             'duration': clip['duration'],
    #         })

    #         # Download clip
    #         downloadTwitchClip('downloads/', clip)

    # createVideoOfListOfClips(savedClips)

    uploadVideoToYouTube()
