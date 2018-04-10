import datetime, os, sys

from core.services import twitch as twitchService
from core.services import moviepy as moviePyService
from core.services import youtube as youtubeService
from core.services import meta as metaService
from core.services import database as databaseService
from core.services import thumbnail as thumbnailService

from core.models.logger import Logger

import constants

if __name__ == "__main__":
    CHANNEL = sys.argv[1]
    GAME = sys.argv[2]
    PERIOD = sys.argv[3]
    CLIPS = int(sys.argv[4])

    logger = Logger('errors.log')

    # Fetch Twitch clips.
    try:
        clips = twitchService.getTwitchClips(period=PERIOD, game=GAME, limit=CLIPS)
    except Exception as e:
        logger.log('Error fetching Twitch clips', e)

    # Download clips.
    try:
        for clip in clips:
            twitchService.downloadTwitchClip(constants.DOWNLOAD_LOCATION, clip)
    except Exception as e:
        logger.log('Error download Twitch clips', e)

    # Render and save video.
    output = constants.DOWNLOAD_LOCATION + datetime.date.today().strftime("%Y_%m_%d") + '.mp4'
    moviePyService.createVideoOfListOfClips(clips, output)

    connection = databaseService.getDatabaseConnection()
    
    period = databaseService.getPeriod(connection, PERIOD)
    channel = databaseService.getChannel(connection, CHANNEL)
    game = databaseService.getGame(connection, GAME)

    # Get ID to use for this video title. 
    video_count = databaseService.getCurrentCompilationVideoCount(connection, channel[0], game[0], period[0])

    # Create thumbnail
    thumbnail = thumbnailService.create(clips[0], video_count, channel[1], game[1], period[1])

    # Create YouTube meta data.
    config = metaService.createVideoConfig(clips, video_count, PERIOD, game[2])
    config['file'] = output
    config['channel'] = channel
    config['thumbnail'] = thumbnail

    # Store compilation video in database.
    databaseService.insertVideo(connection, config['title'], datetime.date.today(), period[0], game[0], channel[0])
    databaseService.closeConnection(connection)

    # Upload video to YouTube.
    youtubeService.uploadVideoToYouTube(config)

    # Remove rendered file after uploading.
    os.remove(output)