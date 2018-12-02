def create_video_config(clips, game):
    config = {}
    config['category'] = 20  # Gaming ID
    config['keywords'] = get_keywords(game, clips)

    return config


def get_keywords(game, clips):
    keywords = game + ', Daily, Compilation, Gaming'
    for clip in clips:
        keywords += ", %s, %s" % (clip.channel.name, clip.title)
    return keywords


def create_video_title(clip_title, video_count, video_type, game):
    return "%s | Most Viewed %s Clips Of The %s #%s" % (
        clip_title.upper(), game, video_type.capitalize(), video_count)


def create_channel_compilation_video_title(clip, game, video_count):
    return "%s | Most Viewed %s %s Clips Compilation #%s" % (clip.title.upper(), clip.channel.name, game.full, video_count)


def create_video_description(clips):
    description = ''
    seconds = 0
    for clip in clips:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        timestamp = ("%02d:%02d" % (m, s))
        description += '\n' + timestamp + ' ' + clean_title(clip.channel.name) + ': ' + clean_title(
            clip.title) + '\n' + 'https://clips.twitch.tv/' + clip.slug + '\n'
        seconds = seconds + clip.duration
    return description


def clean_title(title):
    # Remove < and >
    title = title.replace("<", "")
    title = title.replace(">", "")
    return title
