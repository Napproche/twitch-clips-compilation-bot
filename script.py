from services import twitch as twitchService
from services import moviepy as moviePyService
from services import youtube as youtubeService

BLACKLISTED_CHANNELS = ["DisguisedToastHS"]

if __name__ == "__main__":
    # clips = []
    
    # response = twitchService.getTwitchClips(period='week', game='Fortnite', limit=10)
    
    # for clip in response['clips']:
    #     # Check if channel isn't blacklisted
    #     if clip['broadcaster']['display_name'] not in BLACKLISTED_CHANNELS:
    #         # Save clip data. TODO: Save to database
    #         clips.append({
    #             'title': clip['title'],
    #             'channel': clip['broadcaster']['display_name'],
    #             'slug': clip['slug'],
    #             'game': clip['game'],
    #             'date': clip['created_at'],
    #             'views': clip['views'],
    #             'duration': clip['duration'],
    #         })

    #         # Download clip
    #         twitchService.downloadTwitchClip('downloads/', clip)

    # moviePyService.createVideoOfListOfClips(clips)

    youtubeService.uploadVideoToYouTube()
