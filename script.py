import datetime

from services import twitch as twitchService
from services import moviepy as moviePyService
from services import youtube as youtubeService
from services import meta as metaService

BLACKLISTED_CHANNELS = ["DisguisedToastHS"]

if __name__ == "__main__":
    clips = []
        
    response = twitchService.getTwitchClips(period='week', game='Fortnite', limit=2)
    
    for clip in response['clips']:
        # Check if channel isn't blacklisted
        if clip['broadcaster']['display_name'] not in BLACKLISTED_CHANNELS:
            # Save clip data. TODO: Save to database
            clips.append({
                'title': clip['title'],
                'channel': clip['broadcaster']['display_name'],
                'slug': clip['slug'],
                'game': clip['game'],
                'date': clip['created_at'],
                'views': clip['views'],
                'duration': clip['duration'],
            })

            # Download clip
            twitchService.downloadTwitchClip('downloads/', clip)

    output = datetime.date.today().strftime("%Y_%m_%d") + '.mp4'
    moviePyService.createVideoOfListOfClips(clips, output)
    config = metaService.createVideoConfig(clips)
    config['file'] = output
    youtubeService.uploadVideoToYouTube(config)
