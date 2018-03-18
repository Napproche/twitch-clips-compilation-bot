import datetime

from services import twitch as twitchService
from services import moviepy as moviePyService
from services import youtube as youtubeService
from services import meta as metaService
from services import database as databaseService

BLACKLISTED_CHANNELS = ["DisguisedToastHS", "xChocoBars"]

if __name__ == "__main__":
    clips = []
    
    # Get popular Twitch clips.
    response = twitchService.getTwitchClips(period='day', game='Fortnite', limit=20)
    
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

            # Download clip.
            twitchService.downloadTwitchClip('downloads/', clip)

    # Render and save video.
    output = 'downloads/' + datetime.date.today().strftime("%Y_%m_%d") + '.mp4'
    moviePyService.createVideoOfListOfClips(clips, output)

    connection = databaseService.getDatabaseConnection()
    
    # Get ID to use for this video title. 
    video_count = databaseService.getCurrentCompilationVideoCount(connection)

    # Create YouTube meta data.
    config = metaService.createVideoConfig(clips, video_count)
    config['file'] = output

    # Store compilation video in database.
    databaseService.insertVideo(connection, config['title'], datetime.date.today(), 1, 1)
    databaseService.closeConnection(connection)

    # # Upload video to YouTube.
    youtubeService.uploadVideoToYouTube(config)

