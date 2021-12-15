from Room import Room
#from DungeonAdventure import *


class Adventurer:

    def __init__(self, game, name: str = None, hit_points: int = 20):
        self.__game = game
        self.__name: str = name
        self.__hit_points: int = hit_points
        self.__healing_potions: int = 0
        self.__vision_potions: int = 0
        self.__pillars: set = set()
        self.__coords = (0,0)

    @property
    def name(self):
        return self.__name

    @property
    def game(self):
        return self.__game

    @property
    def hit_points(self):
        return self.__hit_points

    @property
    def healing_potions(self):
        return self.__healing_potions

    @property
    def vision_potions(self):
        return self.__vision_potions

    @property
    def pillars(self):
        return self.__pillars

    def display_inventory(self):
        # Keeps a list of items in inventory
        print("Inventory...")
        print(f"Healing potion count: {self.__healing_potions}")
        print(f"Vision potion count: {self.__vision_potions}")
        print(f"Pillars: {', '.join(self.__pillars)}")

    def display_status(self):
        print(f"Adventurer: {self.__name}")
        print(f"Health: {self.__hit_points}")

    def take_damage(self, damage: int = 10):
        self.__hit_points -= damage
        if self.__hit_points <= 0:
            self.dissolve()
        # FIXME if down to zero, dies

    def dissolve(self):
        print("Your molecules have dissolved and become one with the universe.")

    def gain_healing_potion(self,):
        self.__healing_potions += 1

    def use_healing_potion(self, hit_points: int = 15):
        if self.__healing_potions == 0:
            print("You have bravely neglected to notice that you do not have any healing potions.")
            return
        self.__healing_potions -= 1
        self.__hit_points += hit_points
        if self.__hit_points > 100:
            self.__hit_points = 100
        print("You have " + str(self.__hit_points) + " hit points now.")
        # FIXME cannot exceed some max threshold

    def gain_vision_potion(self):
        self.__vision_potions += 1

    def use_vision_potion(self):
        self.__vision_potions -= 1
        # TODO adjust visible rooms, hand off to Game for this
        # return self.__game.envision()

    def gain_pillar(self, pillar_name):
        self.__pillars.add(pillar_name)

    def move(self, direction) -> bool:
        """ Try to step in a a direction.
        Return True if successful, False if cannot.
        """
        if direction == "North":
            self.__coords[0] -= 1
        elif direction == "East":
            self.__coords[1] -= 1
        elif direction == "South":
            self.__coords[0] += 1
        elif direction == "West":
            self.__coords[1] += 1

        # TODO traverse to adjacent room hand off to Game for this.
        # return self.__game.traverse(direction)
        return True

# END
