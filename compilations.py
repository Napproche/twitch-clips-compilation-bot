import datetime
import os
import sys

from core.services import twitch as twitchService
from core.services import moviepy as moviePyService
from core.services import youtube as youtubeService
from core.services import meta as metaService
from core.services import thumbnail as thumbnailService
from core.enums.video_type import VideoType

from core.models.models import Game, Channel, Clip, Video, Destination, Type

import constants

if __name__ == "__main__":
    DESTINATION = sys.argv[1]
    GAME = sys.argv[2]
    CLIP_COUNT = int(sys.argv[3])
    VIDEO_TYPE = VideoType.Compilation.value

    game = Game.get(Game.name == GAME)
    destination = Destination.get(Destination.name == DESTINATION)
    video_type = Type.get(Type.id == VIDEO_TYPE)

    selected_channel = None
    selected_clips = []

    highest_clip_count = 0

    channels = Channel.select()
    for channel in channels:
        clips = Clip.select().where(
            (Clip.channel == channel.id) &
            (Clip.used_in_compilation_video == False)
        ).order_by(-Clip.views)

        if len(clips) >= CLIP_COUNT:

            if len(clips) > highest_clip_count:
                highest_clip_count = len(clips)
                selected_channel = channel
                selected_clips = clips[:CLIP_COUNT]

    if selected_channel is not None:
        compilation_count = Video.select().where(
            (Video.type == video_type) &
            (Video.game == game) &
            (Video.channel == channel)
        ).count() + 1

        output = constants.DOWNLOAD_LOCATION + \
            datetime.date.today().strftime("%Y_%m_%d") + '_' + \
            selected_channel.slug + '_compilation_' + \
            str(compilation_count) + '.mp4'

        for clip in selected_clips:
            twitchService.download_clip(
                constants.DOWNLOAD_LOCATION, clip.slug, clip.channel.slug)

        print('Rendering video to location  %s' % (output))
        moviePyService.create_video_of_list_of_clips(selected_clips, output)

        thumbnail = thumbnailService.create(
            selected_clips[0], compilation_count, destination.name, game.name, video_type.name)

        config = metaService.create_video_config(
            selected_clips, compilation_count, VIDEO_TYPE, game.name)
        config['title'] = metaService.create_channel_compilation_video_title(selected_clips[0], game, compilation_count)
        config['description'] = metaService.create_video_description(
            selected_clips)
        config['file'] = output
        config['destination'] = destination.name
        config['thumbnail'] = thumbnail

        for clip in selected_clips:
            clip.used_in_compilation_video = True
            clip.save()
            os.remove(twitchService.get_clip_output_path(constants.DOWNLOAD_LOCATION, clip))

        youtubeService.upload_video_to_youtube(config)

        os.remove(output)
