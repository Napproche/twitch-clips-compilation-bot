import datetime
import os
import sys

from core.services import twitch as twitchService
from core.services import moviepy as moviePyService
from core.services import youtube as youtubeService
from core.services import meta as metaService
from core.services import thumbnail as thumbnailService
from core.models.logger import Logger

from core.models.models import Game, Type, Destination, Video, Clip, Channel

import constants

if __name__ == "__main__":
    DESTINATION = sys.argv[1]
    GAME = sys.argv[2]
    VIDEO_TYPE = sys.argv[3]
    CLIPS = int(sys.argv[4])

    logger = Logger('errors.log')
    logger.broadcast('Starting bot with parameters: {0}, {1}, {2}, {3}'.format(
        DESTINATION, GAME, VIDEO_TYPE, CLIPS))

    # clips = twitchService.get_mock_clips(limit=CLIPS)
    clips = twitchService.get_top_clips(period=VIDEO_TYPE, game=GAME, limit=CLIPS)

    video_type = Type.get(name=VIDEO_TYPE)
    destination, created = Destination.get_or_create(name=DESTINATION)
    destination = Destination.get(name=DESTINATION)
    game = Game.get(name=GAME)

    for clip in clips:
        twitchService.download_clip(constants.DOWNLOAD_LOCATION, clip)

    output = constants.DOWNLOAD_LOCATION + \
        datetime.date.today().strftime("%Y_%m_%d") + '.mp4'

    print('Rendering video to location  %s' % (output))
    moviePyService.create_video_of_list_of_clips(clips, output)

    video_count = Video.select().where(
        (Video.destination == destination) &
        (Video.type == video_type) &
        (Video.game == game)
    ).count() + 1 

    video_title = metaService.create_video_title(
        clips[0]['title'], video_count, video_type.name, game.name)

    video = Video(title=video_title, game=game,
                  type=video_type, destination=destination)
    video.save()

    for clip_data in clips:
        channel = Channel.get_or_create(
            name=clip_data['channel_display_name'],
            slug=clip_data['channel_slug'],
            logo=clip_data['channel_logo'],
            url=clip_data['channel_url']
        )

        clip = Clip.get_or_create(
            title=clip_data['title'],
            slug=clip_data['slug'],
            views=clip_data['views'],
            thumbnail=clip_data['thumbnail'],
            duration=clip_data['duration'],
            date=clip_data['date'],
            used_in_compilation_video=False,
            channel=channel[0],
            game=game
        )

        clip = Clip.get(slug=clip_data['slug'])
        clip.videos.add(video)

    thumbnail = thumbnailService.create(
        video.clips[0], video_count, destination.name, game.name, video_type.name)

    config = metaService.create_video_config(
        clips, video_count, VIDEO_TYPE, game.name)

    config['title'] = video_title
    config['description'] = metaService.create_video_description(video.clips)
    config['file'] = output
    config['channel'] = destination
    config['thumbnail'] = thumbnail

    youtubeService.upload_video_to_youtube(config)

    os.remove(output)
