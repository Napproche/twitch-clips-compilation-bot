def create_video_config(clips, game, title, file, destination):
    config = {}
    config['category'] = 20  # Gaming ID
    config['keywords'] = get_keywords(game, clips)
    config['description'] = create_video_description(clips)
    config['title'] = title
    config['file'] = file
    config['destination'] = destination

    return config


def get_keywords(game, clips):
    keywords = game + ', Daily, Compilation, Gaming'
    for clip in clips:
        keywords += ", %s, %s" % (clip.channel.name, clip.title)
    return keywords


def create_video_title(clip_title, video_count, video_type, game):
    return "%s | Most Viewed %s Clips Of The %s #%s" % (
        shorten_title_if_needed(clip_title.upper(), 45), game, video_type.capitalize(), video_count)


def create_channel_compilation_video_title(clip, game, video_count):
    return "%s | Most Viewed %s %s Clips Compilation #%s" % (shorten_title_if_needed(clip.title.upper(), 45), clip.channel.name, game.full, video_count)


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
    """
        Remove < and >
    """
    title = title.replace("<", "")
    title = title.replace(">", "")
    return title


def shorten_title_if_needed(title, max_chars):
    """
        Strip title if needed to fit in the max length of 100 chars of a YouTube video.
    """
    return (title[:max_chars] + '...') if len(title) > max_chars else title
