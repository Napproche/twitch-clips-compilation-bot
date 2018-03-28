import datetime
import os
import sys

from services import twitch as twitchService
from services import moviepy as moviePyService
from services import youtube as youtubeService
from services import meta as metaService
from services import database as databaseService

import constants

if __name__ == "__main__":
    PERIOD = sys.argv[1] 
    GAME = sys.argv[2]
    CLIPS = int(sys.argv[3])

    # Get popular Twitch clips.
    clips = twitchService.getTwitchClips(period=PERIOD, game=GAME, limit=CLIPS)

    # # Download clips.
    for clip in clips:
        twitchService.downloadTwitchClip(constants.DOWNLOAD_LOCATION, clip)

    # Render and save video.
    output = constants.DOWNLOAD_LOCATION + datetime.date.today().strftime("%Y_%m_%d") + '.mp4'
    # moviePyService.createVideoOfListOfClips(clips, output)

    connection = databaseService.getDatabaseConnection()
    
    # Get the type ID of this period.
    type_id = databaseService.getPeriodObjectID(connection, PERIOD)

    # Get ID to use for this video title. 
    video_count = databaseService.getCurrentCompilationVideoCount(connection, type_id)

    # Create YouTube meta data.
    config = metaService.createVideoConfig(clips, video_count, PERIOD)
    config['file'] = output

    # Store compilation video in database.
    databaseService.insertVideo(connection, config['title'], datetime.date.today(), type_id, 1)
    databaseService.closeConnection(connection)

    # Upload video to YouTube.
    youtubeService.uploadVideoToYouTube(config)

    # Remove rendered file after uploading.
    os.remove(output)