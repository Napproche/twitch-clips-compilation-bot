def createVideoConfig(clips, video_count):
    config = {}
    
    config['title'] = createVideoTitle(clips, video_count)
    config['description'] = createDescription(clips)
    config['category'] = 20 # Gaming ID
    config['keywords'] = getKeywords()

    return config

def createVideoTitle(clips, video_count):
    defualt_title = " | Daily Fortnite Highlights #" + str(video_count)
    return clips[0]['title'].upper() + defualt_title

def createDescription(clips):
    description = ''
    for clip in clips:
        description += '\n' + cleanTitle(clip['title']) + '\n' + 'https://clips.twitch.tv/' + clip['slug'] + '\n'
    return description

def getKeywords():
    return 'Fortnite, Daily, Compilation, Automatic, Bot, Gaming, Twitch, Clips, Twitch clips, Epic Games'

def cleanTitle(title):
    # Remove < and >
    title = title.replace("<", "")
    title = title.replace(">", "")
    return title