import datetime
import os
import sys

from core.services import twitch as twitchService
from core.services import moviepy as moviePyService
from core.services import youtube as youtubeService
from core.services import meta as metaService
from core.services import thumbnail as thumbnailService
from core.models.logger import Logger
from core.models.database import Database

import constants

if __name__ == "__main__":
    CHANNEL = sys.argv[1]
    GAME = sys.argv[2]
    PERIOD = sys.argv[3]
    CLIPS = int(sys.argv[4])

    logger = Logger('errors.log')
    logger.broadcast('Starting bot with parameters: {0}, {1}, {2}, {3}'.format(
        CHANNEL, GAME, PERIOD, CLIPS))

    clips = twitchService.get_twitch_clips(
        period=PERIOD, game=GAME, limit=CLIPS)

    database = Database()
    period = database.get_channel(PERIOD)
    channel = database.get_channel(CHANNEL)
    game = database.get_game(GAME)

    # for clip in clips:
        # twitchService.download_clip(constants.DOWNLOAD_LOCATION, clip)

    output = constants.DOWNLOAD_LOCATION + \
        datetime.date.today().strftime("%Y_%m_%d") + '.mp4'
    moviePyService.create_video_of_list_of_clips(clips, output)

    # video_count = databaseService.get_current_compilation_video_count(
    #     connection, channel[0], game[0], period[0])

    # thumbnail = thumbnailService.create(
    #     clips[0], video_count, channel[1], game[1], period[1])

    # config = metaService.create_video_config(
    #     clips, video_count, PERIOD, game[2])
    # config['file'] = output
    # config['channel'] = channel
    # config['thumbnail'] = thumbnail

    # databaseService.insert_video(
    #     connection, config['title'], datetime.date.today(), period[0], game[0], channel[0])
    # databaseService.close_connection(connection)

    # youtubeService.upload_video_to_youtube(config)

    # os.remove(output)
