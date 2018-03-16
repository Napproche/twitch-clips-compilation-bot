def createVideoConfig(clips):
    config = {}
    
    config['title'] = createVideoTitle(clips)
    config['description'] = createDescription(clips)
    config['category'] = 20 # Gaming ID
    config['keywords'] = getKeywords()

    return config

def createVideoTitle(clips):
    defualt_title = " | Daily Fortnite Clips"
    return clips[0]['title'] + defualt_title

def createDescription(clips):
    description = ''
    for clip in clips:
        description += '\n' + cleanTitle(clip['title']) + '\n' + ' https://clips.twitch.tv/' + clip['slug'] + '\n'
    return description

def getKeywords():
    return 'Fortnite, Daily, Compilation, Automatic, Bot, Gaming, Twitch, Clips, Twitch clips, Epic Games'

def cleanTitle(title):
    # Remove < and >
    title = title.replace("<", "")
    title = title.replace(">", "")
    return title