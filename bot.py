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
    VIDEO_TYPE = sys.argv[3]
    CLIPS = int(sys.argv[4])

    logger = Logger('errors.log')
    logger.broadcast('Starting bot with parameters: {0}, {1}, {2}, {3}'.format(
        CHANNEL, GAME, VIDEO_TYPE, CLIPS))

    # clips = twitchService.get_mock_clips(limit=CLIPS)

    clips = twitchService.get_top_clips(period=VIDEO_TYPE, game=GAME, limit=CLIPS)

    database = Database()
    video_type = database.get_video_type(VIDEO_TYPE)
    destination = database.get_destination(CHANNEL)
    game = database.get_game(GAME)

    # for clip in clips:
    #     twitchService.download_clip(constants.DOWNLOAD_LOCATION, clip)

    output = constants.DOWNLOAD_LOCATION + \
        datetime.date.today().strftime("%Y_%m_%d") + '.mp4'

    # print('Rendering video to location  %s' % (output))
    # moviePyService.create_video_of_list_of_clips(clips, output)

    video_count = database.get_current_compilation_video_count(
        destination[0], game[0], video_type[0])
    thumbnail = thumbnailService.create(
        clips[0], video_count, destination[1], game[1], video_type[1])

    config = metaService.create_video_config(
        clips, video_count, VIDEO_TYPE, game[2])
    config['file'] = output
    config['channel'] = destination
    config['thumbnail'] = thumbnail

    video_id = database.insert_video(config['title'], datetime.date.today(
    ), video_type[0], game[0], destination[0])

    for clip in clips:
        channel = database.get_channel(
            clip['channel_display_name'], clip['channel_slug'], clip['channel_logo'], clip['channel_logo'])
        clip_id = database.insert_clip(clip['title'], clip['slug'], clip['views'], clip['date'], channel[0], game[0])
        database.insert_videos_clips(video_id, clip_id)

    database.close_connection()

    # youtubeService.upload_video_to_youtube(config)

    # os.remove(output)
