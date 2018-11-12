import datetime
import os
import sys

from core.services import twitch as twitchService
from core.services import moviepy as moviePyService
from core.services import youtube as youtubeService
from core.services import meta as metaService
from core.services import thumbnail as thumbnailService
from core.models.logger import Logger
# from core.models.database import Database
from core.enums.video_type import VideoType

from core.models.models import Game, Channel

import constants

if __name__ == "__main__":
    GAME = sys.argv[1]
    CLIP_COUNT = int(sys.argv[2])
    VIDEO_TYPE = VideoType.Compilation.value

    game = Game.get(Game.name == GAME)

    selected_channel = None
    selected_clips = []

    highest_clip_count = 0

    # Get channel with most clips to make compilation of.
    channels = Channel.get()
    for channel in channels:
        print(channel)
        # clips = database.get_clips_by_channel(
        #     channel[0], used_in_compilation_video=False)

        # if len(clips) >= CLIP_COUNT:

        #     if len(clips) > highest_clip_count:
        #         highest_clip_count = len(clips)
        #         selected_channel = channel
        #         selected_clips = clips
        #         # Sort list on most viewed clips first
        #         selected_clips.sort(key=lambda x: x[3], reverse=True)
        #         selected_clips = clips[:CLIP_COUNT]

    if selected_channel is not None:
        # compilation_count = database.get_compilation_count_by_channel(game[0], selected_channel[0])

        # output = constants.DOWNLOAD_LOCATION + \
        #     datetime.date.today().strftime("%Y_%m_%d") + '_' + \
        #     selected_channel[2] + '_compilation_' + \
        #     str(compilation_count) + '.mp4'
        # print(output)

        print('Rendering video to location  %s' % (output))
        # moviePyService.create_video_of_list_of_clips(selected_clips, output)

        # todo 
        # thumbnail = thumbnailService.create(
        #     clips[0], video_count, destination[1], game[1], video_type[1])


        # print(selected_clips, compilation_count, VIDEO_TYPE, game[2])
        # config = metaService.create_video_config(selected_clips, compilation_count, VIDEO_TYPE, game[2])
        # config['file'] = output
        # config['channel'] = destination
        # config['thumbnail'] = thumbnail

        print(config)


        # # Update clips with used_in_compilation_video = True
        # for clip in selected_clips:
        #     print(clip)
        #     # database.set_clip_used_in_compilation_video_true(clip[0])
        #     # delete downloaded clips?
