def createVideoConfig(clips, video_count, period):
    config = {}
    
    config['title'] = createVideoTitle(clips, video_count, period)
    config['description'] = createDescription(clips)
    config['category'] = 20 # Gaming ID
    config['keywords'] = getKeywords()

    return config

def createVideoTitle(clips, video_count, period):
    if period == 'day':
        defualt_title = " | Fortnite Highlights of the Day #" + str(video_count)
    elif period == 'week':
        defualt_title = " | Fortnite Highlights of the Week #" + str(video_count)
    elif period == 'month':
        defualt_title = " | Fortnite Highlights of the Month #" + str(video_count)

    return clips[0]['title'].upper() + defualt_title

def createDescription(clips):
    description = ''
    seconds = 0
    for clip in clips:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        timestamp = ("%02d:%02d" % (m, s))
        description += '\n' + timestamp + ' ' + cleanTitle(clip['title']) + '\n' + 'https://clips.twitch.tv/' + clip['slug'] + '\n'
        seconds = seconds + clip['duration']
    return description

def getKeywords():
    return 'Fortnite, Daily, Compilation, Automatic, Bot, Gaming, Twitch, Clips, Twitch clips, Epic Games'

def cleanTitle(title):
    # Remove < and >
    title = title.replace("<", "")
    title = title.replace(">", "")
    return title