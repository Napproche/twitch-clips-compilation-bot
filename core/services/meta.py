def create_video_config(clips, video_count, video_type, game):
    config = {}
    config['category'] = 20 # Gaming ID
    config['keywords'] = get_keywords(game)

    return config

def get_keywords(game):
    return game + ', Daily, Compilation, Automatic, Bot, Gaming, Twitch, Clips, Twitch clips, Epic Games'

def create_video_title(clip_title, video_count, video_type, game):
    default_title = ""
    if video_type == 'day':
        default_title = " | " + game + " Highlights #" + str(video_count)
    elif video_type == 'week':
        default_title = " | " + game + " Highlights of the Week #" + str(video_count)
    elif video_type == 'month':
        default_title = " | " + game + " Highlights of the Month #" + str(video_count)
    elif video_type == 'compilation':
        default_title = " | " + game + " TODO: USER HERE Compilation #" + str(video_count)

    return clip_title.upper() + default_title

def create_video_description(clips):
    description = ''
    seconds = 0
    for clip in clips:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        timestamp = ("%02d:%02d" % (m, s))
        description += '\n' + timestamp + ' ' + clean_title(clip.channel.name) + ': '+  clean_title(clip.title) + '\n' + 'https://clips.twitch.tv/' + clip.slug + '\n'
        seconds = seconds + clip.duration
    return description

def clean_title(title):
    # Remove < and >
    title = title.replace("<", "")
    title = title.replace(">", "")
    return title