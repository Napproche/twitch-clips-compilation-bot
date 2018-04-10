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
    logger.broadcast('Starting bot with parameters: {0}, {1}, {2}, {3}'.format(CHANNEL, GAME, PERIOD, CLIPS))

    try:
        clips = twitchService.getTwitchClips(period=PERIOD, game=GAME, limit=CLIPS)
    except Exception as e:
        logger.log('Error fetching Twitch clips', e)

    try:
        for clip in clips:
            twitchService.downloadTwitchClip(constants.DOWNLOAD_LOCATION, clip)
    except Exception as e:
        logger.log('Error download Twitch clips', e)

    try:
        output = constants.DOWNLOAD_LOCATION + datetime.date.today().strftime("%Y_%m_%d") + '.mp4'
        moviePyService.createVideoOfListOfClips(clips, output)
    except Exception as e:
        logger.log('Error rendering video', e)

    try:
        connection = databaseService.getDatabaseConnection()

        period = databaseService.getPeriod(connection, PERIOD)
        channel = databaseService.getChannel(connection, CHANNEL)
        game = databaseService.getGame(connection, GAME)

        video_count = databaseService.getCurrentCompilationVideoCount(connection, channel[0], game[0], period[0])
    except Exception as e:
        logger.log('Error fetching data from local database', e)

    try:
        thumbnail = thumbnailService.create(clips[0], video_count, channel[1], game[1], period[1])
    except Exception as e:
        logger.log('Error creating thumbnail', e)

    try:
        config = metaService.createVideoConfig(clips, video_count, PERIOD, game[2])
        config['file'] = output
        config['channel'] = channel
        config['thumbnail'] = thumbnail
    except Exception as e:
        logger.log('Error creating YouTube meta data config', e)

    try:
        databaseService.insertVideo(connection, config['title'], datetime.date.today(), period[0], game[0], channel[0])
        databaseService.closeConnection(connection)
    except Exception as e:
        logger.log('Error inserting video data in local database', e)

    try:
        youtubeService.uploadVideoToYouTube(config)
    except Exception as e:
        logger.log('Error uploading video to YouTube', e)

    try:
        os.remove(output)
    except Exception as e:
        logger.log('Error removing file from server', e)