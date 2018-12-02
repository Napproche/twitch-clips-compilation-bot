import datetime
import os
import sys

from core.services import twitch as twitchService
from core.services import moviepy as moviePyService
from core.services import youtube as youtubeService
from core.services import meta as metaService
from core.services import thumbnail as thumbnailService
from core.models.logger import Logger
from core.models.parameters import Parameters

from core.models.models import Game, Type, Destination, Video, Clip, Channel

import constants

if __name__ == "__main__":
    parameters = Parameters(script_name=sys.argv[0], destination=sys.argv[1],
                            video_type=sys.argv[2], game=sys.argv[3], count=int(sys.argv[4]), custom_thumbnails=sys.argv[5])
    logger = Logger(parameters)

    # clips = twitchService.get_mock_clips(limit=CLIPS)
    clips = twitchService.get_top_clips(
        period=parameters.video_type.name, game=parameters.game.name, count=parameters.count)

    for clip in clips:
        twitchService.download_clip(
            constants.DOWNLOAD_LOCATION, clip['slug'], clip['channel_slug'])

    video_count = Video.select().where(
        (Video.destination == parameters.destination) &
        (Video.type == parameters.video_type) &
        (Video.game == parameters.game) &
        (Video.destination == parameters.destination)
    ).count() + 1

    video_title = metaService.create_video_title(
        clips[0]['title'], video_count, parameters.video_type.name, parameters.game.full)

    video = Video.create(title=video_title, game=parameters.game,
                         type=parameters.video_type, destination=parameters.destination)

    for clip_data in clips:
        channel = Channel.get_or_create(
            name=clip_data['channel_display_name'],
            slug=clip_data['channel_slug'],
            logo=clip_data['channel_logo'],
            url=clip_data['channel_url']
        )

        clip = None
        if Clip.select().where(Clip.slug == clip_data['slug']).exists():
            clip = Clip.get(slug=clip_data['slug'])
        else:
            clip = Clip.create(
                title=clip_data['title'],
                slug=clip_data['slug'],
                views=clip_data['views'],
                thumbnail=clip_data['thumbnail'],
                duration=clip_data['duration'],
                date=clip_data['date'],
                used_in_compilation_video=False,
                channel=channel[0],
                game=parameters.game
            )

        clip.videos.add(video)

    output = constants.DOWNLOAD_LOCATION + \
        datetime.date.today().strftime("%Y_%m_%d") + '.mp4'

    moviePyService.create_video_of_list_of_clips(video.clips, output)

    config = metaService.create_video_config(video.clips, parameters.game.full)

    config['title'] = video_title
    config['description'] = metaService.create_video_description(video.clips)
    config['file'] = output
    config['destination'] = parameters.destination.name

    if parameters.custom_thumbnails:
        config['thumbnail'] = thumbnailService.create(
            video.clips[0], video_count, parameters.destination.name, parameters.game.name, parameters.video_type.name)

    youtubeService.upload_video_to_youtube(config)

    os.remove(output)
