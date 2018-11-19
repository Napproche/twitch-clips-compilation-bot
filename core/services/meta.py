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
    default_title = ""
    if video_type == 'day':
        default_title = " | " + game + " Daily Highlights #" + str(video_count)
    elif video_type == 'week':
        default_title = " | " + game + \
            " Highlights of the Week #" + str(video_count)
    elif video_type == 'month':
        default_title = " | " + game + \
            " Highlights of the Month #" + str(video_count)

    return clip_title.upper() + default_title


def create_channel_compilation_video_title(clip, game, video_count):
    return "%s | %s %s Highlight Compilation #%s" % (clip.title.upper(), clip.channel.name, game.name, video_count)


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
