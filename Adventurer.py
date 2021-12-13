# from Room import Room


class Adventurer:

    def __init__(self, game, name: str = None, hit_points: int = 20):
        self.__game = game
        self.__name: str = name
        self.__hit_points: int = hit_points
        self.__healing_potions: int = 0
        self.__vision_potions: int = 0
        self.__pillars: set = set()

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
        # FIXME if down to zero, dies

    def gain_healing_potion(self,):
        self.__healing_potions += 1

    def use_healing_potion(self, hit_points: int = 15):
        self.__healing_potions -= 1
        self.__hit_points += hit_points
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
        # TODO traverse to adjacent room hand off to Game for this.
        # return self.__game.traverse(direction)
        return True

# END
