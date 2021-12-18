from typing import Optional
# from Room import Room
# from DungeonAdventure import *


class Adventurer:
    default_hit_points_initial = 20
    default_hit_points_max = 100

    def __init__(self, game=None, name: str = None, hit_points: int = None, hit_points_max: int = None):
        self.__game = game
        self.__name: str = name
        self.__hit_points: int = hit_points
        self.__hit_points_max: int = hit_points_max
        self.__healing_potions: int = 0
        self.__vision_potions: int = 0
        self.__pillars: set = set()  # empty

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, val: str) -> None:
        self.__name = val

    @property
    def game(self):
        return self.__game

    @property
    def hit_points(self) -> int:
        return self.__hit_points

    @hit_points.setter
    def hit_points(self, val: int) -> None:
        if val is not None:
            self.__hit_points = val
        elif self.game is not None:
            self.__hit_points = self.game.default_hit_points_initial

    @property
    def hit_points_max(self) -> int:
        return self.__hit_points_max

    @hit_points_max.setter
    def hit_points_max(self, val: int) -> None:
        if val is not None:
            self.__hit_points_max = val
        elif self.game is not None:
            self.__hit_points_max = self.game.default_hit_points_max

    @property
    def is_alive(self) -> bool:
        return self.hit_points > 0

    @property
    def healing_potions(self) -> int:
        return self.__healing_potions

    @healing_potions.setter
    def healing_potions(self, val: int) -> None:
        self.__healing_potions = val

    @property
    def vision_potions(self) -> int:
        return self.__vision_potions

    @vision_potions.setter
    def vision_potions(self, val: int) -> None:
        self.__vision_potions = val

    @property
    def pillars(self) -> set:
        return self.__pillars

    def has_pillar(self, pillar):
        return bool(pillar in self.pillars)

    def display_inventory(self):
        # Keeps a list of items in inventory
        print("Inventory...")
        print(f"Healing potions: {self.healing_potions}")
        print(f"Vision potions:  {self.vision_potions}")
        print(f"Pillars: {', '.join(self.pillars)}")

    def display_status(self):
        print(f"Adventurer: {self.name}")
        print(f"Health: {self.hit_points}")

    def take_damage(self, damage: int = 1):
        self.hit_points -= damage
        if self.hit_points <= 0:
            self.hit_points = 0
            self.game.continues = False

    def gain_healing_potion(self,):
        self.healing_potions += 1

    def use_healing_potion(self, hit_points: int = 15) -> int:
        if self.healing_potions <= 0:
            return -1
        self.healing_potions -= 1
        self.hit_points += hit_points
        if self.hit_points > self.hit_points_max:
            self.hit_points = self.hit_points_max
        return self.healing_potions

    def gain_vision_potion(self):
        self.vision_potions += 1

    def use_vision_potion(self) -> int:
        if self.vision_potions <= 0:
            return -1
        self.vision_potions -= 1
        # TODO adjust visible rooms (call a method in game for this)
        return self.vision_potions

    def gain_pillar(self, pillar_name):
        self.pillars.add(pillar_name)

# END
