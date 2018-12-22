import datetime
import os
import sys

from core.services import twitch as twitchService
from core.services import moviepy as moviePyService
from core.services import youtube as youtubeService
from core.services import meta as metaService
from core.services import thumbnail as thumbnailService
from core.enums.video_type import VideoType
from core.models.logger import Logger
from core.models.parameters import Parameters
from core.models.models import Game, Channel, Clip, Video, Destination, Type

import constants

if __name__ == "__main__":
    parameters = Parameters(script_name=sys.argv[0], destination=sys.argv[1],
                            video_type=VideoType.Compilation.value, game=sys.argv[2], count=int(sys.argv[3]), custom_thumbnails=sys.argv[4])
    logger = Logger(parameters)

    selected_channel = None
    selected_clips = []

    highest_clip_count = 0

    channels = Channel.select()
    for channel in channels:
        clips = Clip.select().where(
            (Clip.channel == channel.id) &
            (Clip.used_in_compilation_video == False)
        ).order_by(-Clip.views)

        if len(clips) >= parameters.count:

            if len(clips) > highest_clip_count:
                highest_clip_count = len(clips)
                selected_channel = channel
                selected_clips = clips[:parameters.count]

    if selected_channel is not None:
        compilation_count = Video.select().where(
            (Video.type == parameters.video_type) &
            (Video.game == parameters.game) &
            (Video.channel == channel) &
            (Video.destination == parameters.destination)
        ).count() + 1

        output = constants.DOWNLOAD_LOCATION + \
            datetime.date.today().strftime("%Y_%m_%d") + '_' + \
            selected_channel.slug + '_compilation_' + \
            str(compilation_count) + '.mp4'

        for clip in selected_clips:
            twitchService.download_clip(
                constants.DOWNLOAD_LOCATION, clip.slug, clip.channel.slug)

        moviePyService.create_video_of_list_of_clips(selected_clips, output)

        compilation_title = metaService.create_channel_compilation_video_title(
            selected_clips[0], parameters.game, compilation_count)

        video = Video.create(title=compilation_title, game=parameters.game,
                             type=parameters.video_type, destination=parameters.destination, channel=selected_channel)

        config = metaService.create_video_config(
            clips=selected_clips, game=parameters.game.full, title=compilation_title, file=output, destination=parameters.destination.name)

        if parameters.count:
            config['thumbnail'] = thumbnailService.create(
                selected_clips[0], compilation_count, parameters.destination.name, parameters.game.name, parameters.video_type.name, selected_clips[0].channel.logo)

        for clip in selected_clips:
            clip.used_in_compilation_video = True
            clip.videos.add(video)
            clip.save()
            os.remove(twitchService.get_clip_output_path(
                constants.DOWNLOAD_LOCATION, clip))

        youtubeService.upload_video_to_youtube(config)

        os.remove(output)
