from core.models.models import Type, Destination, Game

class Parameters:
    def __init__(self, script_name, destination, video_type, count, game):
        destination, created = Destination.get_or_create(name=destination)

        self.destination = Destination.get(name=destination.name)
        self.script_name = script_name
        self.video_type = Type.get(name=video_type)
        self.game = Game.get(name=game)
        self.count = count