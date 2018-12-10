from core.models.models import Type, Destination, Game

class Parameters:
    def __init__(self, script_name, destination, video_type, count, game, custom_thumbnails=False):
        destination, created = Destination.get_or_create(name=destination)

        self.destination = Destination.get(name=destination.name)
        self.script_name = script_name
        self.video_type = Type.get(name=video_type)
        self.game = Game.get(cli=game)
        self.count = count
        self.custom_thumbnails = bool(int(custom_thumbnails))