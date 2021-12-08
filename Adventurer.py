from Room import Room

class Adventurer:

    def __init__(self, name, hit_points):
        self.__name = name
        self.__hit_points = hit_points
        self.__healing_potion = 0
        self.__vision_potion = 0
        self.__pillars = []

    def display_inventory(self):
        # Keeps a list of items in inventory
        print("Inventory:")
        print("Healing potion count: ", self.__healing_potion)
        print("Vision potion count: ", self.__vision_potion)
        print("Pillars: ", self.__pillars)

    def display_status(self):
        print("Adventurer: ", self.__name)
        print("Health: ", self.__hit_points)

    def apply_damage(self, pit_damage):
        print("Fell into pit")
        self.__hit_points = self.__hit_points - pit_damage
        print("Your Heath: " + self.__hit_points)


    
