from core.models.models import db, Game, Type, Destination, Channel, Clip, Video, VideoClips

if __name__ == "__main__":
    db.connect()
    db.create_tables([Game, Type, Destination, Channel, Clip, Video, VideoClips])

    Type.create(name='day')
    Type.create(name='week')
    Type.create(name='month')
    Type.create(name='compilation')

    Game.create(name='Fortnite', full='Fortnite')
    Game.create(name='Twitch', full='Twitch')    
    Game.create(name='Just%20Chatting', full='Just Chatting')
    Game.create(name='Super%20Smash%20Bros.%20Ultimate', full='Super Smash Bros. Ultimate')