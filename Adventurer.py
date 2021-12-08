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

    # def healing potion pick up, increase healing potion by 1 in inventory
    def healing_pickup(self,):
        self.__healing_potion = self.__healing_potion + 1

    # def drink healing potion, increase hit points by 15, decrease healing potion by 1
    def drink_healing_potion(self, hit_points):
        self.__hit_points = self.__hit_points + 15
        self.__healing_potion = self.__healing_potion - 1

    # def vision potion pick up, increase vision potion by 1 in inventory
    def vision_potion(self):
        self.__vision_potion = self.__vision_potion + 1

    # def drink vision potion, decrease vision potion by 1 in inventory
    def drink_vision_potion(self):
        self.__vision_potion = self.__vision_potion - 1

    # pick up pillar, increase
    def pillar_pickup(self, pillar_name):
        self.__pillars.append(pillar_name)


    
