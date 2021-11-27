from Room import Room

class Adventurer:

    def __init__(self, name, hit_points):
        self.name = ""
        self.hit_points = 100
        Room.healing_potion = 0
        Room.vision_potion = 0
        Room.pillars = []

    
