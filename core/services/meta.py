def create_video_config(clips, video_count, video_type, game):
    config = {}
    
    config['title'] = create_video_title(clips, video_count, video_type, game)
    config['description'] = create_video_description(clips)
    config['category'] = 20 # Gaming ID
    config['keywords'] = get_keywords(game)

    return config

def create_video_title(clips, video_count, video_type, game):
    if video_type == 'day':
        defualt_title = " | " + game + " Highlights #" + str(video_count)
    elif video_type == 'week':
        defualt_title = " | " + game + " Highlights of the Week #" + str(video_count)
    elif video_type == 'month':
        defualt_title = " | " + game + " Highlights of the Month #" + str(video_count)

    return clips[0]['title'].upper() + defualt_title

def create_video_description(clips):
    description = ''
    seconds = 0
    for clip in clips:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        timestamp = ("%02d:%02d" % (m, s))
        description += '\n' + timestamp + ' ' + clean_title(clip['channel_display_name']) + ': '+  clean_title(clip['title']) + '\n' + 'https://clips.twitch.tv/' + clip['slug'] + '\n'
        seconds = seconds + clip['duration']
    return description

def get_keywords(game):
    return game + ', Daily, Compilation, Automatic, Bot, Gaming, Twitch, Clips, Twitch clips, Epic Games'

def clean_title(title):
    # Remove < and >
    title = title.replace("<", "")
    title = title.replace(">", "")
    return title